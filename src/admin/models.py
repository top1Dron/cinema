import os

from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver


class Mail(models.Model):
    email = models.FileField(upload_to='emails/', validators=[FileExtensionValidator(allowed_extensions=('html',))])
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email.url


attributes = ('email',)


@receiver(models.signals.post_delete, sender=Mail)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding sender object is deleted.
    """
    for attribute in attributes:
        if hasattr(instance, attribute):
            attr = getattr(instance, attribute)
            if attr:
                try:
                    if os.path.isfile(attr.path):
                        os.remove(attr.path)
                except ValueError:
                    pass


@receiver(models.signals.pre_save, sender=Mail)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding sender object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        sender_obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False
    old_file = new_file = None
    for attribute in attributes:
        if hasattr(sender_obj, attribute):
            old_file = getattr(sender_obj, attribute)
        if hasattr(instance, attribute):
            new_file = getattr(instance, attribute)

    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except ValueError as e:
            pass