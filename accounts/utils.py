import random
import string
import threading
import time
import datetime
from django.utils import timezone
from django.conf import settings
from sms_ir import SmsIr
from . import models


def find_phone_number_owner(phone_number):
    user =  models.Account.objects.filter(phone_number=phone_number)
    if user.exists():
        return user.first()
    else:
        return None

# ----------------------------------------------------------

def generate_otp(length=7):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

# ----------------------------------------------------------

def check_last_otp(user):
    last_otp = user.otp.last()
    
    if not last_otp:
        return True

    # Compare the OTP creation time plus 2 minutes with the current time
    if last_otp.created_at + timezone.timedelta(minutes=2) > timezone.now():
        return False
    else:
        return True


# ----------------------------------------------------------

def send_otp_phone_number(phone_number, otp):
    """Send OTP to the given phone number using sms.ir API."""
    sms_ir = SmsIr(settings.SMS_API_KEY, settings.SMS_LINE_NUMBER)
    # result = sms_ir.send_verify_code(
    #     number=phone_number,
    #     template_id=settings.SMS_TEMPLATE,
    #     parameters=[
    #         {
    #             "name" : "code",
    #             "value": otp,
    #         },
    #     ],
    # )

# ----------------------------------------------------------

def delete_otp_after_2_minutes(otp_obj):
    time.sleep(120)         # sleep for 2 minutes
    # try to delete the code
    try:
        otp_obj.delete()           
    except:
        pass

# ----------------------------------------------------------

def create_otp(phone_number, user):
    
    otp = generate_otp()
    # send_otp_phone_number(phone_number, otp)
    
    otp_obj = models.OneTimePassword.objects.create(user=user, code=otp)
    delete_thread = threading.Thread(target=delete_otp_after_2_minutes, kwargs={"otp_obj": otp_obj})
    delete_thread.start()