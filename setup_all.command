#!/bin/bash
set -e
cd "$(dirname "$0")"
echo "=== [1/4] PhotoBlogServer venv 생성 ==="
cd PhotoBlogServer
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -q --upgrade pip
pip install -q "Django>=5.1,<5.3" djangorestframework pillow sqlparse asgiref
echo "=== [2/4] DB 마이그레이션 + admin 계정 생성 ==="
python manage.py migrate --noinput
DJANGO_SUPERUSER_PASSWORD=123456 python manage.py createsuperuser --noinput --username admin --email admin@example.com || echo "(admin 계정 이미 있음, 무시)"
deactivate
cd ..

echo "=== [3/4] YOLOv5 venv 생성 ==="
cd YOLOv5
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -q --upgrade pip
echo "=== [4/4] torch/torchvision 설치 (시간 좀 걸림, 기다려줘) ==="
pip install -q torch torchvision
pip install -q -r requirements.txt
deactivate
cd ..

echo
echo "✅ 전부 설치 완료! 이제 run_server.command 부터 실행하면 돼."
echo "아무 키나 누르면 창이 닫힙니다."
read -n 1
