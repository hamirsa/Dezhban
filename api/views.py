from rest_framework import views, permissions, throttling
from api.serializers import SendOTPSerializer, VerifyOTPSerializer
from api.tasks import send_otp_task
from api.models import CustomUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.throttling import SendOTPThrottle


class SendOTPAPIView(views.APIView):
    """
    Clients can use this APIView to receive an OTP for login/register.
    """

    throttle_classes = (throttling.ScopedRateThrottle, SendOTPThrottle)
    throttle_scope = 'send-otp'

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        send_otp_task.delay(phone_number=data['phone_number'])
        return Response(status=status.HTTP_200_OK)


class VerifyOTPAPIView(views.APIView):
    """
    No matter clients are going to login or register, they can call this api
    to verify their OTPs and receive access & refresh token for further uses.
    """

    throttle_scope = 'verify-otp'

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        otp_manager = OTPManager(phone_number=data['phone_number'])

        if otp_manager.is_valid(otp=data['otp']):
            try:
                user = CustomUser.objects.get(phone_number=data['phone_number'])
            except CustomUser.DoesNotExist:
                user = CustomUser.objects.create(phone_number=data['phone_number'])
            
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response(ObtainTokenSerializer({
                    'access': str(refresh.access_token),    
                    'refresh': str(refresh)

                }).data)
            return Response(data={"detail": "User is deactivated."}, status=status.HTTP_403_FORBIDDEN)

        return Response(data={"detail": "Wrong phone number or OTP"}, status=status.HTTP_403_FORBIDDEN)


class TestPageAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        return Response(data={"detail": "you can see this, so you've done great so far :)"})