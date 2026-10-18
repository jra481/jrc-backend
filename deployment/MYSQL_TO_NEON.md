# Migrate the MySQL data to Neon PostgreSQL

The application schema is created by Django migrations. The safest migration
for this project is:

1. Export rows from the old MySQL database with Django.
2. Create the schema in Neon with Django migrations.
3. Import the rows into Neon with Django.
4. Reset PostgreSQL sequences so new rows receive correct IDs.

Do this during a maintenance window. Keep the old MySQL database unchanged
until the Neon deployment has been verified.

## 1. Export from MySQL

Set the old MySQL values in a local `.env` file and leave `DATABASE_URL` unset:

```text
DEBUG=True
DB_NAME=EEHOOK
DB_USER=<mysql-user>
DB_PASSWORD=<mysql-password>
DB_HOST=<mysql-host>
DB_PORT=3306
```

Then run from the repository root:

```powershell
python manage.py dumpdata --all --natural-foreign --natural-primary `
  --exclude admin.logentry `
  --exclude contenttypes `
  --exclude auth.permission `
  --exclude sessions.session `
  --exclude token_blacklist `
  --indent 2 --output mysql-data.json
```

Do not commit `mysql-data.json`; it contains user and order data. Delete it
after the import is complete.

## 2. Connect to Neon and create the schema

Replace the database settings in `.env` with the pooled Neon connection string
from the Neon Console:

```text
DATABASE_URL=postgresql://<user>:<password>@<endpoint>-pooler.<region>.aws.neon.tech/neondb?sslmode=require
```

The password must be URL-encoded if it contains characters such as `@`, `#`,
`/`, or `:`. Run:

```powershell
python manage.py migrate --noinput
python manage.py check
```

## 3. Import the data

```powershell
python manage.py loaddata mysql-data.json
```

Reset sequences after the import:

```powershell
python manage.py sqlsequencereset admin auth contenttypes sessions token_blacklist myapp payment | python manage.py dbshell
```

If `dbshell` is unavailable locally, install the PostgreSQL client or run the
SQL emitted by `sqlsequencereset` in the Neon SQL Editor.

## 4. Render configuration

Set `DATABASE_URL` in the Render web service to the Neon pooled connection
string. Remove old `DB_HOST`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` values or
leave them unused; `DATABASE_URL` takes precedence. Keep the start command:

```text
python manage.py migrate --noinput && gunicorn myproject.wsgi:application
```

Never use `127.0.0.1` or `localhost` for the Neon host.

## Important non-database data

`dumpdata` migrates database rows only. Copy the `uploads/` media directory to
the production media storage separately, or existing product/user images will
not be available after the database switch.
