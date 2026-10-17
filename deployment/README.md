# Production edge configuration

## Render

Use the repository root as the service root. Configure the service with:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn myproject.wsgi:application`

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
