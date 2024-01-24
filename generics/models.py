import uuid
import jdatetime
from django.utils.text import slugify
from django.db import models
  

class Category(models.Model):
    CATEGORY_LIST   = (("shop", "فروشگاهی"), ("services", "خدماتی"), ("productive", "تولیدی"))
    title           = models.CharField(max_length=30, verbose_name="نام دسته بندی")
    category_type  = models.CharField(max_length=20, choices=CATEGORY_LIST, verbose_name="نوع کسب و کار", default="shop",)

    def __str__(self):
        return self.title

# ================================================

class Tag(models.Model):
    name = models.CharField(max_length=50)

    
# ================================================

class Location(models.Model):
    province        = models.CharField(max_length=80, verbose_name="استان")
    city            = models.CharField(max_length=100, verbose_name="شهر")
    address         = models.CharField(max_length=255, verbose_name="آدرس")
    
    class Meta:
        verbose_name = 'Location'

# ================================================

class BaseAdvertisingModel(models.Model):  
    STATUS_CHOICES = (
        ('published', 'منتشر شده'),
        ('draft', 'معلق'),
    )
    # --------------------------------------
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # --------------------------------------
    title = models.CharField(max_length=120, verbose_name="عنوان")
    # --------------------------------------
    slug = models.SlugField(max_length=200, unique=True)
    # --------------------------------------
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد آگهی")
    # --------------------------------------
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار آگهی")
    # --------------------------------------
    date_updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")
    # --------------------------------------
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True, verbose_name="وضعیت انتشار",)
    # --------------------------------------
    summary = models.CharField(max_length=400, null=True, blank=True, verbose_name="خلاصه")
    # --------------------------------------
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="توضیحات")
    # --------------------------------------
    categories = models.ManyToManyField(Category, blank=True, verbose_name='دسته بندی')
    # --------------------------------------
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="تگ")
    # --------------------------------------
    locations = models.ManyToManyField(to=Location, verbose_name="موقعیت(های) مکانی")
    # --------------------------------------

    
    class Meta:
        abstract = True
        ordering = ("-date_published",)

    # --------------------------------------
    
    @property
    def JaliliDateCreated(self):
        return jdatetime.date.fromgregorian(
            day=self.date_created.day,
            month=self.date_created.month,
            year=self.date_created.year,
        )

    # --------------------------------------    

    @property
    def JaliliDatePublished(self):
        return jdatetime.date.fromgregorian(
            day=self.date_published.day,
            month=self.date_published.month,
            year=self.date_published.year,
        )
    
    # --------------------------------------
    
    @property
    def JalaliDateUpdated(self):
        return jdatetime.date.fromgregorian(
            day=self.date_updated.day,
            month=self.date_updated.month,
            year=self.date_updated.year,
        )
    
    # --------------------------------------
    
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)       
    #     super().save(*args, **kwargs)