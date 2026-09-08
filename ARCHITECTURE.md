# Architecture

## Overview

Flask Band Website CMS is a Flask-based web application consisting of two
primary areas:

1. Public band website
2. Administration interface

Both are part of the same application but are kept logically separated.

## High-Level Architecture

The application is organized around a Flask application factory and separate
public and administration blueprints.

A typical production deployment uses Nginx and Gunicorn:

    Browser
       |
       v
     Nginx
       |
       +-- /static/ assets ---> Static files
       |
       +-- Dynamic requests
                  |
                  v
              Gunicorn
                  |
                  v
          Flask Application
               Factory
                  |
           +------+------+
           |             |
           v             v
    Public Blueprint  Admin Blueprint
           |             |
           +------+------+
                  |
                  v
          SQLAlchemy Models
                  |
                  v
              Database

Static assets can be served directly by Nginx. Dynamic application requests
are forwarded to Gunicorn, which runs the Flask application.

## Public Website

Primary public routes:

    /
    ├── /band
    ├── /music
    ├── /live
    ├── /media
    ├── /merch
    └── /contact

The public website is mobile-first and designed to remain lightweight.

Jinja templates render server-side HTML.

JavaScript is used only where it provides a clear usability benefit.

## Administration

Administration lives under:

    /admin

Primary administration areas include:

    /admin
    ├── dashboard
    ├── news
    ├── shows
    ├── releases
    ├── media
    ├── band
    ├── contact
    └── authentication

The administration interface is designed to remain practical to use from a
phone.

Common content updates can be performed through normal forms rather than
source-code editing.

## Data Models

### User

Used for administration authentication.

### News

Stores site updates and homepage news content.

### Show

Stores upcoming and historical performances.

Past shows can be determined automatically based on date.

### Release

Stores demos, EPs, albums, singles, compilations, tracklists, and related
metadata.

### Media

Stores photo metadata and YouTube video information.

### BandMember

Stores current and former band-member information.

### BandMemberActivity

Stores structured role-specific activity periods for band members.

Multiple activity periods can be associated with the same member and role.

### BandBiography

Stores short and long band descriptions and historical information.

### SiteSettings

Stores shared configuration such as:

- Contact email
- Booking email
- Press email
- Social links
- Default site metadata
- Featured homepage content

## Media Handling

The application includes a reusable image-upload service for CMS-managed
images.

The upload pipeline:

1. Receives the uploaded file through a multipart form.
2. Decodes the image with Pillow rather than trusting the filename extension.
3. Accepts supported JPEG, PNG, and WebP images.
4. Enforces the configured request-size limit.
5. Resizes oversized images while preserving aspect ratio.
6. Re-encodes the processed image as WebP.
7. Generates a random filename rather than using the client-provided filename.
8. Stores the resulting image under the application's static upload directory.

Runtime uploads are intentionally excluded from Git.

The upload service can be extended to additional CMS-managed image types.

Possible future media improvements include:

- Mobile and desktop image variants
- AVIF where appropriate
- Alternative text management
- Image focal-point selection

## Video

Video content can be hosted externally on YouTube.

YouTube players are not loaded immediately with the page.

Preferred approach:

1. Display a lightweight thumbnail.
2. User selects the video.
3. Load the YouTube player on demand.

This reduces unnecessary third-party JavaScript and improves mobile
performance.

## Database

The default development database is SQLite.

The application uses SQLAlchemy and Flask-Migrate for database access and
schema migrations.

The architecture allows another SQLAlchemy-supported database engine, such as
PostgreSQL, to be used when appropriate.

## Configuration

Application configuration is environment-specific.

Secrets must not be stored in Git.

Important production configuration includes:

- `SECRET_KEY`
- `DATABASE_URL`
- `RATELIMIT_STORAGE_URI`
- `TRUSTED_HOSTS`
- Database credentials
- External service credentials, if added

Production startup validates required security-sensitive configuration and
fails rather than silently starting with unsafe defaults.

Local secrets belong in environment variables or ignored local configuration.

## Development and Deployment

A typical workflow is:

    Development workstation
            |
            | git push
            v
       Git repository
            |
            | git pull / deployment
            v
     Deployment host

A typical production request path is:

    Dynamic requests:
    Browser -> Nginx -> Gunicorn -> Flask

    Static assets:
    Browser -> Nginx -> static files

Nginx terminates HTTPS and can serve `/static/` directly. Gunicorn should
listen only on a loopback or otherwise appropriately protected interface.

The application is not tied to a specific hosting provider or hardware
platform.

Example Nginx and systemd configurations are provided under `deploy/`.

Detailed environment and deployment requirements are documented in
[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Security Principles

The application follows these security principles:

- Strong password hashing
- Authentication
- Authorization
- Secure sessions
- CSRF protection
- Login rate limiting
- Persistent/shared rate-limit storage in production
- Secure cookie configuration
- Trusted host validation
- Upload MIME/type validation
- Upload size limits
- Generated safe filenames
- Image decoding and re-encoding
- Security-relevant audit logging
- Reverse-proxy awareness
- HTTPS in production
- Secrets kept outside Git

Debug mode must never be enabled in production.
