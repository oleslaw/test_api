#!/bin/bash
celery -A api worker --loglevel=info --concurrency=1 --max-tasks-per-child=10 &
celery -A api beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler