# Deployment

This document describes the deployment requirements and environment model for the Flask Band Website CMS.

The repository includes a tested reference architecture based on Gunicorn, Nginx, Redis and systemd. The application is not tied to a specific hosting provider.

## Environments

The project distinguishes between two application environments:

- `development`
- `production`

The environment is selected using `APP_ENV`.

If `APP_ENV` is not set, the application defaults to development mode.

## Development

Local development uses:

    APP_ENV=development

The application can be started with:

    python run.py

The Flask development server is intended only for local development and must not be used as the public production server.

Development may use:

- SQLite
- In-memory rate-limit storage
- HTTP
- Flask debug mode

## Staging

A staging environment is recommended before deploying the application publicly.

A typical staging deployment may provide:

- Production-mode Flask configuration
- Gunicorn WSGI serving
- Nginx reverse proxy
- HTTPS termination
- Redis-backed rate limiting
- SQLite database
- Direct Nginx serving of static assets
- systemd service management
- Desktop and mobile testing
- CMS and upload testing

Staging can be used for functional, deployment, proxy, HTTPS, performance, security and content-management testing.

## Production

Production uses:

    APP_ENV=production

The application performs startup checks for required production configuration and refuses to start if required security settings are missing.

Production requirements include:

- Debug mode disabled
- Strong unique `SECRET_KEY`
- Explicit `TRUSTED_HOSTS`
- Persistent/shared rate-limit storage
- HTTPS
- Production WSGI server
- Secure session cookies
- Database backups
- Monitoring
- Security review

## Environment Variables

### APP_ENV

Selects the application environment.

Example:

    APP_ENV=production

### SECRET_KEY

Used by Flask for cryptographic signing of sessions and other security-sensitive data.

A unique cryptographically strong value is required in production.

Never commit the production secret key to Git.

When rebuilding an installation, a new cryptographically strong `SECRET_KEY` can be generated. Changing the key intentionally invalidates existing user sessions and CSRF tokens.

### DATABASE_URL

Defines the application database connection.

SQLite can be used for small deployments:

    DATABASE_URL=sqlite:///instance/band_website.db

Other database backends may be configured according to deployment requirements.

### RATELIMIT_STORAGE_URI

Defines the storage backend used by Flask-Limiter.

Development may use:

    memory://

Production must not use in-memory storage.

A persistent or shared backend such as Redis should be used in production.

Example:

    RATELIMIT_STORAGE_URI=redis://127.0.0.1:6379/0

### TRUSTED_HOSTS

Defines the HTTP Host values accepted by Flask.

Production requires this setting.

Multiple hosts are comma-separated.

Example:

    TRUSTED_HOSTS=example.com,www.example.com

The configured values must match the deployment's domain configuration.

## HTTPS and Reverse Proxy

Production deployments should use HTTPS.

HTTP Strict Transport Security (HSTS) should be enabled only after the site is confirmed to operate exclusively over HTTPS.

Werkzeug `ProxyFix` should be configured only when the application runs behind a trusted reverse proxy and the proxy topology is known.

Proxy settings must not be guessed.

## WSGI Server

`run.py` is the local development entry point.

The reference deployment uses Gunicorn as the production WSGI server.

Gunicorn is managed by systemd and listens only on the loopback interface. Nginx acts as the public-facing reverse proxy.

The application backend should not be exposed directly to the network.

## Secrets

Real secrets must never be committed to the repository.

The repository includes `.env.example` as a configuration template only.

Local `.env` files and environment-specific secret files are excluded through `.gitignore`.

## Reference Deployment Architecture

The included reference configuration uses:

    HTTPS client connection
        ↓
    Nginx on TCP 443
        ↓
    Gunicorn on 127.0.0.1:8000
        ↓
    Flask application
        ↓
    SQLite database + Redis rate-limit storage

Gunicorn is managed by systemd and is not exposed directly to the network.

Nginx terminates TLS and forwards requests to Gunicorn.

Nginx also serves `/static/` directly from the application static directory. CSS, JavaScript, bundled images and runtime-uploaded public images therefore do not pass through Gunicorn or Flask.

The application uses Werkzeug `ProxyFix` in production configuration and trusts one reverse proxy hop.

Reference configuration templates are stored in:

- `deploy/nginx/band-website-staging.conf.example`
- `deploy/systemd/band-website-staging.service.example`

Real hostnames, secrets, certificates and environment files must not be committed to the repository.

## Deployment Checklist

1. Clone the repository.
2. Create a Python virtual environment with a supported Python version.
3. Install Linux deployment requirements:

       python -m pip install -r requirements-linux.txt

4. Create the local `.env` file from `.env.example`.
5. Set production values:
   - `APP_ENV=production`
   - strong `SECRET_KEY`
   - appropriate `DATABASE_URL`
   - persistent Redis `RATELIMIT_STORAGE_URI`
   - correct `TRUSTED_HOSTS`
6. Run database migrations:

       python -m flask --app run.py db upgrade

7. Create or restore application content as required.
8. Install the systemd service using the provided example.
9. Start and enable the application service.
10. Verify that Gunicorn listens only on the loopback interface.
11. Configure Nginx using the provided example.
12. Verify that `/static/` is served directly by Nginx rather than Gunicorn.
13. Validate the Nginx configuration before reloading:

       sudo nginx -t

14. Verify HTTPS and certificate validation.
15. Test public pages.
16. Test admin login, logout and CSRF-protected forms.
17. Review application and Nginx logs for errors.

The application backend must not be exposed directly to the public network.