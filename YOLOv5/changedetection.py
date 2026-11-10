import os
import cv2
import pathlib
import requests
from datetime import datetime
import discord_notify


class ChangeDetection:
    """
    YOLOv5 검출 결과 중 '새로 나타난(0->1) 객체'만 골라
    PhotoBlogServer(Django REST API)에 자동으로 게시글(사진)을 등록한다.
    (Ch08. Django와 YOLO를 이용한 침입자 감시 시스템 실습 기반, 서버 인증 방식(TokenAuthentication)에 맞춰 조정)
    """

    result_prev = []
    HOST = os.environ.get('PHOTOBLOG_HOST', 'http://127.0.0.1:8000')  # 로컬 기본값, 클라우드 테스트 시 run_detect_cloud.command가 덮어씀
    username = 'admin'
    password = '123456'
    token = ''
    title = ''
    text = ''

    def __init__(self, names):
        self.result_prev = [0 for i in range(len(names))]

        res = requests.post(self.HOST + '/api-token-auth/', {
            'username': self.username,
            'password': self.password,
        })
        res.raise_for_status()
        self.token = res.json()['token']  # 토큰 저장
        print('ChangeDetection: 로그인 성공, token =', self.token)

    def add(self, names, detected_current, save_dir, image):
        self.title = ''
        self.text = ''
        change_flag = 0  # 변화 감지 플래그
        i = 0
        while i < len(self.result_prev):
            if self.result_prev[i] == 0 and detected_current[i] == 1:
                change_flag = 1
                self.title = names[i]
                self.text += names[i] + ', '
            i += 1

        self.result_prev = detected_current[:]  # 객체 검출 상태 저장

        if change_flag == 1:
            self.send(save_dir, image)

    def send(self, save_dir, image):
        now = datetime.now()
        now_iso = now.isoformat()

        today = datetime.now()
        save_path = pathlib.Path(os.getcwd()) / pathlib.Path(save_dir) / 'detected' / str(today.year) / str(today.month) / str(today.day)
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

        full_path = save_path / '{0}-{1}-{2}-{3}.jpg'.format(today.hour, today.minute, today.second, today.microsecond)

        dst = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(full_path), dst)

        # 인증이 필요한 요청에 아래의 headers를 붙임 (TokenAuthentication: "Token <key>")
        headers = {'Authorization': 'Token ' + self.token}

        # Post Create
        data = {
            'title': self.title,
            'text': self.text,
        }
        with open(full_path, 'rb') as f:
            files = {'image': f}
            res = requests.post(self.HOST + '/api_root/Post/', data=data, files=files, headers=headers)
        print('ChangeDetection: 서버 전송 결과', res.status_code, res.text[:200])

        # 공통평가 02 - 편의기능#1: 서버 전송 성공 시 Discord로도 실시간 알림
        if res.status_code == 201:
            discord_notify.send_discord_alert(self.title, self.text, full_path)
