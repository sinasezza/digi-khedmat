import uuid
import pathlib
from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from generics import models as generics_models


class Advertise(generics_models.BaseAdvertisingModel):
    class Meta:
        default_related_name = "ads"
        verbose_name_plural = "ads(s)"

# ==============================================================

class StuffAdvertising(generics_models.BaseAdvertisingModel):
    STUFF_STATUSES = (
        ('unknown', "نامشخص"),
        ('new', "نو"),
        ('semi-new', "در حد نو"),
        ('used', "کارکرده"),
        ('defective', "معیوب"),
    )
    # --------------------------------------------------------------------------
    stuff_status = models.CharField(max_length=60, default='unknown', choices=STUFF_STATUSES, verbose_name="وضعیت کالا")
    # --------------------------------------------------------------------------
    price = models.CharField(max_length=10, null=True, default="رایگان" , verbose_name="قیمت")
    # --------------------------------------------------------------------------
    
    class Meta:
        pass
    
    # --------------------------------------------------------------------------
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    # --------------------------------------------------------------------------
    
    def get_absolute_url(self):
        return reverse("ads:adv_detail", kwargs={"adv_slug": self.slug})
    
    # --------------------------------------------------------------------------
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = f"{self.id}-{slugify(self.title)}"
        super().save(*args, **kwargs)
    
    # --------------------------------------------------------------------------

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

# ==============================================================

class BusinessAdvertising():
    name = models.CharField(max_length=100, verbose_name="نام کسب و کار")
    # ----------------------------------------------------------
    images = models.ManyToManyField(to=BusinessImage, blank=True, verbose_name="تصاویر")
    # ----------------------------------------------------------
    web_address = models.CharField(max_length=200, null=True, blank=True)
    social_network = models.CharField(max_length=200, null=True, blank=True)
    shop_address = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    B_phone = models.CharField(max_length=13, verbose_name="تلفن")

# ==============================================================