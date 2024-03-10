import uuid
import jdatetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from accounts.models import Account
from django.db import models
  

class JobCategory(models.Model):
    title           = models.CharField(max_length=30, verbose_name="نام دسته بندی")
    
    class Meta:
        verbose_name_plural = 'Job Categories'

    def __str__(self):
        return self.title

# ================================================

class StuffCategory(models.Model):
    title           = models.CharField(max_length=30, verbose_name="نام دسته بندی")
    
    class Meta:
        verbose_name_plural = 'Stuff Categories'

    def __str__(self):
        return self.title

# ================================================

class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name

    
# ================================================

class Region(models.Model):
    state = models.CharField(max_length=80, verbose_name="استان")
    city     = models.CharField(max_length=100, verbose_name="شهر")
    
    def __str__(self):
        return f"{self.state}-{self.city}"
    

# ================================================

class BaseAdvertisingModel(models.Model):  
    STATUS_CHOICES = (
        ('draft', 'معلق'),
        ('published', 'منتشر شده'),
    )
    # --------------------------------------
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # --------------------------------------
    title = models.CharField(max_length=120, verbose_name="عنوان")
    # --------------------------------------
    slug = models.SlugField(max_length=256, blank=True, unique=True, allow_unicode=True)
    # --------------------------------------
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد آگهی")
    # --------------------------------------
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار آگهی")
    # --------------------------------------
    date_updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")
    # --------------------------------------
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت انتشار",)
    # --------------------------------------
    summary = models.CharField(max_length=400, null=True, blank=True, verbose_name="خلاصه")
    # --------------------------------------
    description = RichTextField(max_length=2000, null=True, blank=True, verbose_name="توضیحات")
    # --------------------------------------
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    # --------------------------------------
    
    
    class Meta:
        abstract = True

    # --------------------------------------
    
    def increment_views(self):
        self.views += 1
        super().save()
    
    # --------------------------------------
    
    
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)       
    #     super().save(*args, **kwargs)
    
    
# ================================================

class Contact(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کاربر")
    # --------------------------------------
    fname = models.CharField(max_length=100, null=True, blank=True, verbose_name="نام")
    # --------------------------------------
    lname = models.CharField(max_length=100, null=True, blank=True, verbose_name="نام خانوادگی")
    # --------------------------------------
    company_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="شرکت")
    # --------------------------------------
    email = models.EmailField(max_length=150, null=True, blank=True, verbose_name="ایمیل")
    # --------------------------------------
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="شماره تلفن")
    # --------------------------------------
    message = models.TextField(max_length=450, verbose_name="نام")
    # --------------------------------------

    def __str__(self):
        return f"{self.fname} {self.lname} - {self.company_name}"
    
# ================================================

class SocialNetwork(models.Model):
    MEDIA_TYPES = (
        ('instagram', "instagram"),
        ('telegram', "telegram"),
        ('twitter(x)', "twitter"),
        ('facebook', "facebook"),
        ('linkedin', "linkedin"),
        ('others', "دیگر"),
    )
    # --------------------------------------
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # -----------------------------------------
    media_type  = models.CharField(max_length=15, choices=MEDIA_TYPES, default='instagram', verbose_name="نوع شبکه")
    # -----------------------------------------
    link = models.CharField(max_length=200, verbose_name="لینک")
    # --------------------------------------
    
    def __str__(self) -> str:
        return f"{self.id} - {self.media_type}: {self.link}"
    