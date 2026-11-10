#!/bin/bash
cd "$(dirname "$0")/YOLOv5"
source venv/bin/activate
echo "=== YOLOv5 변경 없는 기본 상태 detect.py 실행 ==="
rm -rf runs/detect/exp_original
python detect_original_backup.py --weights yolov5s.pt --source data/images --project runs/detect --name exp_original 2>&1
echo
echo "완료! 아무 키나 누르면 창이 닫힙니다."
read -n 1
