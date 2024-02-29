import uuid
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
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
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def name(self):
        # Iterate over COOPERATION_TYPES to find the label for the current type
        for choice in self.COOPERATION_TYPES:
            if choice[0] == self.type:
                return choice[1]
        return '-'  # Return an empty string if the type is not found

# =======================================================================

class StudyGrade(models.Model):
    grade = models.CharField(max_length=100, verbose_name="نام مقطع")
    
    def  __str__(self) -> str:
        return  self.grade
    
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
    cooperation_types = models.ManyToManyField(to=CooperationType, blank=True, related_name='jobs', verbose_name="نوع همکاری")
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
    military_service = models.CharField(max_length=50, null=True, blank=True, verbose_name="وضعیت سربازی")
    # --------------------------------------
    region  = models.ForeignKey(to=generics_models.Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs', verbose_name="منطقه")
    # --------------------------------------
    categories = models.ManyToManyField(to=generics_models.JobCategory, blank=True, related_name='jobs', verbose_name="دسته بندی")
    # --------------------------------------
    tags = models.ManyToManyField(generics_models.Tag, blank=True, related_name='jobs', verbose_name="برچسب ها")
    # --------------------------------------
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="آدرس")
    # --------------------------------------
    
    
    class Meta:
        default_related_name = "jobs"

    # --------------------------------------
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    # --------------------------------------
    
    def get_absolute_url(self):
        return reverse("jobs:job-detail", kwargs={"job_slug": self.slug})
    
    # --------------------------------------
    
    def get_edit_url(self):
        return reverse("jobs:job-update", kwargs={"job_slug": self.slug})
    
    # --------------------------------------
    
    def update_cooperation_types(self, types):
        self.cooperation_types.set(types)
        super().save()
    
    # --------------------------------------
    
    def update_categories(self, categories):
        self.categories.set(categories)
        super().save()
    
    # --------------------------------------
    
    def update_tags(self, tags):
        self.tags.set(tags)
        super().save()
    
    # --------------------------------------
    
    def get_gender(self):
        # Iterate over GENDERS to find the label for the current gender title
        for gender in self.GENDERS:
            if gender[0] == self.gender:
                return gender[1]
        return '-'  # Return an empty string if the type is not found
    
    # --------------------------------------
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = f"{self.id}-{slugify(value=self.title, allow_unicode=True)}"
        super().save(*args, **kwargs)
    
    # --------------------------------------

# =======================================================================

class JobGroup(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="نام")
    job_advertising = models.ForeignKey(to=JobAdvertising, on_delete=models.CASCADE, null=True, blank=True, related_name='job_groups', verbose_name="آگهی کاریابی")
    
    class Meta:
        verbose_name = "گروه شغلی"
        verbose_name_plural = "گروه های شغلی"
        

# =======================================================================

class StudyField(models.Model):
    field = models.CharField(max_length=100, verbose_name="نام رشته")
    job_advertising = models.ForeignKey(to=JobAdvertising, on_delete=models.CASCADE, null=True, blank=True, related_name='study_fields', verbose_name="آگهی کاریابی")
    
    class Meta:
        verbose_name = "رشته تحصیلی"
        verbose_name_plural = "رشته های تحصیلی"

# =======================================================================

class BaseResumeManager(models.Manager):
    
    def unseen_resumes(self):
        return self.filter(seen=False)
    
    # --------------------------------------
    
    def unseen_count(self):
        return self.filter(seen=False).count()
    
    # --------------------------------------
    

class BaseResume(models.Model):
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # --------------------------------------
    title = models.CharField(max_length=80, blank=True, verbose_name="عنوان شغلی")
    # --------------------------------------
    fname = models.CharField(max_length=255, null=True, blank=True, verbose_name="نام")
    # --------------------------------------
    lname = models.CharField(max_length=255, null=True, blank=True, verbose_name="نام خانوادگی")
    # --------------------------------------
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name="توضیحات")
    # -----------------------------------------
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    # -----------------------------------------
    seen = models.BooleanField(default=False, verbose_name="مشاهده شده")
    # -----------------------------------------
    is_sent = models.BooleanField(default=False, verbose_name="ارسال شده")
    # -----------------------------------------
    
    objects = BaseResumeManager()

    
    class Meta:
        abstract = True
    
    # -----------------------------------------
    
    
    def __str__(self):
        return f"adv:{self.advertisement} - name:{self.full_name} - title:{self.title}"

    # --------------------------------------
    
    def send(self):
        self.is_sent = True
        super.save()
    
    # -----------------------------------------
    
    @property
    def full_name(self):
        return f"{self.fname} {self.lname}"

    # --------------------------------------
    
    def mark_as_seen(self, commit=False):
        self.seen = True
        if commit:
            super().save()
    
    # -----------------------------------------
    


# =======================================================================

class ResumeFile(BaseResume):
    def resume_pdf_file_path(instance, filename):
        new_filename = str(uuid.uuid1())
        return f"jobs/cvs/pdfs/{new_filename}.pdf"

    # --------------------------------------
    employer = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='rcv_resume_files', verbose_name="کارفرما")
    # --------------------------------------
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='resume_files', verbose_name="کاربر")
    # --------------------------------------
    advertisement = models.ForeignKey(to=JobAdvertising, on_delete=models.CASCADE, blank=True, null=True, related_name='resume_files', verbose_name="آگهی")
    # -----------------------------------------
    pdf_file = models.FileField(max_length=100, upload_to=resume_pdf_file_path, null=True, blank=True, verbose_name="فایل رزومه")
    # --------------------------------------

    def get_absolute_url(self):
        return reverse("jobs:resume-file-detail", kwargs={"id": self.id})
    
    # -----------------------------------------
    
    def get_pdf_url(self):
        return reverse("jobs:pdf-download", kwargs={'id': self.id})
    

    

# =======================================================================

class Resume(BaseResume):
    def resume_image_path(instance, filename):
        new_filename = str(uuid.uuid1())
        return f"jobs/cvs/images/{new_filename}.png"
    
    # --------------------------------------
    
    GENDERS = (
        ("male", "مرد"),
        ("female", "زن"),
    )
    
    # --------------------------------------
    employer = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='rcv_resumes', verbose_name="کارفرما")
    # --------------------------------------
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='resumes', verbose_name="کاربر")
    # --------------------------------------
    advertisement = models.ForeignKey(to=JobAdvertising, on_delete=models.CASCADE, blank=True, null=True, related_name='resumes', verbose_name="آگهی")
    # -----------------------------------------
    gender = models.CharField(max_length=15, default="male", choices=GENDERS, verbose_name="جنسیت")
    # --------------------------------------
    military_service = models.CharField(max_length=200, null=True, blank=True, verbose_name="وضعیت سربازی")
    # --------------------------------------
    image = models.ImageField(upload_to=resume_image_path, null=True, blank=True, verbose_name="عکس")
    # --------------------------------------
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name="شماره تلفن")
    # --------------------------------------
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="ایمیل")
    # --------------------------------------
    linkedin = models.CharField(max_length=255, null=True, blank=True, verbose_name="آدرس لینکدین")
    # --------------------------------------
    github = models.CharField(max_length=255, null=True, blank=True, verbose_name="آدرس گیتهاب")
    # --------------------------------------
    website = models.CharField(max_length=255, null=True, blank=True, verbose_name="آدرس وبسایت")
    # --------------------------------------

    class Meta:
        pass

    # --------------------------------------

    def get_absolute_url(self):
        return reverse("jobs:resume-detail", kwargs={"id": self.id})
    
    # --------------------------------------
    
    def get_complete_url(self):
        return reverse("jobs:resume-complete", kwargs={'resume_id': self.id})
    
    # --------------------------------------
    
    @property
    def gender_name(self):
        # Iterate over GENDERS to find the label for the current gender
        for choice in self.GENDERS:
            if choice[0] == self.gender:
                return choice[1]
        return '-'  # Return an empty string if the gender is not found   
    
    # --------------------------------------



# =======================================================================

class Experience(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    # --------------------------------------
    company = models.CharField(max_length=255, verbose_name="شرکت/مجموعه")
    # --------------------------------------
    start_date = models.DateField(null=True, blank=True, verbose_name="تاریخ شروع")
    # --------------------------------------
    end_date = models.DateField(null=True, blank=True, verbose_name="تاریخ پایان")
    # --------------------------------------
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="توضیحات")    
    # --------------------------------------
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    # --------------------------------------

    def __str__(self):
        return f"resume:{self.resume} - title:{self.title}"

    class Meta:
        pass

# =======================================================================

class Skill(models.Model):
    title = models.CharField(max_length=80, verbose_name="عنوان")
    # --------------------------------------
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    # --------------------------------------

    def __str__(self):
        return f"resume:{self.resume} - title:{self.title}"

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

    def __str__(self):
        return f"resume:{self.resume} - title:{self.title}"

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


    def __str__(self):
        return f"resume:{self.resume} - title:{self.title}"

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
    
    class Meta:
        pass

    # --------------------------------------

    def __str__(self):
        return f"resume:{self.resume} - title:{self.name} - level:{self.level}"
    
    # --------------------------------------
    
    @property
    def level_name(self) -> str:
        # Iterate over LEVELS to find the label for the current level
        for choice in self.LEVELS:
            if choice[0] == self.level:
                return choice[1]
        return '-'  # Return an empty string if the level is not found



# =======================================================================