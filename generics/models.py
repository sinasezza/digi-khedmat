import uuid
import jdatetime
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.db import models
  

class Category(models.Model):
    CATEGORY_LIST   = (("shop", "فروشگاهی"), ("services", "خدماتی"), ("productive", "تولیدی"))
    title           = models.CharField(max_length=30, verbose_name="نام دسته بندی")
    category_type   = models.CharField(max_length=20, choices=CATEGORY_LIST, verbose_name="نوع کسب و کار", default="shop",)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

# ================================================

class Tag(models.Model):
    name = models.CharField(max_length=50)

    
# ================================================

class Region(models.Model):
    state = models.CharField(max_length=80, verbose_name="استان")
    city     = models.CharField(max_length=100, verbose_name="شهر")

# ================================================

class Address(models.Model):
    region  = models.ForeignKey(to=Region, on_delete=models.CASCADE, verbose_name="منطقه")
    address = models.CharField(max_length=255, verbose_name="آدرس")
    

# ================================================

class BaseAdvertisingModel(models.Model):  
    STATUS_CHOICES = (
        ('draft', 'معلق'),
        ('published', 'منتشر شده'),
    )
    # --------------------------------------
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # --------------------------------------
    title = models.CharField(max_length=120, verbose_name="عنوان")
    # --------------------------------------
    slug = models.SlugField(max_length=256, unique=True)
    # --------------------------------------
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد آگهی")
    # --------------------------------------
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار آگهی")
    # --------------------------------------
    date_updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")
    # --------------------------------------
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت انتشار",)
    # --------------------------------------
    summary = models.CharField(max_length=400, null=True, blank=True, verbose_name="خلاصه")
    # --------------------------------------
    description = RichTextField(max_length=2000, null=True, blank=True, verbose_name="توضیحات")
    # --------------------------------------
    categories = models.ManyToManyField(Category, blank=True, verbose_name='دسته بندی')
    # --------------------------------------
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="تگ")
    # --------------------------------------
    addresses = models.ManyToManyField(to=Address, blank=True, verbose_name="موقعیت(های) مکانی")
    # --------------------------------------
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    
    class Meta:
        abstract = True

    # --------------------------------------
    
    def increment_views(self):
        self.views += 1
        super().save()
    
    # --------------------------------------
    
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)       
    #     super().save(*args, **kwargs)