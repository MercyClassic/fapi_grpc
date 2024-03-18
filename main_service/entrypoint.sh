#!/bin/bash
cd /app
alembic upgrade head
cd /app/src
gunicorn --bind=0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker app.main.main:app
