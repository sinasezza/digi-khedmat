import uuid
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
        ordering = ('date_published',)
    
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
    