import uuid
from django.db import models
from generics import models as generics_models


class Advertise(generics_models.BaseAdvertisingModel):
    class Meta:
        default_related_name = "ads"