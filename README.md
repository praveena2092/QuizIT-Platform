# Quiz Master V2

A multi-user quiz and exam-preparation web app with two roles, **Admin** and **User**.
Admins organise content as Subject → Chapter → Quiz → Question; users take quizzes
and track their performance. Built as the **MAD-II** project for the IIT Madras BS Degree program.

## Features

- **Role-based access** – token authentication with Flask-Security (admin / user)
- **Content hierarchy** – Subjects, Chapters, Quizzes and Questions with full CRUD
- **Quiz attempts** – timed quizzes, scoring, and a history of past scores per user
- **Charts** – summary dashboards with Chart.js
- **Background jobs** – Celery + Redis for CSV exports, daily reminders and monthly reports
- **Email** – HTML report emails (tested locally with MailHog)
- **Caching** – Redis via Flask-Caching

## Tech stack

| Layer | Tools |
|-------|-------|
| Backend | Flask, Flask-RESTful, Flask-Security, Flask-SQLAlchemy, Flask-CORS |
| Database | SQLite |
| Jobs / cache | Celery, Redis |
| Frontend | Vue 3, Vue Router, Vite, Bootstrap 5, Chart.js |

## Project structure

```
.
├── backend/
│   ├── app.py              # App factory, seed data, Celery schedule
│   ├── api/                # REST resources and routes
│   ├── application/        # models, config, tasks, mail, Celery setup
│   ├── templates/          # Email templates
│   └── static/             # Generated CSV exports (git-ignored)
├── frontend/               # Vue 3 + Vite single-page app
├── docs/project-report.pdf # Project report
└── dev.sh                  # tmux helper that starts everything
```

## Prerequisites

Python 3.10+, Node.js 18+, Redis, and [MailHog](https://github.com/mailhog/MailHog) (optional, for emails).

## Getting started

**1. Backend**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                    # http://127.0.0.1:5000
```

**2. Frontend**
```bash
cd frontend
npm install
npm run dev                      # http://localhost:5173
```

**3. Background services** (optional, needed for exports, reminders and emails)
```bash
redis-server                                            # or: sudo systemctl start redis
MailHog                                                 # inbox at http://localhost:8025
cd backend && celery -A app.celery worker --loglevel INFO
cd backend && celery -A app.celery beat --loglevel INFO
```

On Linux/macOS with tmux installed, `./dev.sh` starts all of the above in one session.

## Demo accounts

Seeded automatically on first run (development only):

| Role | Email | Password |
|------|-------|----------|
| Admin | `user@admin.com` | `1234` |
| User | `user@user.com` | `1234` |

## API overview

| Entity | Endpoints |
|--------|-----------|
| Subject | `GET /api/subject/get`, `POST /api/subject/create`, `PUT /api/subject/update/<id>`, `DELETE /api/subject/delete/<id>` |
| Chapter | `/api/chapter/{get,create,update,delete}/<id>` |
| Quiz | `/api/quiz/{get,create,update,delete}/<id>` |
| Question | `/api/question/{get,create,update,delete}/<id>` |
| Score | `/api/score/{get,create,update,delete}` |
| Auth & misc | `/api/login`, `/api/register`, `/api/export`, `/api/quiz/start`, `/api/quiz/<id>/submit`, … (see `backend/api/routes.py`) |

## Known limitations

- The Flask secret key and salt in `backend/application/config.py` are development values; use environment variables in production.
- The frontend calls the API at `http://127.0.0.1:5000` directly; there is no environment-based API URL yet.
- Only a development configuration exists.

## Author

Praveena N (22f3001454) – IIT Madras BS Degree

## License

[MIT](LICENSE)
