from django.contrib import admin

from .models import Event, EventHour, Subevent


class EventHourInline(admin.TabularInline):
    model = EventHour


class SubeventInline(admin.TabularInline):
    model = Subevent


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("pk", "hidden", "facebook_id", "name", "description", "image")
    inlines = (SubeventInline, EventHourInline,)


@admin.register(EventHour)
class EventHourAdmin(admin.ModelAdmin):
    list_display = ("event", "time")


@admin.register(Subevent)
class SubeventAdmin(admin.ModelAdmin):
    list_display = ("event", "name")
