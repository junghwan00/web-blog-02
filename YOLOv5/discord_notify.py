import os
import json
import requests

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'discord_webhook.txt')


def _get_webhook_url():
    """환경변수 DISCORD_WEBHOOK_URL 또는 discord_webhook.txt(gitignore됨)에서 웹훅 URL을 읽어온다."""
    env_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if env_url:
        return env_url.strip()
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            url = f.read().strip()
            if url:
                return url
    return None


def send_discord_alert(title, text, image_path):
    """
    공통평가 02 - 편의기능#1: 실시간 알림
    감지된 객체 정보 + 이미지를 Discord 채널(웹훅)로 전송한다.
    웹훅 URL이 설정되지 않은 경우 조용히 건너뛴다 (메인 감지/전송 흐름을 막지 않음).
    """
    webhook_url = _get_webhook_url()
    if not webhook_url:
        print('DiscordNotify: 웹훅 URL이 설정되지 않아 알림을 건너뜁니다. '
              '(YOLOv5/discord_webhook.txt 에 웹훅 URL을 한 줄 넣으면 활성화됩니다)')
        return

    payload = {
        'content': '🚨 **침입자 감시 시스템 알림**',
        'embeds': [{
            'title': '감지된 객체: {0}'.format(title),
            'description': text,
            'color': 15158332,
        }],
    }

    try:
        with open(image_path, 'rb') as f:
            files = {
                'file': (os.path.basename(str(image_path)), f, 'image/jpeg'),
                'payload_json': (None, json.dumps(payload)),
            }
            res = requests.post(webhook_url, files=files, timeout=5)
        print('DiscordNotify: 전송 결과', res.status_code)
    except Exception as e:
        print('DiscordNotify: 전송 실패 -', e)
