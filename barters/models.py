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
from generics import models as generics_models
from accounts.models import Account


class BarterAdvertising(generics_models.BaseAdvertisingModel):  
    def barter_qrcode_path(instance, filename):
        new_filename = str(uuid.uuid1())
        return f"barter/qrcodes/{new_filename}.png"
    
    # --------------------------------------
    owner = models.ForeignKey(to=Account, related_name="barters", on_delete=models.CASCADE, verbose_name="مالک")
    # --------------------------------------
    qrcode_image = models.ImageField(max_length=255, upload_to=barter_qrcode_path, blank=True, null=True, verbose_name="بارکد آگهی")
    # --------------------------------------
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="آدرس")
    # --------------------------------------
    region  = models.ForeignKey(to=generics_models.Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='barters', verbose_name="منطقه")
    # --------------------------------------
    categories = models.ManyToManyField(to=generics_models.StuffCategory, blank=True, related_name='barters', verbose_name='دسته بندی')
    # --------------------------------------
    tags = models.ManyToManyField(generics_models.Tag, blank=True, related_name='barters', verbose_name="تگ")
    # --------------------------------------
    
    class Meta:
        ordering = ("-date_published",)
        default_related_name = "barters"

    # --------------------------------------
    
    def __str__(self) -> str:
        return f"{self.slug}"
    
    # --------------------------------------
    
    def get_absolute_url(self):
        return reverse("barters:barter-detail", kwargs={"barter_slug": self.slug})
    
    # --------------------------------------
    
    def get_edit_url(self):
        return reverse("barters:barter-update", kwargs={"barter_slug": self.slug})
    
    # --------------------------------------
    
    def get_delete_url(self):
        return reverse("barters:barter-delete", kwargs={"barter_slug": self.slug})
    
    # --------------------------------------
    
    def update_categories(self, categories):
        self.categories.set(categories)
        super().save()
    
    # --------------------------------------
    
    def update_tags(self, tags):
        self.tags.set(tags)
        super().save()
    
    # --------------------------------------
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.slug = f"{self.id}-{slugify(value=self.title, allow_unicode=True)}"
        
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
                
        super().save(*args, **kwargs)
    
    # --------------------------------------

# ================================================
class BarterImage(models.Model):
    def barter_image_path(instance, filename):
        file_path = pathlib.Path(filename)
        new_filename = str(uuid.uuid1())
        return f"barters/imgs/{new_filename}{file_path.suffix}"
    # --------------------------------------------
    title = models.CharField(max_length=40, null=True, blank=True, verbose_name="عنوان")
    # --------------------------------------------
    image = models.ImageField(max_length=255, upload_to=barter_image_path, verbose_name="تصویر")
    # --------------------------------------------
    barter_advertising = models.ForeignKey(to=BarterAdvertising, on_delete=models.CASCADE, null=True, blank=True, related_name='images', verbose_name="آگهی تهاتر کالا")

    
    def __str__(self):
        return f"{self.id}> {self.barter_advertising}>{self.title}"
    