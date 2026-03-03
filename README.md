# GymTracker

Django web app for tracking gym workouts and exercises. Built for DSCC coursework.

## Setup

```bash
git clone https://github.com/BexTuychiev/dscc-coursework.git
cd dscc-coursework
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Docker

```bash
cp .env.example .env
docker compose up -d --build
```

## Running tests

```bash
pytest -v
```

## Features

- User registration and login
- Create/edit/delete workouts with exercises
- Track sets, reps and weight
- Exercise library by muscle group
- Admin panel
