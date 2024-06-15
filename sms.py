import base64
import hashlib
import hmac
import requests
import time
import uuid

from .constants import SMS_API_URL, SMS_SECRET, SMS_USER


def get_cleaned_phone_number(number):
    number = number[1:] if number[0] == '+' else number
    print(number)
    return number


def generate_hmac(key, message):
    key = base64.b64decode(key)
    msg = message.encode('utf-8')
    h = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.b64encode(h)


class SMS:
    def __init__(self, text, dest):
        self.text = text
        self.dest = dest

    @staticmethod
    def _send_message(user, msg_id, dest, text, secret):
        ts = int(time.time())
        msg = f'{user}:{msg_id}:{dest}:{text}:{ts}'
        req_hmac = generate_hmac(secret, msg)
        return requests.post(SMS_API_URL + user + '/send', data={
            'msg-id': msg_id,
            'dest': dest,
            'text': text,
            'ts': ts,
            'hmac': req_hmac
        })

    def send(self):
        dest = get_cleaned_phone_number(self.dest)
        rv = self._send_message(user=SMS_USER, msg_id=uuid.uuid4(), dest=dest, text=self.text, secret=SMS_SECRET)
        return {"status_code": rv.status_code, "content": rv.content}
