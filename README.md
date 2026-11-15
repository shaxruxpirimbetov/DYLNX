<div align="center">

# DYLNX

**Quiet backends, fast when it counts.**

Official website and API of the DYLNX engineering team — Nukus, Karakalpakstan.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django-REST%20Framework-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?logo=postgresql&logoColor=white)
![Cloudflare R2](https://img.shields.io/badge/Cloudflare-R2-F38020?logo=cloudflare&logoColor=white)
![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?logo=vercel&logoColor=white)

**Live API:** <https://dylnx-indol.vercel.app>

</div>

---

## Overview

This repository contains the full source of the DYLNX company website:

- a **Django REST Framework backend** that serves the portfolio, the team, the contact form and the newsletter list;
- a **single-page frontend** (`templates/index.html`, no build step) in a lynx-inspired dark theme, with a built-in **admin panel** for managing content without touching the Django admin.

The backend is deployed in production; the page is rendered by Django at `/` and talks to the API over `fetch`.

## Features

**Public site**
- Sections: **Studio**, **Services**, **Work**, **Team**, **Contact**.
- **Portfolio** loaded from the API with pagination and image galleries per project.
- **Team** cards built from users with the `EMPLOYEE` role, with a built-in fallback if the API is unreachable.
- **Contact form** and **email subscription**, both writing to the API.
- **Four languages:** English, Russian, Uzbek and Karakalpak, with automatic detection from the browser.
- Respects `prefers-reduced-motion`.

**Admin panel** (inside the same page, JWT sign-in)
- Create, edit, hide and delete **projects**, including logo and gallery upload.
- Read incoming **messages** and **subscriptions**.
- Create, edit and delete **users** and team members (avatar, stack, role).

**Backend**
- JWT authentication (access 5 h, refresh 1 day).
- Role-based users: `USER`, `EMPLOYEE`, `ADMIN`.
- Image uploads stored in **Cloudflare R2** and served from a public URL.
- Per-IP rate limiting: 10 requests/min anonymous, 100 requests/min authenticated.
- Strict CORS in production, `X-Frame-Options: DENY`, `nosniff`.

## Repository layout

```
.
├── DYLNX/                  Django project (settings, urls, wsgi/asgi)
├── apps/
│   ├── user/               Custom user (role, avatar, stack), team endpoint
│   ├── project/            Portfolio projects and their images
│   ├── message/            Contact-form messages
│   └── subscription/       Newsletter e-mail list
├── templates/
│   ├── index.html          Current site + admin panel
│   ├── index_v2.html       Previous version
│   └── index_old.html      Legacy version
├── manage.py
└── requirements.txt
```

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Auth | `djangorestframework-simplejwt` |
| Database | PostgreSQL (Neon) via `DATABASE_URL` — `dj-database-url`, `psycopg` |
| File storage | Cloudflare R2 (S3-compatible) — `django-storages`, `boto3`, `Pillow` |
| CORS / config | `django-cors-headers`, `python-decouple` |
| Frontend | Plain HTML / CSS / JavaScript (single file, no build step) |

## Getting started

### Prerequisites

- Python 3.10+
- A PostgreSQL database (any URL supported by `dj-database-url`)
- A Cloudflare R2 bucket with a public URL — Django's default file storage is R2, so these variables are required even for local development

### Installation

```bash
git clone https://github.com/shaxruxpirimbetov/DYLNX.git
cd DYLNX

python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:3000        # required when DEBUG=False

# Database
DATABASE_URL=postgres://user:password@host:5432/dbname

# Cloudflare R2
CLOUDFLARE_ACCOUNT_ID=...
CLOUDFLARE_ACCESS_KEY_ID=...
CLOUDFLARE_SECRET_ACCESS_KEY=...
CLOUDFLARE_R2_BUCKET=...
CLOUDFLARE_R2_PUBLIC_URL=https://pub-xxxx.r2.dev
```

### Run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the site and sign in to the built-in admin panel with the superuser account. The classic Django admin is available at `/admin/`.

> **Note:** the frontend reads the API address from the `API_ORIGIN` constant at the top of the script in `templates/index.html`. It points to the production API by default — change it to `http://127.0.0.1:8000` to work against your local backend.

## API reference

Authenticate with `Authorization: Bearer <access_token>`. List endpoints are paginated (`?page=`, 20 items per page).

### Auth

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/token/` | Obtain access and refresh tokens (`username`, `password`) |
| `POST` | `/api/refresh/` | Refresh the access token (`refresh`) |

### Projects — `/api/project/`

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/project/` | public | List projects with their images |
| `POST` | `/api/project/` | admin | Create a project (`multipart/form-data`: `title`, `description`, `logo`, `link`, `is_active`, `images` × N) |
| `GET` | `/api/project/<id>/` | public | Retrieve a project |
| `PUT` / `PATCH` / `DELETE` | `/api/project/<id>/` | admin | Update or delete a project |

### Users — `/api/user/`

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/user/team/` | public | Public team list (users with role `EMPLOYEE`) |
| `GET` | `/api/user/me/` | authenticated | Current user |
| `GET` / `POST` | `/api/user/` | admin | List / create users |
| `GET` / `PUT` / `PATCH` / `DELETE` | `/api/user/<id>/` | the user themself or superuser | Manage a user |

### Messages — `/api/message/`

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/message/` | public | Send a contact message (`first_name`, `last_name`, `text`) |
| `GET` | `/api/message/` | see *Known limitations* | List messages |

### Subscriptions — `/api/subscription/`

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/subscription/` | public | Subscribe an e-mail address (unique) |
| `GET` | `/api/subscription/` | admin | List subscribers |

## Data model

| Model | Fields |
|---|---|
| **User** | Django `AbstractUser` + `role` (`USER` / `EMPLOYEE` / `ADMIN`), `avatar`, `stack` |
| **Project** | `title`, `description`, `logo`, `link`, `is_active`, timestamps |
| **ProjectImage** | `project` → Project, `image`, timestamp |
| **Message** | `first_name`, `last_name`, `text`, timestamps |
| **Subscription** | `email` (unique), timestamps |

## Known limitations

These are documented here so they are fixed before wider use:

- `GET /api/message/` has no access restriction, so contact-form submissions are readable by anyone. Restrict it to staff (`IsAdminUser` for `GET`, `AllowAny` for `POST`).
- `UpdateUserSerializer` lists the field `fist_name` (typo for `first_name`), which makes `PATCH /api/user/<id>/` fail until corrected.
- There are no detail routes for messages and subscriptions, so entries cannot be deleted through the API or the admin panel.
- The `apps/comment` app is a scaffold and is not enabled in `INSTALLED_APPS`.

## Deployment

The backend is deployed at <https://dylnx-indol.vercel.app>. For any deployment:

1. Set all environment variables from the configuration section.
2. Run `python manage.py migrate` on each release.
3. Set `DEBUG=False`, a strong `SECRET_KEY`, and `CORS_ALLOWED_ORIGINS` to the exact origins that call the API.

## About

DYLNX is a four-person engineering team based in Nukus, Karakalpakstan, Uzbekistan, working on backend systems, software and hardware.