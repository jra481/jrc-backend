# AWS EC2 deployment

This backend is a Django application deployed to an Ubuntu 24.04 LTS EC2
instance. The supported layout is:

```text
Internet -> EC2 security group -> Nginx :443 -> Gunicorn 127.0.0.1:8000 -> Django
                                                        |-> Neon PostgreSQL (recommended)
                                                        |-> local Memcached 127.0.0.1:11211
```

The EC2 instance does not need to run PostgreSQL when the existing Neon
database is kept. If the database is moved to AWS later, set the `DB_*`
variables instead of `DATABASE_URL` and keep MySQL bound to localhost or a
private subnet.

## 1. AWS prerequisites

Create an Ubuntu 24.04 LTS 64-bit EC2 instance. A small general-purpose
instance is enough to start; increase the instance size after observing CPU
and memory usage. Allocate an Elastic IP and create a DNS `A` record such as
`api.example.com` pointing to it.

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
ALLOWED_HOSTS=api.example.com
DEPLOYMENT_ALLOWED_HOSTS=api.example.com
SITE_URL=https://jrc-frontend.vercel.app
STOREFRONT_ORIGINS=https://jrc-frontend.vercel.app
DATABASE_URL=postgresql://<user>:<url-encoded-password>@<neon-pooler-host>/<database>?sslmode=require
MEMCACHED_LOCATION=127.0.0.1:11211
RUN_MIGRATIONS_ON_START=false
JWT_COOKIE_SAMESITE=None
TRUST_PROXY_SSL_HEADER=true
```

Add the Google, SMTP, Stripe, WhatsApp, and any other application secrets to
the same file. Keep `JWT_COOKIE_DOMAIN` empty. `JWT_COOKIE_SAMESITE=None` is
required when the Vercel storefront calls the API on a different site; use
`Lax` only when the frontend and API are served through the same site/proxy.

The database password must be URL-encoded inside `DATABASE_URL`. Never use
`127.0.0.1` as the database host unless the database is installed on this
same EC2 instance.

In the frontend's Vercel project settings, set the production build variable
`VITE_API_BASE_URL=https://api.example.com/api` and redeploy the frontend. Do
not leave the production value as `/api` unless Vercel is explicitly
configured with a proxy rewrite to the EC2 API.

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

## 5. Nginx and HTTPS

Copy `nginx/eehook-api.conf.example` to
`/etc/nginx/sites-available/eehook-api.conf`, replace `api.example.com` with
the real hostname, and obtain the certificate before enabling the final
HTTPS-enabled config:

```bash
sudo certbot certonly --standalone -d api.example.com \
  --pre-hook "systemctl stop nginx" \
  --post-hook "systemctl start nginx"
sudo ln -s /etc/nginx/sites-available/eehook-api.conf /etc/nginx/sites-enabled/eehook-api.conf
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl reload nginx
```

The template proxies only to `127.0.0.1:8000`, serves Django static/media
files, redirects HTTP to HTTPS, and sets the trusted forwarded protocol used
by Django. Keep port 8000 closed in both the EC2 security group and UFW.

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

From any machine that can reach the DNS record:

```bash
curl -fsS https://api.example.com/health/
```

The response should report the API as healthy. If it fails, inspect both
`sudo journalctl -u eehook-backend` and `/var/log/nginx/error.log`. Check that
DNS, the EC2 security group, UFW, `ALLOWED_HOSTS`, CORS origins, and the
database URL all match the deployed hostnames.
