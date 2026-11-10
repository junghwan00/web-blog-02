#!/bin/bash
cd "$(dirname "$0")/YOLOv5"
source venv/bin/activate
echo "=== 검출기 코드 수정 버전 detect.py 실행 (블로그 서버로 전송) ==="
python detect.py --weights yolov5s.pt --source data/images --project runs/detect --name exp_send_gui 2>&1
echo
echo "완료! 아무 키나 누르면 창이 닫힙니다."
read -n 1
