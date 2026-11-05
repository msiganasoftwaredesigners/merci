from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


from .models import (
    Business_line,
    BusinessLineGallery,
)
@receiver(pre_save, sender=BusinessLineGallery)
def delete_old_gallery_image(sender, instance, **kwargs):

        if not instance.pk:
            return

        try:
            old = BusinessLineGallery.objects.get(pk=instance.pk)

            if old.image and old.image != instance.image:
                old.image.delete(save=False)

        except BusinessLineGallery.DoesNotExist:
            pass

@receiver(pre_save, sender=Business_line)
def delete_old_business_image(sender, instance, **kwargs):

        if not instance.pk:
            return

        try:
            old = Business_line.objects.get(pk=instance.pk)

            if old.image and old.image != instance.image:
                old.image.delete(save=False)

        except Business_line.DoesNotExist:
            pass

@receiver(post_delete, sender=Business_line)
def delete_business_image(sender, instance, **kwargs):

    if instance.image:
        instance.image.delete(save=False)


@receiver(post_delete, sender=BusinessLineGallery)
def delete_gallery_image(sender, instance, **kwargs):

    if instance.image:
        instance.image.delete(save=False)