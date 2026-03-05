# Agent Rules for EdwaredCloud Project

## 1. Modular Architecture (Blueprints)

- Every new feature or subsystem MUST be a separate Flask Blueprint.
- Keep `__init__.py`, `routes.py`, and `models.py` separate within the blueprint folder.

## 2. Branding (Executive Cinematic)

- All UI components MUST follow the tokens defined in `variables.css`.
- Use the **Montserrat** font for all headings.
- Maintain the **Navy and Gold** color palette at all times.
- Icons should be minimal and consistent.

## 3. Methodology (5S)

- **Seiri:** Remove any unused code or temporary files.
- **Seiton:** Maintain a clean directory structure. Externalize CSS and JS.
- **Seiso:** Use clear, descriptive names for variables and functions.
- **Seiketsu:** Document complex logic and follow the establish patterns.
- **Shitsuke:** Verify every commit against these rules.

## 4. Environment & Security

- Never hardcode sensitive data; use `.env` files.
- **CRITICAL:** Use of the virtual environment (`venv`) is mandatory for all development and execution steps.
- **SYNC:** All changes MUST be synchronized with GitHub (`git push`) once local testing and verification are successful.
- All database operations should be modular and audit-accessible via the established tunnel.

## 5. Responsiveness

- All UI MUST be mobile-first and responsive.
- Test every new page on simulated mobile views.
