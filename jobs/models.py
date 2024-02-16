import uuid
from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from generics import models as generics_models
from accounts.models import Account


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
    # ---------------------------------------------------------------------
    owner = models.ForeignKey(to=Account, on_delete=models.CASCADE, null=True, blank=True, related_name="jobs", verbose_name="مالک")
    # ---------------------------------------------------------------------
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

    # --------------------------------------
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    # --------------------------------------
    
    def get_absolute_url(self):
        return reverse("jobs:job-detail", kwargs={"job_slug": self.slug})
    
    # --------------------------------------
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = f"{self.id}-{slugify(value=self.title, allow_unicode=True)}"
        super().save(*args, **kwargs)
    
    # --------------------------------------
    

# =======================================================================

class Resume(models.Model):
    def resume_image_path(instance, filename):
        new_filename = str(uuid.uuid1())
        return f"jobs/cvs/images/{new_filename}.png"
    
    # --------------------------------------
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # --------------------------------------
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="کاربر")
    # --------------------------------------
    fname = models.CharField(max_length=255, verbose_name="نام")
    # --------------------------------------
    lname = models.CharField(max_length=255, verbose_name="نام خانوادگی")
    # --------------------------------------
    title = models.CharField(max_length=80, blank=True, verbose_name="عنوان شغلی")
    # --------------------------------------
    description = models.TextField(max_length=255, blank=True, verbose_name="توضیحات")
    # --------------------------------------
    image = models.ImageField(upload_to=resume_image_path, null=True, blank=True, verbose_name="عکس")
    # --------------------------------------
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name="شماره تلفن")
    # --------------------------------------
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="ایمیل")
    # --------------------------------------
    linkedin = models.CharField(max_length=255,  null=True, blank=True, verbose_name="آدرس لینکدین")
    # --------------------------------------
    github = models.CharField(max_length=255,  null=True, blank=True, verbose_name="آدرس گیتهاب")
    # --------------------------------------
    website = models.CharField(max_length=255,  null=True, blank=True, verbose_name="آدرس وبسایت")
    # --------------------------------------


    class Meta:
        pass

    # --------------------------------------

    def __str__(self):
        return f"{self.full_name} - {self.title}"

    # --------------------------------------
    
    @property
    def full_name(self):
        return f"{self.fname} {self.lname}"

    # --------------------------------------

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # --------------------------------------


# =======================================================================

class ResumeFile(models.Model):
    def resume_pdf_file_path(instance, filename):
        new_filename = str(uuid.uuid1())
        return f"jobs/cvs/pdfs/{new_filename}.pdf"
    # --------------------------------------
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # --------------------------------------
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="کاربر")
    # --------------------------------------
    pdf_file = models.FileField(max_length=100, upload_to=resume_pdf_file_path, null=True, blank=True, verbose_name="فایل رزومه")
    # --------------------------------------
    advertisement_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="نوع آگهی")
    # -----------------------------------------
    object_id = models.UUIDField(verbose_name="شناسه آگهی")
    # -----------------------------------------
    advertisement = GenericForeignKey("advertisement_type", "object_id")
    # -----------------------------------------
    date_sent = models.DateTimeField(auto_now_add=True,  verbose_name='تاریخ ارسال')
    # -----------------------------------------

# =======================================================================

class Experience(models.Model):
    title = models.CharField(max_length=255)
    # --------------------------------------
    company = models.CharField(max_length=255)
    # --------------------------------------
    start_date = models.DateField(null=True, blank=True, verbose_name="تاریخ شروع")
    # --------------------------------------
    end_date = models.DateField(null=True, blank=True, verbose_name="تاریخ پایان")
    # --------------------------------------
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="توضیحات")    
    # --------------------------------------
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    # --------------------------------------
    order = models.IntegerField(blank=False, default=100_000)
    # --------------------------------------

    def tech_as_list(self):
        tech_list = ""
        if not self.tech == "":
            tech_list = self.tech.replace(", ", ",").split(',')
            tech_list = [x[0].upper() + x[1:] for x in tech_list]
        return tech_list

    def __str__(self):
        return self.title

    class Meta:
        pass

# =======================================================================


class Skill(models.Model):
    title = models.CharField(max_length=80, verbose_name="عنوان")
    # --------------------------------------
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    # --------------------------------------
    order = models.IntegerField(blank=False, default=100_000)
    # --------------------------------------

    def __str__(self):
        return self.title

    class Meta:
        pass

# =======================================================================

class Education(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    # --------------------------------------
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="توضیحات")
    # --------------------------------------
    start_date = models.DateField(null=True, blank=True, verbose_name="تاریخ شروع")
    # --------------------------------------
    end_date = models.DateField(null=True, blank=True, verbose_name="تاریخ پایان")
    # --------------------------------------
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    # --------------------------------------
    order = models.IntegerField(blank=False, default=100_000)
    # --------------------------------------

    def __str__(self):
        return self.title

    class Meta:
        pass

# =======================================================================

class Achievement(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    # --------------------------------------
    description = models.TextField(blank=True, verbose_name="توضیحات")
    # --------------------------------------
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='achievements')
    # --------------------------------------
    order = models.IntegerField(blank=False, default=100_000)
    # --------------------------------------

    def __str__(self):
        return self.title

    class Meta:
        pass

# =======================================================================

class Language(models.Model):
    LEVELS = (
        ('beginner', "مبتدی"),
        ('intermediate', "متوسط"),
        ('professional', "حرفه ای"),
    )
    name = models.CharField(max_length=255, verbose_name="نام")
    # --------------------------------------
    level = models.CharField(max_length=255, choices=LEVELS, default='beginner', verbose_name="سطح")
    # --------------------------------------
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    # --------------------------------------
    order = models.IntegerField(blank=False, default=100_000)
    # --------------------------------------

    def __str__(self):
        return self.title

    class Meta:
        pass

# =======================================================================