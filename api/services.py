import random
import redis
from dezhban import settings


otp_redis = redis.Redis(
    host='localhost',
    port=6379,
    db=2,
    decode_responses=True
)


class OTPManager:
    
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def generate_save(self):
        self._otp = random.randint(10999, 987654)
        otp_redis.set(name=self.phone_number, value=self._otp, ex=180)

    def send(self):
        send_sms(phone_number=self.phone_number, otp=self.value)

    @property
    def value(self):
        return otp_redis.get(self.phone_number)

    def is_valid(self, otp):
        if otp_redis.get(self.phone_number) == otp:
            otp_redis.delete(self.phone_number)
            return True
        return False


def send_sms(phone_number, otp):

    url = "https://api.sms.ir/v1/send/verify/"
    json = {
    "mobile": phone_number,
    "templateId": 100000,
    "parameters": [
        {
        "name": "Code",
        "value": otp
        }
    ]
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/plain",
        "x-api-key": settings.SMS_IR_TOKEN
    }


    r = requests.post(url, json=json, headers=headers)
    return r.status_code
