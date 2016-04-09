from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class EventHour(models.Model):
    event = models.ForeignKey(Event, related_name="hours")
    users = models.ManyToManyField(User, related_name="hours")
