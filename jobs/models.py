from django.db import models
from generics import models as generics_models


class JobAdvertising(generics_models.BaseAdvertisingModel):
    class Meta:
        default_related_name = "jobs"