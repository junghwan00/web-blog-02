#!/bin/bash
cd "$(dirname "$0")/YOLOv5"
source venv/bin/activate
echo "=== YOLOv5 기본 상태 detect.py 실행 (변경 전) ==="
python detect.py --weights yolov5s.pt --source data/images --project runs/detect --name exp_default_gui --view-img 2>&1
echo
echo "완료! 아무 키나 누르면 창이 닫힙니다."
read -n 1
