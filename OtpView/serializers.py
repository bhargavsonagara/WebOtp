from rest_framework import serializers
from .utils import *
from .models import *
import phonenumbers


class SendOtpListSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    otp = serializers.IntegerField(required=False)
    created_at = serializers.CharField(required=False)


class OtpListSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    username = serializers.EmailField(required=False)
    email = serializers.EmailField(required=False)
    mobile_number = serializers.IntegerField()
    send_otps = SendOtpListSerializer(many=True)


class OtpListResponseSerializer(serializers.Serializer):
    responseCode = serializers.IntegerField()
    responseMessage = serializers.CharField()
    responseData = OtpListSerializer(many=True)


class OtpSendResponseSerializer(serializers.Serializer):
    responseCode = serializers.IntegerField()
    responseMessage = serializers.CharField()


class OtpSendSerializer(serializers.Serializer):
    email = serializers.EmailField()
    mobile_number = serializers.IntegerField()
    isd_code = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super(OtpSendSerializer, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['blank'] = u'Email cannot be blank!'
        self.fields['email'].error_messages['required'] = u'The email field is required'

    def validate(self, attrs):
        strmobileNumber = attrs.get('isd_code') + \
            str(attrs.get('mobile_number'))
        my_number = phonenumbers.parse(strmobileNumber)

        if not phonenumbers.is_valid_number(my_number):
            raise serializers.ValidationError(
                "Please enter a valid mobile number.")

        if(not Otp.objects.filter(email=attrs.get('email')).exists()):
            raise serializers.ValidationError("Email does not exists.")
        return attrs
