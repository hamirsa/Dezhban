from rest_framework.throttling import BaseThrottle
from api.services import OTPManager


class SendOTPThrottle(BaseThrottle):
    """
    Check if an sms have been sent to this phone number in last 60 seconds.

    hint: you can change the waiting time usin this formula:
        otp expity time - time limit

        example:
            180(set in api/services.py) - 60(we put it 60, here.) = 120
        *you can change this numbers base on your usecase. :)
    """
    
    def allow_request(self, request, view):
        self.otp_manager = OTPManager(request.data['phone_number'])
        return self.otp_manager.ttl() <= 120

    def wait(self):
        return self.otp_manager.ttl() - 120
        