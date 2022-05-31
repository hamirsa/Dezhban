from rest_framework import serializers
import re

class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        """
        Check that phone_number is an valid Iranian number.
        """

        phone_number_pattern = '^09(1[0-9]|2[0-2]|3[0-9]|9[0-9])[0-9]{7}$'
        if not re.match(pattern=phone_number_pattern, string=value):
            raise serializers.ValidationError('phone_number must be like 09123456789 & exactly 11 digits.')
        return value


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    otp = serializers.CharField(max_length=6)

    def validate_phone_number(self, value):
        """
        Check that phone_number is an valid Iranian number.
        """

        phone_number_pattern = '^09(1[0-9]|2[0-2]|3[0-9]|9[0-9])[0-9]{7}$'
        if not re.match(pattern=phone_number_pattern, string=value):
            raise serializers.ValidationError('phone_number must be like 09123456789 & exactly 11 digits.')
        return value

    def validate_otp(self, value):
        """
        Check that otp is match with otp_pattern.
        """

        otp_pattern = '^[1-9][0-9]{5}$'
        if not re.match(pattern=otp_pattern, string=value):
            raise serializers.ValidationError('otp must contains exactly 6 digits & can not start with 0.')
        return value
