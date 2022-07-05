from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save

from picture_api import settings

import os
from uuid import uuid4

def path_and_rename(instance, filename):
    """
    Rename input files to random UUID string
    """
    upload_to = 'pictures'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

class Picture(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    image = models.ImageField(
        upload_to=path_and_rename,
        max_length=254
    )

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(Picture,self).delete(*args,**kwargs)

@receiver(pre_save, sender=Picture)
def purge_picture(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(id=instance.id)
        os.remove(old_instance.image.path)
    except sender.DoesNotExist:
        pass
