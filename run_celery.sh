#!/bin/bash
celery -A api worker --loglevel=info &
celery -A api beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler