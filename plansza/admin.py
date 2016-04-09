from django.contrib import admin

from .models import Event, EventHour


class EventHourInline(admin.StackedInline):
    model = EventHour


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("pk", "facebook_id", "name", "description", "image")
    inlines = (EventHourInline,)


@admin.register(EventHour)
class EventHourAdmin(admin.ModelAdmin):
    list_display = ("event",)
