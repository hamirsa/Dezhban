from rest_framework import serializers
import re

class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):

        pattern = '^09(1[0-9]|2[0-2]|3[0-9]|9[0-9])[0-9]{7}$'
        if not re.match(pattern=pattern, string=value):
            raise serializers.ValidationError('phone_number must be like 09123456789 & exactly 11 digits.')
        return value
