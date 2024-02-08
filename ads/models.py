import uuid
from django.db import models
from generics import models as generics_models


class Advertise(generics_models.BaseAdvertisingModel):
    class Meta:
        default_related_name = "ads"
        

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
    price = models.CharField(max_length=10, null=True, default=True, verbose_name="رایگان")
    # --------------------------------------------------------------------------
    