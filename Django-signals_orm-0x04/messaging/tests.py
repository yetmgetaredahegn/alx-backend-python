from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='test')
        self.bob = User.objects.create_user(username='bob', password='test')

    def test_notification_created_on_message_send(self):
        Message.objects.create(sender=self.alice, receiver=self.bob, content='Hi!')
        notif = Notification.objects.filter(user=self.bob).first()

        self.assertIsNotNone(notif)
        self.assertIn('alice', notif.text)
