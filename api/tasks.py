from celery import Celery
from api.services import OTPManager

app = Celery('tasks', broker='redis://localhost:6379')


@app.task(bind=True, queue='otp')
def send_otp_task(self, phone_number):
    otp_manager = OTPManager(phone_number)
    otp_manager.generate_save()
    print(f"============= sending OTP to '{phone_number}'===============")
    try:
        otp_manager.send()
        print(f"================ OTP sent to {phone_number}. =================")
    except Exception as exc:
        self.retry(exc=exc)
