# Stage 1: Build dependencies
FROM python:3.12-alpine AS builder

RUN apk add --no-cache gcc musl-dev postgresql-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache libpq

RUN addgroup -S app && adduser -S app -G app

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

RUN python manage.py collectstatic --noinput

RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["gunicorn", "gymtracker.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
