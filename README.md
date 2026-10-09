# Healthcare Backend API

A RESTful API built with Django and Django REST Framework for managing patients, doctors, and patient-doctor mappings. Authenticated users can manage their own patient records, view and register doctors, and map doctors to their patients.

---

## Tech Stack

- **Framework:** Django 6.1, Django REST Framework 3.18
- **Authentication:** SimpleJWT (JSON Web Tokens)
- **Database:** PostgreSQL (with SQLite fallback/support)
- **Environment Management:** python-decouple

---

## Folder Structure

```
Backend/
├── config/              # Django project settings, URLs, custom exception handler
├── accounts/            # User registration & authentication APIs
├── patients/            # Patient management models, serializers, views, tests
├── doctors/             # Doctor management models, permissions, views, tests
├── mappings/            # Patient-Doctor mapping models, views, tests
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Environment Variables

Configure environment variables by creating a `.env` file from `.env.example`:

| Variable | Description | Example / Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | `change-me-to-a-long-random-string` |
| `DEBUG` | Debug mode boolean | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | PostgreSQL connection string (optional) | `postgresql://user:pass@localhost:5432/dbname` |
| `DB_NAME` | Database name | `healthcare_db` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |

---

## Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env if using custom database credentials
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

| Area | Method + Path | Auth Required | Description / Notes |
|---|---|---|---|
| Auth | `POST /api/auth/register/` | Public | Register new user (`name`, `email`, `password`) |
| Auth | `POST /api/auth/login/` | Public | Obtain JWT `access` & `refresh` tokens |
| Patients | `POST /api/patients/` | JWT | Create a new patient (`created_by` set automatically) |
| Patients | `GET /api/patients/` | JWT | List **only** patients created by authenticated user |
| Patients | `GET /api/patients/<id>/` | JWT | Retrieve patient details (404 if not owned by user) |
| Patients | `PUT /api/patients/<id>/` | JWT | Update patient details (404 if not owned by user) |
| Patients | `DELETE /api/patients/<id>/` | JWT | Delete patient record (404 if not owned by user) |
| Doctors | `POST /api/doctors/` | JWT | Register a new doctor |
| Doctors | `GET /api/doctors/` | JWT | List **all** registered doctors |
| Doctors | `GET /api/doctors/<id>/` | JWT | Retrieve doctor details |
| Doctors | `PUT /api/doctors/<id>/` | JWT | Update doctor details (creator only, 403 otherwise) |
| Doctors | `DELETE /api/doctors/<id>/` | JWT | Delete doctor record (creator only, 403 otherwise) |
| Mappings | `POST /api/mappings/` | JWT | Assign a doctor to a patient (patient must belong to user) |
| Mappings | `GET /api/mappings/` | JWT | List all mappings for patients owned by user |
| Mappings | `GET /api/mappings/<patient_id>/` | JWT | Retrieve all doctors assigned to a specific patient ID |
| Mappings | `DELETE /api/mappings/<id>/` | JWT | Unassign doctor by mapping ID |

### Note on Mapping Endpoints (`/api/mappings/<id>/`)

The route `/api/mappings/<id>/` handles two distinct behaviors depending on the HTTP method:
- `GET /api/mappings/<patient_id>/`: `<id>` is interpreted as a **Patient ID**. Returns patient details and a list of doctors assigned to that patient.
- `DELETE /api/mappings/<mapping_id>/`: `<id>` is interpreted as a **Mapping ID**. Deletes that specific mapping record.

---

## How to Run Tests

Execute the Django test suite across all applications:

```bash
python manage.py test
```

---

## Key Design Decisions

1. **JWT Authentication:** SimpleJWT provides statutory session-less authentication using Bearer tokens.
2. **Owner-Scoped Patient Isolation:** Patient endpoints return 404 for un-owned IDs to prevent user enumeration.
3. **Built-in User Model:** `django.contrib.auth.models.User` is used with `email` functioning as the unique username during registration/login.
4. **Cascade Deletions & Unique Constraint:** Deleting a patient or doctor cascades to their mapping records, and a `UniqueConstraint(patient, doctor)` prevents duplicate doctor assignments.
