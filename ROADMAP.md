# Roadmap

Flask Band Website CMS is based on a working real-world application.

The public repository is a sanitized and generalized source snapshot rather
than a historical record of the original website's development. This roadmap
therefore focuses only on possible future improvements that are relevant to
the reusable public project.

## Current Functionality

The current application includes:

- Public mobile-first band website
- Administration interface
- News management
- Show management and past-show archive
- Discography and tracklists
- Band-member profiles
- Structured member activity history
- Band biography
- Media gallery
- YouTube video integration
- Merchandise catalog
- CMS-managed image uploads
- Contact and social-link management
- Featured homepage content
- Authentication and authorization
- CSRF protection
- Login rate limiting
- Production configuration validation
- Security response headers
- Content Security Policy
- Database migrations
- Nginx and systemd deployment examples

## Possible Improvements

### Media

- [ ] Add editable alternative text for CMS-managed images
- [ ] Add image focal-point selection
- [ ] Generate dedicated responsive image variants
- [ ] Evaluate AVIF output where appropriate
- [ ] Extend reusable image handling where useful

### Band Profiles

- [ ] Add optional external links to member profiles
- [ ] Improve management of complex historical membership data

### Merchandise

- [ ] Improve shipping and postage workflow
- [ ] Evaluate optional ecommerce integration
- [ ] Improve inventory management for larger catalogs

### Administration

- [ ] Expand security-relevant audit logging
- [ ] Improve content preview workflows
- [ ] Add additional administrative usability improvements

### Testing

- [ ] Add automated application tests
- [ ] Add route and permission tests
- [ ] Add upload-pipeline tests
- [ ] Add production-configuration validation tests
- [ ] Add CI for linting and automated tests

### Deployment

- [ ] Expand deployment examples
- [ ] Add containerized deployment example if useful
- [ ] Document additional database backends
- [ ] Add generic backup and restore guidance without environment-specific data

## Project Principles

Future development should preserve the project's core goals:

- Keep the public site lightweight.
- Prefer server-rendered HTML where practical.
- Avoid unnecessary frontend dependencies.
- Keep content management usable on mobile devices.
- Treat security as part of the application architecture.
- Keep secrets and runtime data outside version control.
- Keep deployment examples generic and portable.
