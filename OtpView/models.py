from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid, time
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^[6-9]\d{9}$')
ten_digit = '''-> Phone number should be of 10 digits <br/> 
-> Phone number must starts with either 9, 8, 7 or 6 <br/>
-> Should enter in this format: 9999955555'''

# Create your models here.
class Otp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True, db_index=True,)
    mobile_number = models.CharField(max_length=255, unique=True, validators=[phone_regex], help_text=ten_digit)
    is_active = models.BooleanField(default=True)
    username = models.CharField(
        unique=False, max_length=150, null=True, blank=True)
    created_at = models.IntegerField(default=time.time(), editable=False)
    update_at = models.IntegerField(default=time.time(), editable=False)
    delete_at = models.IntegerField(default=time.time())

class SendMessages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp_id = models.ForeignKey(Otp, on_delete=models.CASCADE)
    otp = models.CharField(null=True, max_length=6, blank=True)
    otp_expired_at = models.IntegerField(null=True, blank=True)
    otp_verified = models.BooleanField(default=False)
    created_at = models.IntegerField(default=time.time(), editable=False)
    update_at = models.IntegerField(default=time.time(), editable=False)