from django.shortcuts import render, redirect
import random
import os
from twilio.rest import Client
from .models import *
from .utils import *
import requests
import json
from twilio.base.exceptions import TwilioRestException
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.types import OpenApiTypes
from .serializers import *
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.parsers import FormParser, MultiPartParser

############ API  #############

headerAuthParam = [OpenApiParameter(
    name='Authorizations',
    type=OpenApiTypes.STR,
    location=OpenApiParameter.HEADER,
    description='Authorization',
    required=True,
    default='Bearer ',)]

headerParam = [
    OpenApiParameter(
        name='Accept-Language', location=OpenApiParameter.HEADER,
        type=OpenApiTypes.STR,
        description='ISO 2 Letter Language Code',
        required=True,
        enum=['en'],
        default='en',
    ),
    OpenApiParameter(
        name='Accept', location=OpenApiParameter.HEADER,
        type=OpenApiTypes.STR,
        description='Type of response you are expecting from API. i.e. (application/json)',
        required=True,
        default='application/json',
    ),
]


class OtpListView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OtpListSerializer

    @extend_schema(
        parameters=headerParam,
        tags=['Otp'],
        responses={200: OtpListResponseSerializer},
        summary='Listing for Contact'
    )
    def get(self, request):
        try:
            otpTypeLista = []
            listOtp = Otp.objects.all()
            for row in listOtp:
                sendOtpTypeLista = []
                for col in SendMessages.objects.filter(otp_id=row):
                    sendOtpTypeLista.append({
                        'id': col.id,
                        'otp': col.otp,
                        'created_at': col.created_at
                    })
                otpTypeLista.append({
                    'id': row.id,
                    'username': row.username,
                    'email': row.email,
                    'mobile_number': row.mobile_number,
                    'send_otps': sendOtpTypeLista
                })
            return send_response(request, code=200, message=_("Success"), data=otpTypeLista)
        except Exception as e:
            return send_response_validation(request, code=404, message=str(e))


class OtpSendView(generics.GenericAPIView):
    serializer_class = OtpSendSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, )

    @extend_schema(
        parameters=headerParam,
        tags=['Otp'],
        responses={200: OtpSendResponseSerializer},
        summary='Send Otp'
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                email = data['email']
                random_otp = random.randint(11111, 99999)
                mobile_number = data['isd_code'] + str(data['mobile_number'])
                message_to_broadcast = (f"Hi. Your OTP is. {random_otp}")
                client = Client(os.getenv("TWILIO_ACCOUNT_SID",),
                                os.getenv("TWILIO_AUTH_TOKEN",))
                client.messages.create(to=mobile_number, from_=os.getenv(
                    "TWILIO_NUMBER",), body=message_to_broadcast)
                
                otp = Otp.objects.get(email=email)
                SendMessages.objects.create(otp_id=otp, otp=random_otp, created_at = int(time.time()))
                return success_200(request, code=200, message="Otp send successfully.")
            else:
                return error_400(request, code=400, message=list(serializer.errors.values())[0][0])
        except Exception as e:
            if(str(e) == "(0) Missing or invalid default region."):
                return send_response_validation(request, code=404, message="Country code not valid.")
            return send_response_validation(request, code=404, message=str(e))


######### Web Portal ##########

def home(request):
    url = os.getenv('SWAGGER_SERVER') + 'listOtp'
    response = requests.get(url).json()
    try:
        response = json.dumps(response['responseData'])
    except KeyError:
        response = json.dumps(response['responseMessage'])

    context = {'data': response}
    return render(request, 'index.html', context=context)


def contactdetails(request, id=None):
    error = False
    if(id == 'undefined'):
        error = True
        messages.warning(request, 'Please select the content.')
    elif(not Otp.objects.filter(id=id).exists()):
        error = True
        messages.warning(request, "Selected content does not exists.")
    if(error):
        return redirect('home')
    otp = Otp.objects.get(id=id)
    name = otp.username
    mobilenumber = otp.mobile_number
    context = {'id': id, 'mobilenumber': mobilenumber, 'name': name}
    return render(request, 'contact-details.html', context=context)


def sendmessage(request, id):
    try:
        error = False
        if(not Otp.objects.filter(id=id).exists()):
            messages.warning(request, "User does not exists.")
        if(error):
            return redirect('contactdetail', id=id)
        otp = Otp.objects.get(id=id)
        random_otp = random.randint(11111, 99999)
        context = {'id': id, 'name': otp.username, 'random_otp': random_otp}
        return render(request, 'send-message.html', context=context)
    except:
        pass


def send(request):
    if request.method == "POST":
        try:
            otp_id = request.POST.get('user_id')
            random_otp = request.POST.get('random_otp')
            otp = Otp.objects.get(id=otp_id)
            message_to_broadcast = (f"Hi. Your OTP is. {random_otp}")
            client = Client(os.getenv("TWILIO_ACCOUNT_SID",),
                            os.getenv("TWILIO_AUTH_TOKEN",))
            client.messages.create(to=otp.mobile_number, from_=os.getenv(
                "TWILIO_NUMBER",), body=message_to_broadcast)
            SendMessages.objects.create(otp_id=otp, otp=random_otp, created_at = int(time.time()))
            messages.success(request, "Message sent successfuly.")
            return redirect('home')
        except TwilioRestException as e:
            messages.warning(request, "Unable to create record in twilio.")
            return redirect("sendmessage", id=otp_id)
    return redirect('home')

def showlist(request):
    sendmessagelist = SendMessages.objects.all()
    context = {'sendmessagelist': sendmessagelist}
    return render(request, 'send-message-list.html', context=context)

def handler404(request, exception):
    return render(request, '404-found.html', status=404)

def handler500(request):
    return render(request, '500-internal.html', status=500)