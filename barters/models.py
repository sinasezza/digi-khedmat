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


class StuffImage(models.Model):
    def stuff_image_path(instance, filename):
        file_path = pathlib.Path(filename)
        new_filename = str(uuid.uuid1())
        return f"stuff/imgs/{new_filename}{file_path.suffix}"
    
    title = models.CharField(max_length=40, null=True, blank=True, verbose_name="عنوان")
    image = models.ImageField(max_length=255, upload_to=stuff_image_path, verbose_name="تصویر")
    
# ================================================

class BarterAdvertising(generics_models.BaseAdvertisingModel):  
    def stuff_qrcode_path(instance, filename):
        new_filename = str(uuid.uuid1())
        return f"stuff/qrcodes/{new_filename}.png"
    
    # --------------------------------------
    owner = models.ForeignKey(to=Account, null=False, blank=False, on_delete=models.CASCADE, verbose_name="مالک")
    # --------------------------------------
    images = models.ManyToManyField(StuffImage, related_name="barters", blank=True, verbose_name="تصاویر")
    # --------------------------------------
    qrcode_image = models.ImageField(max_length=255, upload_to=stuff_qrcode_path, blank=True, null=True, verbose_name="بارکد آگهی")
    # --------------------------------------
    
    class Meta:
        default_related_name = "barters"

    # --------------------------------------
    
    def get_absolute_url(self):
        return reverse("barters:stuff-detail", kwargs={"stuff_id": self.id, "stuff_slug": self.slug})
    
    # --------------------------------------
    
    def get_update_url(self):
        return reverse("barters:stuff-update", kwargs={"stuff_id": self.id, "stuff_slug": self.slug})
    
    # --------------------------------------
    
    def get_delete_url(self):
        return reverse("barters:stuff-delete", kwargs={"stuff_id": self.id, "stuff_slug": self.slug})
    
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
                
        super().save(*args, **kwargs)
    
    # --------------------------------------
    