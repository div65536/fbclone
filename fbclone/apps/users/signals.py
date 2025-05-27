from django.dispatch import Signal,receiver
from django.db.models.signals import pre_save
from users.models import FbUser

# bio_change_signal = Signal()

# @receiver(bio_change_signal)
# def handle_bio_change(sender, instance, **kwargs):
#     print("bio changed")


# @receiver(pre_save, sender=FbUser)
# def fire_bio_change_signal(sender, instance, **kwargs):

#     if not instance.pk:
#         return 
#     else:
#         old_instance = FbUser.objects.get(pk=instance.pk)
#         if old_instance.bio != instance.bio:
#             bio_change_signal.send(sender=sender,instance=instance)