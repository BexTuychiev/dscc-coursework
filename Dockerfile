# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir pip --upgrade

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system app && adduser --system --group app

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

RUN python manage.py collectstatic --noinput

RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["gunicorn", "gymtracker.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
