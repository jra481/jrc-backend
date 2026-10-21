# AWS EC2 deployment

This backend is a Django application deployed to an Ubuntu 24.04 LTS EC2
instance. The supported layout is:

```text
Browser -> Vercel HTTPS -> EC2 :80 -> Nginx -> Gunicorn 127.0.0.1:8000 -> Django
                                                               |-> Neon PostgreSQL
                                                               |-> local Memcached 127.0.0.1:11211
```

The EC2 instance does not need to run PostgreSQL when the existing Neon
database is kept. If the database is moved to AWS later, set the `DB_*`
variables instead of `DATABASE_URL` and keep MySQL bound to localhost or a
private subnet.

## 1. AWS prerequisites

Create an Ubuntu 24.04 LTS 64-bit EC2 instance. A small general-purpose
instance is enough to start; increase the instance size after observing CPU
and memory usage. Allocate an Elastic IP. The current frontend uses a Vercel
external rewrite to the fixed backend address `13.50.221.204`, so a separate
API DNS record is not required for this proxy setup.

Configure the instance security group with these inbound rules:

- TCP 22 only from your administration IP range
- TCP 80 from the internet (needed for the certificate challenge and HTTP redirect)
- TCP 443 from the internet

Do not expose TCP 8000 or TCP 11211. The instance firewall below also keeps
those ports private.

Connect using the EC2 key pair and the Ubuntu user:

```bash
ssh -i /path/to/key.pem ubuntu@<elastic-ip>
```

## 2. Install the VM dependencies

Run the following on the EC2 instance:

```bash
sudo apt update
sudo apt install -y git python3-venv python3-dev build-essential nginx memcached certbot python3-certbot-nginx
sudo adduser --system --group --home /srv/eehook-backend deploy
sudo install -d -o deploy -g deploy /srv/eehook-backend
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
```

Clone the repository and install the dependencies:

```bash
sudo -u deploy git clone https://github.com/jra481/jrc-backend.git /srv/eehook-backend
cd /srv/eehook-backend
sudo -u deploy python3 -m venv .venv
sudo -u deploy .venv/bin/python -m pip install --upgrade pip
sudo -u deploy .venv/bin/pip install -r requirements.txt
sudo sed -i 's/^#\?\s*-l .*/-l 127.0.0.1/' /etc/memcached.conf
sudo sed -i 's/^#\?\s*-U .*/-U 0/' /etc/memcached.conf
sudo systemctl enable --now memcached
```

Memcached is intentionally bound to localhost. Verify it with:

```bash
sudo ss -ltnp | grep 11211
```

## 3. Configure production environment

Create the root-owned environment file and fill it with real production
values. Do not commit this file:

```bash
sudo cp /srv/eehook-backend/.env.example /etc/eehook-backend.env
sudo chown root:deploy /etc/eehook-backend.env
sudo chmod 640 /etc/eehook-backend.env
sudoedit /etc/eehook-backend.env
```

At minimum, set:

```dotenv
DEBUG=False
SECRET_KEY=<strong-random-secret-at-least-50-characters>
ALLOWED_HOSTS=13.50.221.204,jrc-frontend.vercel.app
DEPLOYMENT_ALLOWED_HOSTS=13.50.221.204,jrc-frontend.vercel.app
SITE_URL=https://jrc-frontend.vercel.app
STOREFRONT_ORIGINS=https://jrc-frontend.vercel.app
DATABASE_URL=postgresql://<user>:<url-encoded-password>@<neon-pooler-host>/<database>?sslmode=require
MEMCACHED_LOCATION=127.0.0.1:11211
RUN_MIGRATIONS_ON_START=false
JWT_COOKIE_SAMESITE=Lax
TRUST_PROXY_SSL_HEADER=true
```

Add the Google, SMTP, Stripe, WhatsApp, and any other application secrets to
the same file. Keep `JWT_COOKIE_DOMAIN` empty. Because the Vercel rewrite
keeps API calls same-origin in the browser, `JWT_COOKIE_SAMESITE=Lax` is the
appropriate setting for this proxy setup.

The database password must be URL-encoded inside `DATABASE_URL`. Never use
`127.0.0.1` as the database host unless the database is installed on this
same EC2 instance.

In the frontend's Vercel project settings, remove any old Render API value.
Leave `VITE_API_BASE_URL` unset or set it to `/api`, then redeploy. The
repository's `vercel.json` proxies `/api/*` and `/media/*` to EC2.

## 4. First release

Run the checks, migrations, and static collection as the `deploy` user:

```bash
cd /srv/eehook-backend
sudo -u deploy .venv/bin/python manage.py check --deploy
sudo -u deploy .venv/bin/python manage.py migrate --noinput
sudo -u deploy .venv/bin/python manage.py collectstatic --noinput
sudo install -d -o deploy -g deploy /srv/eehook-backend/uploads
```

Install and start the systemd service:

```bash
sudo cp /srv/eehook-backend/deployment/aws-ec2/eehook-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now eehook-backend
sudo systemctl status eehook-backend --no-pager
```

The service runs Gunicorn on localhost only. It uses two workers and two
threads, a conservative starting point for a small EC2 instance.

## 5. Nginx and the Vercel proxy

Copy `nginx/eehook-api-proxy.conf.example` to
`/etc/nginx/sites-available/eehook-api.conf` and enable it:

```bash
sudo cp /srv/eehook-backend/deployment/nginx/eehook-api-proxy.conf.example \
  /etc/nginx/sites-available/eehook-api.conf
sudo ln -s /etc/nginx/sites-available/eehook-api.conf /etc/nginx/sites-enabled/eehook-api.conf
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl reload nginx
```

Vercel terminates browser HTTPS. The EC2 template accepts the proxy traffic
on port 80, proxies to `127.0.0.1:8000`, serves Django static/media files,
and marks the forwarded request as HTTPS for Django. Keep port 8000 and
11211 closed in both the EC2 security group and UFW. For end-to-end TLS
directly to EC2, replace this proxy mode later with a custom API domain and
the HTTPS Nginx template.

## 6. Updates

Use this release sequence for subsequent deployments:

```bash
cd /srv/eehook-backend
sudo -u deploy git pull --ff-only origin main
sudo -u deploy .venv/bin/pip install -r requirements.txt
sudo -u deploy .venv/bin/python manage.py migrate --noinput
sudo -u deploy .venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart eehook-backend
sudo journalctl -u eehook-backend -n 100 --no-pager
```

Migrations run once before the service restart. Keeping
`RUN_MIGRATIONS_ON_START=false` prevents every Gunicorn worker from attempting
to migrate during a restart.

## 7. Verify the deployment

After the frontend is redeployed, verify through the Vercel domain:

```bash
curl -fsS https://jrc-frontend.vercel.app/api/health/
```

The response should report the API as healthy. If it fails, inspect both
`sudo journalctl -u eehook-backend` and `/var/log/nginx/error.log`. Check that
the EC2 security group, UFW, Vercel rewrites, `ALLOWED_HOSTS`, CORS origins,
and the database URL all match the deployed hostnames.
