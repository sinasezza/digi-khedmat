import uuid
import jdatetime
import pathlib
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils.text import slugify
from django.contrib.sites.models import Site
from django.utils import timezone
# from shortuuid.django_fields import ShortUUIDField
from django.db import models
from django.urls import reverse
from account.models import Account


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

class StuffImage(models.Model):
    def stuff_image_path(instance, filename):
        file_path = pathlib.Path(filename)
        new_filename = str(uuid.uuid1())
        return f"stuff/imgs/{new_filename}{file_path.suffix}"
    
    title = models.CharField(max_length=40, null=True, blank=True, verbose_name="عنوان")
    image = models.ImageField(max_length=255, upload_to=stuff_image_path, verbose_name="تصویر")
    
# ================================================

class Stuff(models.Model):  
    def stuff_qrcode_path(instance, filename):
        new_filename = str(uuid.uuid1())
        return f"stuff/qrcodes/{new_filename}.png"
    
    STATUS_CHOICES = (
        ('published', 'منتشر شده'),
        ('draft', 'معلق'),
    )
    id    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # --------------------------------------
    # id = ShortUUIDField(primary_key=True, length=11, max_length=11)
    # --------------------------------------
    title = models.CharField(max_length=120, verbose_name="عنوان")
    # --------------------------------------
    slug = models.SlugField(max_length=200, unique=True)
    # --------------------------------------
    owner = models.ForeignKey(to=Account, null=False, blank=False, on_delete=models.CASCADE, verbose_name="مالک")
    # --------------------------------------
    url_address = models.URLField(max_length=300, null=True, blank=True, verbose_name="آدرس url آگهی") 
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
    category = models.ManyToManyField(Category, blank=True)
    # --------------------------------------
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=("تگ"))
    # --------------------------------------
    images = models.ManyToManyField(StuffImage, related_name="stuffs", blank=True, verbose_name="تصاویر")
    # --------------------------------------
    location = models.CharField(max_length=100, verbose_name="موقعیت آگهی")
    # --------------------------------------
    qrcode_image = models.ImageField(max_length=255, upload_to=stuff_qrcode_path, blank=True, null=True)
    # --------------------------------------
    
    class Meta:
        ordering = ("-date_published",)
        default_related_name = "stuffs"
    # --------------------------------------
    
    def get_absolute_url(self):
        return reverse("barter:stuff-detail", kwargs={"stuff_id": self.id, "stuff_slug": self.slug})
    
    # --------------------------------------
    
    def get_update_url(self):
        return reverse("barter:stuff-update", kwargs={"stuff_id": self.id, "stuff_slug": self.slug})
    
    # --------------------------------------
    
    def get_delete_url(self):
        return reverse("barter:stuff-delete", kwargs={"stuff_id": self.id, "stuff_slug": self.slug})
    
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
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        
        # generate url address of barter object
        current_site = Site.objects.get_current()
        self.url_address = str(current_site) + self.get_absolute_url()
                
        # create QRcode based on generated url address
        qr_text = self.url_address
        qr_image = qrcode.make(qr_text, box_size=25)
        qr_image_pil = qr_image.get_image()
        stream = BytesIO()
        qr_image_pil.save(stream, format="PNG")
        file_name = f"{self.slug}-{qr_text}.png"
        self.qrcode_image.save(file_name, File(stream), save=False)
        
        print(f"qr image is : {self.qrcode_image}")
        
        super().save(*args, **kwargs)
    
    # --------------------------------------
    