from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import FinanceMovements




@receiver(pre_delete, sender=FinanceMovements)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        file_path = instance.file.path
        if default_storage.exists(file_path):
            default_storage.delete(file_path)


@receiver(pre_save, sender=FinanceMovements)
def delete_old_file_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance= FinanceMovements.objects.get(pk=instance.pk)
        
            if old_instance.file and old_instance.file != instance.file:
                old_file_path = old_instance.file.path
                if default_storage.exists(old_file_path):
                    default_storage.delete(old_file_path)
        except FinanceMovements.DoesNotExist():
            pass