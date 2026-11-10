#!/bin/bash
cd "$(dirname "$0")/PhotoBlogServer"
source venv/bin/activate
echo "=== Django 서버 실행 (공통평가02) ==="
python manage.py runserver 127.0.0.1:8000
