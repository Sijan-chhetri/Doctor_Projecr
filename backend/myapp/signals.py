# myapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import VideoComment

@receiver(post_save, sender=VideoComment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        print(f"New comment created: {instance.comment_text}")
