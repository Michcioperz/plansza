import requests
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.db import models, transaction
from django.dispatch import receiver

from .utils import get_graph


def get_random_photo() -> str:
    return requests.head("https://source.unsplash.com/people/1500x550", allow_redirects=True).url


class Event(models.Model):
    name = models.CharField(max_length=255)
    facebook_id = models.BigIntegerField(null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(default=get_random_photo)


class EventHour(models.Model):
    event = models.ForeignKey(Event, related_name="hours")
    users = models.ManyToManyField(User, related_name="hours")


class Friend(models.Model):
    user = models.OneToOneField(User, related_name="friend")
    friends = models.ManyToManyField("self", symmetrical=True)

    def update(self):
        with transaction.atomic():
            # TODO: this may not work for more than 15 or so friends
            self.friends = [Friend.objects.get(user__social_auth__uid=x["id"]) for x in
                            get_graph(self.user).get_connections("me", "friends")["data"]]
            self.save()


@receiver(user_logged_in)
def friend_reroll(sender, request, user, **kwargs):
    try:
        f = user.friend
    except:
        f = Friend.objects.create(user=user)
    f.update()
