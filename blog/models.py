from django.db import models
from django.utils.text import slugify
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django_quill.fields import QuillField
from django.utils.html import strip_tags
import html
from django.utils.timezone import now
import os


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = QuillField()
    image = models.ImageField(upload_to='images/posts', blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='posts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    views_count = models.PositiveIntegerField(default=0)
    links = models.JSONField(blank=True, null=True)  # Store links as a list of dictionaries
    links_title = models.CharField(max_length=200, blank=True)  # Optional field for links title

    def get_plain_title(self):
        return strip_tags(self.title)

    def save(self, *args, **kwargs):
        try:
            this = Post.objects.get(id=self.id)
            if this.image and this.image != self.image:
                this.image.delete(save=False)
        except Post.DoesNotExist:
            pass  # New instance, so no previous image to delete

        # Set slug and short_description
        self.slug = slugify(self.title)

        if self.content:
            plain_text_content = html.unescape(strip_tags(str(self.content.html)))
            if not self.short_description or self.short_description[:130] != plain_text_content[:130]:
                self.short_description = plain_text_content[:130]


        # Optimize and save the image
        if self.image:
            img = Image.open(self.image)
            output = BytesIO()
            img_format = img.format
            img.save(output, format=img_format, quality=75)
            output.seek(0)

            # Re-assign the image file to prevent the recursive path issue
            image_name = self.image.name.split('/')[-1]  # Extract the base filename
            self.image = ContentFile(output.read(), name=image_name)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
    

def optimize_image(image_field, max_width=1200, quality=80):
    """
    Convert image to WEBP and resize if too large.
    """

    img = Image.open(image_field)

    if img.mode != "RGB":
        img = img.convert("RGB")

    if img.width > max_width:
        ratio = max_width / img.width

        new_height = int(img.height * ratio)

        img = img.resize(
            (max_width, new_height),
            Image.LANCZOS
        )

    output = BytesIO()

    img.save(
        output,
        format="WEBP",
        quality=quality,
        optimize=True
    )

    output.seek(0)

    filename = os.path.splitext(os.path.basename(image_field.name)
    )[0]

    return ContentFile(
        output.read(),
        name=f"{filename}.webp"
    )

class Business_line(models.Model):
    name = models.CharField(max_length=200)
    Category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='business_lines', null=True, blank=True)
    description = QuillField()
    image = models.ImageField(upload_to='images/business_lines', blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    views_count = models.PositiveIntegerField(default=0)
    business_services_title = models.CharField(max_length=200, blank=True)
    register_link = models.URLField(blank=True, null=True)
    register_link_title = models.CharField(max_length=200, blank=True)
    business_title = models.CharField(max_length=250, blank=True, null=True)
    businness_description_title = QuillField(blank=True, null=True)
    website_link = models.URLField(
        blank=True,
        null=True
    )
    website_link_title = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)

        if self.image:
            if not self.image.name.endswith(".webp"):
                self.image = optimize_image(
                    self.image,
                    max_width=1200,
                    quality=80
                )

        super().save(*args, **kwargs)

   

    def __str__(self):
        return self.name
    
class BusinessLineGallery(models.Model):
    business_line = models.ForeignKey(
        Business_line,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(
        upload_to="business_line_gallery/"
    )
    

    title = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if self.image:
            if not self.image.name.endswith(".webp"):
                self.image = optimize_image(
                    self.image,
                    max_width=1200,
                    quality=80
                )

        super().save(*args, **kwargs)

   

    def __str__(self):
        return self.business_line.name


class BusinessLineService(models.Model):
    business_line = models.ForeignKey(
        Business_line,
        on_delete=models.CASCADE,
        related_name='services'
    )

    name = models.CharField(max_length=200)
    business_link = models.URLField(blank=True, null=True)


    description = models.TextField()

    icon = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.name