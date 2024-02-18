import uuid
import pathlib
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db import models
from generics import models as generics_models
from accounts import models as accounts_models


class StuffAdvertising(generics_models.BaseAdvertisingModel):
    STUFF_STATUSES = (
        ('unknown', "نامشخص"),
        ('new', "نو"),
        ('semi-new', "در حد نو"),
        ('used', "کارکرده"),
        ('defective', "معیوب"),
    )
    # --------------------------------------------------------------------------
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='stuff_ads', null=True, blank=True, verbose_name="مالک")
    # --------------------------------------------------------------------------
    stuff_status = models.CharField(max_length=60, default='unknown', choices=STUFF_STATUSES, verbose_name="وضعیت کالا")
    # --------------------------------------------------------------------------
    price = models.CharField(max_length=25, null=True, default="رایگان" , verbose_name="قیمت")
    # --------------------------------------------------------------------------
    region  = models.ForeignKey(to=generics_models.Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='stuffs', verbose_name="منطقه")
    # --------------------------------------
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="آدرس")
    
    class Meta:
        pass
    
    # --------------------------------------------------------------------------
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    # --------------------------------------------------------------------------
    
    def get_absolute_url(self):
        return reverse("ads:adv-detail", kwargs={"adv_slug": self.slug})
    
    # --------------------------------------------------------------------------
    
    def get_edit_url(self):
        return reverse("ads:adv-update", kwargs={"adv_slug": self.slug})
    
    # --------------------------------------------------------------------------
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = f"{self.id}-{slugify(value=self.title, allow_unicode=True)}"
        super().save(*args, **kwargs)
    
    # --------------------------------------------------------------------------

# ==============================================================
    
class StuffImage(models.Model):
    def stuff_image_path(instance, filename):
        file_path = pathlib.Path(filename)
        new_filename = str(uuid.uuid1())
        return f"barters/imgs/{new_filename}{file_path.suffix}"
    
    title = models.CharField(max_length=40, null=True, blank=True, verbose_name="عنوان")
    image = models.ImageField(max_length=255, upload_to=stuff_image_path, verbose_name="تصویر")
    stuff_advertising = models.ForeignKey(StuffAdvertising, on_delete=models.CASCADE, related_name='images', verbose_name="تبلیغات کالا")

    def __str__(self):
        return f"{self.id}>{self.title}"

# ==============================================================

class BusinessAdvertising(models.Model):
    BUSINESS_TYPES = (
        ('unknown', "نامشخص"),
        ('offline', "آفلاین"),
        ('online', "آنلاین"),
        ('hybrid', "ترکیبی"),
    )
    # ----------------------------------------------------------
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ----------------------------------------------------------
    business_type = models.CharField(max_length=10, choices=BUSINESS_TYPES, default="unknown" ,verbose_name="نوع کسب و کار")
    # ----------------------------------------------------------
    name = models.CharField(max_length=100, verbose_name="نام کسب و کار")
    # ----------------------------------------------------------
    web_address = models.CharField(max_length=200, null=True, blank=True, verbose_name="آدرس وبسایت")
    # ----------------------------------------------------------
    social_networks = models.ManyToManyField(to=generics_models.SocialNetwork, blank=True, verbose_name="شبکه های اجتماعی")
    # ----------------------------------------------------------
    business_address = models.CharField(max_length=300, null=True, blank=True, verbose_name="آدرس کسب و کار")
    # ----------------------------------------------------------
    description = models.TextField(max_length=800, null=True, blank=True, verbose_name="توضیحات")
    # ----------------------------------------------------------
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="تلفن")
    # ----------------------------------------------------------
    region  = models.ForeignKey(to=generics_models.Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='businesses', verbose_name="منطقه")
    # --------------------------------------
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="آدرس")
    
    
    class Meta:
        pass
    

# ==============================================================

class BusinessImage(models.Model):
    def business_image_path(instance, filename):
        file_path = pathlib.Path(filename)
        new_filename = str(uuid.uuid1())
        return f"ads/business/imgs/{new_filename}{file_path.suffix}"
    # ----------------------------------------------------------
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name="عنوان")
    # ----------------------------------------------------------
    image = models.ImageField(upload_to=business_image_path, verbose_name="عکس")
    # ----------------------------------------------------------
    business_advertising = models.ForeignKey(to=BusinessAdvertising, on_delete=models.CASCADE, null=True, blank=True, related_name='images', verbose_name="آگهی کسب و کار")

# ==============================================================