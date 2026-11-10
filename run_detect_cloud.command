#!/bin/bash
cd "$(dirname "$0")/YOLOv5"
source venv/bin/activate
echo "=== YOLOv5 -> PythonAnywhere 클라우드 전송 테스트 ==="
export PHOTOBLOG_HOST="https://junghwan.pythonanywhere.com"
python detect.py --weights yolov5s.pt --source data/images --project runs/detect --name exp_cloud
echo ""
echo "완료! 아무 키나 누르면 창이 닫힙니다."
read -n 1
