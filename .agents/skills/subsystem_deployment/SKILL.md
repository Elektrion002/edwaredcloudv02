---
name: Subsystem Deployment & Infrastructure
description: Mandatory technical guidelines for deploying isolated microservices and subsystems in the EdwaredCloud VPS environment.
---

# Subsystem Deployment & Infrastructure Skill

This skill ensures the technical integrity, isolation, and stability of the EdwaredCloud ecosystem when adding new subsystems or microservices.

## 1. Package Identity & Namespace

To prevent Python import conflicts between the Master system and Subsystems:

- **Unique Naming:** Never use generic folder names like `app/` for a subsystem's core package.
- **Descriptive Prefixes:** Use unique names such as `recompensas_app`, `catalogos_app`, etc.
- **Run Script:** The `run.py` entry point must import the specific app object from its unique package name.

## 2. Network & Routing Standards

Every subsystem must be resilient to its subpath environment:

- **ProxyFix Middleware:** ALWAYS initialize Werkzeug's `ProxyFix` in the Flask factory:
  ```python
  from werkzeug.middleware.proxy_fix import ProxyFix
  app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
  ```
- **Nginx Headers:** Ensure the `X-Forwarded-Prefix` header is set to the subsystem's subpath (e.g., `/rpandemo01`).
- **DB Port Policy:** Standardize PostgreSQL connection string to port `5432` unless a specific isolated instance is required. Verify connectivity with `pg_isready`.

## 3. High-Integrity Deployment Workflow

Avoid shell-related configuration corruption:

- **Local Prep:** Prepare all `.service` files and `nginx.conf` blocks locally.
- **SCP Transfer:** Transfer files to the VPS using `scp` only. NEVER use `cat <<EOF` via SSH for complex files with variable symbols (`$`).
- **Process Hygiene:** Use `pkill -f gunicorn` to clear orphan processes if a port is stuck before restarting services.

## 4. Security & UX Consistency

- **Credential Visibility:** Use "Eye Toggle" icons for PINs and Passwords in admin forms to avoid plain-text exposure while ensuring data entry accuracy.
- **Validation:** Implement robust server-side validation to prevent unhandled 500 errors from missing mandatory fields.
- **Branding:** Follow the `Executive Cinematic Branding` skill for all UI components to maintain a premium Navy & Gold look.

## 5S Compliance for Infrastructure

- **Seiton (Set in order):** Group subsystems in the `/var/www/edwared_cloud_v2/subsystems/` directory.
- **Seiketsu (Standardize):** Use the `Subsystem` model in the Master app to register all active routes dynamically.
