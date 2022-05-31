from rest_framework import views
from api.serializers import SendOTPSerializer, VerifyOTPSerializer
from api.tasks import send_otp_task
from api.models import CustomUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken



class SendOTPAPIView(views.APIView):

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        send_otp_task.delay(phone_number=data['phone_number'])
        return Response(status=status.HTTP_200_OK)


class VerifyOTPView(views.APIView):

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

            refresh = RefreshToken.for_user(user)

            return Response(ObtainTokenSerializer({
                'access': str(refresh.access_token),    
                'refresh': str(refresh)

            }).data)

        return Response(data={"Failed": "Wrong phone number or OTP"}, status=status.HTTP_403_FORBIDDEN)
