from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import get_template


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.GROUP_NAME = "user-notifications"
        # self.channel_name unique for each consumer(client)

        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.GROUP_NAME, self.channel_name)

    def user_joined(self, event):
        html = get_template("core/partials/notification.html").render(
            context={"username": event["text"]}
        )
        self.send(text_data=event["text"])
        self.send(text_data=html)
