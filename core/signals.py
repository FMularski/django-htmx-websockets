from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def send_notifications_on_signup(sender, instance, created, **kwargs):
    if created:
        # notify all users in the 'user-notification' group

        # 1. get channel layer outside of a consumer with get_channel_layer
        channel_layer = get_channel_layer()
        # 2. specify event: name of a function in consumers.py and additional payload
        event = {"type": "user_joined", "text": instance.username}
        # 3. convert async method group_send to a sync method and pass the group name and the event
        async_to_sync(channel_layer.group_send)("user-notifications", event)
