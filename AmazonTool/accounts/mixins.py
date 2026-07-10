import random
from .tasks import send_otp_mail , send_email_otp_mail
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class OtpMixin:
    def send_or_resend_otp(self,user):
        otp = str(random.randint(100000,999999))
        print(otp)
        user.otp = make_password(otp)
        user.otp_created_at = timezone.now()
        user.otp_block_time = None
        user.otp_attempt = 0
        user.save()
        send_otp_mail.delay(user.email,otp)
        return otp
    
class EmailOtpMixin:
    def send_or_resend_email_otp(self,user):
        otp = str(random.randint(100000,999999))
        print(otp)
        user.otp = make_password(otp)
        user.otp_created_at = timezone.now()
        user.otp_block_time = None
        user.otp_attempt = 0
        user.save()
        send_email_otp_mail.delay(user.pending_email,otp)
        return otp