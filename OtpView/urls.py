from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contactdetail/', contactdetails, name='contactdetail'),
    path('showlist/', showlist, name='showlist'),
    path('contactdetail/<str:id>/', contactdetails, name='contactdetail'),
    path('sendmessage/<str:id>/', sendmessage, name='sendmessage'),
    path('send/', send, name='send'),
    path('listOtp', OtpListView.as_view(), name="listotp"),
    path('otpsend', OtpSendView.as_view(), name="otpsend"),
]
