from django.db import models
from generics import models as generics_models


class CooperationType(models.Model):
    COOPERATION_TYPES = (
        ('full_time', "تمام وقت"),
        ('part_time', "پاره وقت"),
        ('contract', "قراردادی"),
        ('hybrid', "هیبریدی/ترکیبی"),
    )
    type = models.CharField(max_length=50, choices=COOPERATION_TYPES, verbose_name="نوع")
    
    class Meta:
        verbose_name = "نوع همکاری"
        verbose_name_plural = "انواع همکاری"

# =======================================================================

class JobGroup(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="نام")
    
    class Meta:
        verbose_name = "گروه شغلی"
        verbose_name_plural = "گروه های شغلی"
        

# =======================================================================

class StudyField(models.Model):
    field = models.CharField(max_length=100, verbose_name="نام رشته")
    
    class Meta:
        verbose_name = "رشته تحصیلی"
        verbose_name_plural = "رشته های تحصیلی"
        

# =======================================================================

class StudyGrade(models.Model):
    grade = models.CharField(max_length=100, verbose_name="نام مقطع")
    
    class Meta:
        verbose_name = "مقطع تحصیلی"
        verbose_name_plural = "مقاطع تحصیلی"
        
        
# =======================================================================

class JobAdvertising(generics_models.BaseAdvertisingModel):
    GENDERS = (
        ("male", "مرد"),
        ("female", "زن"),
        ("unknown", "فرقی نمیکند"),
    )
    cooperation_types = models.ManyToManyField(to=CooperationType, blank=True, verbose_name="نوع همکاری")
    # ---------------------------------------------------------------------
    group = models.ForeignKey(to=JobGroup, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="گروه شعلی")
    # ---------------------------------------------------------------------
    study_field = models.ForeignKey(to=StudyField, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="رشته تحصیلی")
    # ---------------------------------------------------------------------
    study_grade = models.ForeignKey(to=StudyGrade, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="مقطع تحصیلی")
    # ---------------------------------------------------------------------
    gender = models.CharField(max_length=15, default="unknown", choices=GENDERS, verbose_name="جنسیت")
    # ---------------------------------------------------------------------
    age_range = models.CharField(max_length=30, null=True, blank=True, verbose_name="بازه سنی")
    # ---------------------------------------------------------------------
    skills = models.TextField(max_length=1000, null=True, blank=True, verbose_name="الزامات / مهارت ها")
    # ---------------------------------------------------------------------
    benefits = models.TextField(max_length=1000, null=True, blank=True, verbose_name="مزایا")
    # ---------------------------------------------------------------------
    work_time = models.CharField(max_length=150, null=True, blank=True, verbose_name="ساعات کاری")
    # ---------------------------------------------------------------------
    
    class Meta:
        default_related_name = "jobs"

# =======================================================================

