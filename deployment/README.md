# Production edge configuration

## Render

Use the repository root as the service root. Configure the service with:

- Build command: `pip install -r requirements.txt`
- Start command: `python manage.py migrate --noinput && gunicorn myproject.wsgi:application`

Configure the database before deploying. The application reads Render's
`DATABASE_URL` for either PostgreSQL (`postgresql://...`) or MySQL
(`mysql://...`). If `DATABASE_URL` is not available, configure all of
`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` instead. Do not
set `DB_HOST` to `127.0.0.1` or `localhost` on Render unless a database server
is running in the same container; that is the cause of the common
`Can't connect to MySQL server on '127.0.0.1'` deployment failure.

The migration step is required because the homepage API reads the newer
`HomepageLink`, `TrustBenefit`, brand, and vehicle catalog schema. It is
idempotent, so restarts safely skip migrations that are already applied. If a
Render dashboard start command overrides the Procfile, use the command above
there as well.

The WSGI entrypoint also runs migrations by default (`RUN_MIGRATIONS_ON_START=true`)
so an explicit Render start command cannot accidentally serve an outdated schema.
Set it to `false` only when a dedicated release step runs migrations before the
web process starts.

The WSGI module is `myproject.wsgi`; this is a Django application, so
`gunicorn app:app` will fail with `ModuleNotFoundError: No module named 'app'`.
The root `Procfile` contains the same start command for deployments that read
their command from the repository.

Django allows Render's public service hostname automatically when Render
provides `RENDER_EXTERNAL_HOSTNAME` (or `RENDER_EXTERNAL_URL`). If those
variables are unavailable, set `ALLOWED_HOSTS` or `DEPLOYMENT_ALLOWED_HOSTS`
to include the exact backend hostname, for example
`jrc-backend-xgsd.onrender.com`. Do not use `*` in production.

Terminate TLS at either an AWS Application Load Balancer or Nginx.  In both
cases, listen publicly only on HTTPS and redirect HTTP with a permanent 301.

For an EC2 Nginx deployment, adapt `nginx/eehook-api.conf.example`, install a
valid certificate (for example, Certbot), and proxy only to Gunicorn on
`127.0.0.1:8000`.  Do not expose Gunicorn's port in the EC2 security group.

For an ALB deployment, configure an HTTP:80 listener whose only action is a
redirect to HTTPS:443; configure the HTTPS listener to forward to a private
target group.  The load balancer must overwrite `X-Forwarded-Proto` with
`https`.  Keep the instance security group limited to the ALB security group.

Set `STOREFRONT_ORIGINS` to every exact HTTPS browser origin allowed to send
credentialed requests. This must include the deployed Jamal Rafeeq storefront
origin (`https://jrc-frontend.vercel.app`) as well as any custom storefront
domains. For a same-origin
storefront `/api` proxy, keep
`JWT_COOKIE_SAMESITE=Lax`; only use `None` when the browser calls a genuinely
cross-site API origin directly.

Configure `MEMCACHED_LOCATION` to a reachable shared Memcached service. The
application defaults `MEMCACHED_IGNORE_EXCEPTIONS=true`, so a temporary cache
outage leaves the API available while cache-backed throttles degrade safely;
set it to `false` when the deployment requires throttling to fail closed.
