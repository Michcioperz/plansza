import requests
from django.contrib.auth.models import User
from django.db import models


def get_random_photo():
    return requests.head("https://source.unsplash.com/people/1500x550", allow_redirects=True).url

class Event(models.Model):
    name = models.CharField(max_length=255)
    facebook_id = models.BigIntegerField(null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(default=get_random_photo)


class EventHour(models.Model):
    event = models.ForeignKey(Event, related_name="hours")
    users = models.ManyToManyField(User, related_name="hours")
