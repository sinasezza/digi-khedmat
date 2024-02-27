import uuid
import pathlib
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
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
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="تلفن")
    # -----------------------------------------
    profile_photo   = models.ImageField(upload_to=user_profile_image_path, null=True, blank=True, verbose_name="عکس پروفایل")
    # -----------------------------------------
    bio             = models.TextField(max_length=1000, null=True, blank=True, verbose_name="بیوگرافی")
    # -----------------------------------------
    age             = models.PositiveSmallIntegerField(default=0 , null=True,blank=True, verbose_name="سن")
    # -----------------------------------------
    gender          = models.CharField(max_length=6,choices=GENDERS,null=True,blank=True, verbose_name="جنسیت")
    # -----------------------------------------
    national_code   = models.CharField(max_length=15, null=True, blank=True, verbose_name="کد ملی")
    # -----------------------------------------
    address = models.CharField(max_length=400, null=True, blank=True, verbose_name="آدرس")
    # -----------------------------------------
    education = models.CharField(max_length=70, null=True, blank=True, verbose_name="تحصیلات")
    # -----------------------------------------
    occupation = models.CharField(max_length=100, null=True, blank=True, verbose_name="شغل")
    # -----------------------------------------
    company_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="نام شرکت")
    # -----------------------------------------
    info_complete = models.BooleanField(default=False, verbose_name="اطلاعات کامل است؟")
    # -----------------------------------------
    favorites = GenericRelation(to='Favorite', object_id_field='object_id', content_type_field='advertisement_type')
    # -----------------------------------------
    
    
    objects = AccountManager()
    # -----------------------------------------
    
    REQUIRED_FIELDS = ["phone_number","email"]
    
    # -----------------------------------------
    
    def get_user_profile(self):
        return reverse("accounts:user-profile", kwargs={"id":self.id,})
    
    # -----------------------------------------
    
    def get_chat_url(self):
        return reverse('chat:get-create-chat-room', kwargs={"receiver_id": self.id})
    
    # -----------------------------------------
    
    @property
    def advertising_count(self):
        barters_count = self.barters.count()
        jobs_count = self.jobs.count()
        stuff_ads = self.stuff_ads.all().count()
        
        return  barters_count + jobs_count  + stuff_ads


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
    
    # -----------------------------------------
    
    def __str__(self) -> str:
        return f"{self.owner.username}'s  favorite for {self.advertisement}"

# ==================================================================================

class OneTimePassword(models.Model):
    code = models.CharField(max_length=6, unique=True, verbose_name="کد")
    # -----------------------------------------
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="otp", verbose_name="کاربر")
    # -----------------------------------------
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    # -----------------------------------------
    
        
    def __str__(self) -> str:
        return f"code -{self.code} for {self.user}"