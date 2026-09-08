# Flask Band Website CMS

A production-oriented band website and lightweight content management system
built with Flask.

This repository is a sanitized and generalized version of a real-world band
website project. Band-specific content, private infrastructure details,
credentials, production data, and original media assets have been removed or
replaced with generic demo content.

The project is published as a practical example of building a traditional,
server-rendered website and custom CMS without a large frontend framework.

## Features

### Public Website

The public website includes:

- Home page
- News
- Band biography and member profiles
- Discography and tracklists
- Upcoming and past shows
- Media gallery
- YouTube video integration
- Merchandise catalog
- Contact information
- Social links

The site is mobile-first and uses server-rendered Jinja templates with
lightweight vanilla JavaScript where needed.

### Administration

A dedicated `/admin` interface allows authorized users to manage website
content without editing source files.

CMS functionality includes:

- News and site updates
- Shows and poster information
- Releases and tracklists
- Media photos
- YouTube videos
- Band members
- Structured member activity history
- Band biography
- Contact information
- Social links
- Featured homepage content
- Merchandise
- Merchandise image uploads
- Pricing and availability
- Optional stock tracking

The administration interface is designed to work on both desktop and mobile
devices.

## Image Upload Pipeline

CMS-managed image uploads are processed by a reusable upload service.

Uploaded images are:

1. Decoded with Pillow instead of trusting the filename extension.
2. Checked against supported image formats.
3. Subject to configured request-size limits.
4. Resized when necessary while preserving aspect ratio.
5. Re-encoded as WebP.
6. Stored using randomly generated filenames.

Runtime uploads are excluded from Git.

## Technology

The application uses:

- Python
- Flask
- Jinja
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-WTF
- Flask-Limiter
- Pillow
- SQLite
- Redis for production rate-limit storage
- Gunicorn
- Nginx
- HTML
- CSS
- Vanilla JavaScript

The project intentionally avoids a frontend framework because the application
does not require one.

## Architecture

The application uses the Flask application-factory pattern and separates the
public website and administration interface into dedicated blueprints.

A typical production request path is:

    Dynamic requests:
    Browser -> Nginx -> Gunicorn -> Flask

    Static assets:
    Browser -> Nginx -> static files

Gunicorn should listen only on a loopback or otherwise appropriately protected
interface when used behind Nginx.

Architecture details are documented in
[`ARCHITECTURE.md`](ARCHITECTURE.md).

## Development Setup

Create and activate a virtual environment.

Windows PowerShell:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

Linux:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

Copy or configure the required environment variables using
[`.env.example`](.env.example) as a reference.

For local development, the default database can use SQLite:

    DATABASE_URL=sqlite:///band_website.db

Development rate limiting can use in-memory storage:

    RATELIMIT_STORAGE_URI=memory://

Production deployments should use persistent/shared rate-limit storage such as
Redis.

## Database Setup

The project uses Flask-Migrate/Alembic for schema migrations.

Apply the existing migrations:

    flask db upgrade

Create an administrator account:

    flask create-admin

Optional generic demo content can be added with:

    flask seed-demo

Never commit a development or production database containing real data.

## Running Locally

Start the Flask development server using the project's development entry
point:

    python run.py

The Flask development server is intended for local development only.

Use a production WSGI server such as Gunicorn for deployment.

## Production Deployment

A typical production deployment consists of:

    Internet
       |
       v
     Nginx
       |
       v
    Gunicorn
       |
       v
     Flask
       |
       v
    Database

Example deployment templates are available under:

    deploy/nginx/
    deploy/systemd/

Detailed deployment guidance is available in
[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

The application is not tied to a particular hosting provider or hardware
platform.

## Security

Security controls implemented in the application include:

- Password hashing
- Authentication and authorization
- Secure session handling
- CSRF protection
- Login rate limiting
- Persistent/shared production rate-limit storage
- Form validation
- Email and URL validation
- Local-path validation
- Secure production cookie settings
- Trusted Host validation
- Content Security Policy
- Security response headers
- Production error handling
- Request-size limits
- Image format validation
- Image decoding and re-encoding
- Generated upload filenames
- Security-relevant audit logging
- Reverse-proxy handling
- Production configuration validation

Production startup validates security-sensitive configuration rather than
silently falling back to unsafe defaults.

Secrets and environment-specific credentials must never be committed to Git.

## Configuration

Important environment variables include:

- `APP_ENV`
- `SECRET_KEY`
- `DATABASE_URL`
- `RATELIMIT_STORAGE_URI`
- `TRUSTED_HOSTS`

See [`.env.example`](.env.example) for examples.

Production environments should use:

- A unique cryptographically strong `SECRET_KEY`
- HTTPS
- Secure cookies
- Explicit trusted hosts
- Persistent/shared rate-limit storage
- A reverse proxy configured to pass the expected forwarding headers
- Regular database and uploaded-media backups

## Demo Assets and Content

The original project-specific content is intentionally not included in this
repository.

The public version uses generic demo branding and media assets so the
application structure can be explored without redistributing the original
website's photographs, artwork, logos, production database, or private
configuration.

Demo content is not intended to represent a real band.

## Repository Scope

This repository demonstrates the application code, CMS architecture,
deployment patterns, and security controls used by the project.

It intentionally does not contain:

- Production credentials or secrets
- Production databases
- Runtime uploads
- Private infrastructure documentation
- Backup configuration
- Original project-specific media
- Private Git history

The public repository starts with a clean history created from the sanitized
source snapshot.

## License

See the repository's `LICENSE` file for license terms.
