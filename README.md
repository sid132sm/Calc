# Calculator

Production-oriented calculator application scaffold using React, Django REST Framework, and PostgreSQL. Calculator behavior has intentionally not been implemented yet.

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 16+

## Backend setup

1. Copy the environment template: `cp .env.example .env`.
2. Create the PostgreSQL database and role using the values in `.env`.
3. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies and apply migrations:

   ```bash
   pip install -r requirements.txt
   cd backend
   python manage.py migrate
   ```

5. Run the API server:

   ```bash
   python manage.py runserver
   ```

The development API is available at `http://localhost:8000/`. API endpoints will be added under `/api/v1/` with calculator functionality.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Vite serves the application at `http://localhost:5173/` by default.

## Layout

- `backend/config`: Django configuration and environment-specific settings.
- `backend/calculator`: the calculator domain app, API, services, migrations, and tests.
- `frontend/src/features`: future feature-specific React code.
- `frontend/src/components`: reusable UI components.
- `frontend/src/styles`: CSS tokens, reset, and layout layers.

## Environment variables

See `.env.example`. Keep `.env` out of version control and replace the sample Django secret before any non-local deployment.
