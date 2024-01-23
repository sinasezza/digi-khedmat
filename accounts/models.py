import uuid
import pathlib
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class AccountManager(UserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError("Users must have a username")
        
        if not password:
            raise ValueError("Users must have password")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
class Account(AbstractUser):
    
    def user_profile_image_path(instance, filename):
        file_path = pathlib.Path(filename)
        new_filename = str(uuid.uuid1())
        return f"account/{new_filename}{file_path.suffix}"
    # -----------------------------------------
    GENDERS = (
        ('male','مرد'),
        ('female','زن'),
    )
    
    # -----------------------------------------
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # -----------------------------------------
    phone_number    = PhoneNumberField(
            max_length=20,
            region=settings.PHONENUMBER_DEFAULT_REGION,
            null=False,
            blank=False,
            unique=True,
            verbose_name="تلفن"
        )
    # -----------------------------------------
    profile_photo   = models.ImageField(upload_to=user_profile_image_path, null=True, blank=True, verbose_name="عکس پروفایل")
    # -----------------------------------------
    bio             = models.TextField(max_length=1000,null=True,blank=True, verbose_name="بیوگرافی")
    # -----------------------------------------
    age             = models.PositiveSmallIntegerField(default=0 , null=True,blank=True, verbose_name="سن")
    # -----------------------------------------
    gender          = models.CharField(max_length=6,choices=GENDERS,null=True,blank=True, verbose_name="جنسیت")
    # -----------------------------------------
    national_code   = models.CharField(max_length=15, null=True, blank=True, verbose_name="کد ملی")
    # -----------------------------------------
    address = models.CharField(max_length=400, null=True, blank=True, verbose_name="آدرس")
    # -----------------------------------------
    objects = AccountManager()