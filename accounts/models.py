import uuid
import pathlib
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    

# ==================================================================================

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
    phone_number = models.CharField(
        max_length=20,
        # region=settings.PHONENUMBER_DEFAULT_REGION,
        null=False,
        blank=False,
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

# ==================================================================================

class NotificationManager(models.Manager):
    def unseen_notifications(self):
        return self.filter(seen=False)

class Notification(models.Model):
    TYPES = (
        ('success', "موفقیت"),
        ('info', "اطلاع رسانی"),
        ('warning', "هشدار"),
        ('error', "خطا"),
    )

    type = models.CharField(max_length=20, default="info", choices=TYPES, verbose_name="نوع")
    # -----------------------------------------
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifications', verbose_name="دریافت کننده")
    # -----------------------------------------
    seen = models.BooleanField(default=False, db_index=True, verbose_name="دیده شده")
    # -----------------------------------------
    message = models.CharField(max_length=255,  verbose_name="پیغام")
    # -----------------------------------------
    review_link = models.URLField(max_length=200, blank=True, null=True, verbose_name="لینک بررسی")
    # -----------------------------------------
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    # -----------------------------------------
    
    objects = NotificationManager()
      
    class Meta:
        ordering = ['-date_created']
        index_together = ('recipient', 'seen')
    
    # -----------------------------------------
    
    def toggle_seen(self):
        self.seen = not self.seen
        self.save()

    # -----------------------------------------

# ==================================================================================

class Favorite(models.Model):
    owner = models.ForeignKey(Account, related_name='favorites', on_delete=models.CASCADE, verbose_name="مالک")
    # -----------------------------------------
    advertisement_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="نوع آگهی")
    # -----------------------------------------
    object_id = models.UUIDField(verbose_name="شناسه آگهی")
    # -----------------------------------------
    advertisement = GenericForeignKey("advertisement_type", "object_id")
    # -----------------------------------------
    date_created = models.DateTimeField(auto_now_add=True,  verbose_name='تاریخ ثبت')
    # -----------------------------------------
    
    class Meta:
        indexes = [
            models.Index(fields=["advertisement_type", "object_id"]),
        ]

# ==================================================================================
