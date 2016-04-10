import arrow
import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Event, EventHour
from .utils import get_graph


@login_required
def list_events(request):
    events = []
    eloader = get_graph(request.user).get_connections(id="me", connection_name="events")
    try:
        while True:
            events += eloader["data"]
            if len(eloader["data"]) < 25:
                break
            eloader = requests.get(eloader["paging"]["next"]).json()
    except KeyError:
        pass
    for event in events:
        ensure_event_import(get_graph(request.user), event["id"])
    allev = Event.objects.filter(facebook_id__in=[int(event["id"]) for event in events]).exclude(hidden=True).order_by(
        "start_time", "end_time", "?")
    return render(request, "plansza/list_events.html",
                  {"events": allev, "upcoming": allev.filter(start_time__gt=timezone.now()),
                   "ongoing": allev.filter(start_time__lte=timezone.now(), end_time__gte=timezone.now())})


def logout_page(request):
    logout(request)
    return redirect("landing_page")


@require_POST
@login_required
def change_status(request, ident):
    hour = get_object_or_404(EventHour, pk=int(ident))
    if "action" in request.POST:
        if request.POST["action"] == "put":
            hour.users.add(request.user)
        if request.POST["action"] == "delete":
            hour.users.remove(request.user)
    return redirect("event_details", ident=hour.event.facebook_id)


@login_required
def event_details(request, ident: str):
    ensure_event_import(get_graph(request.user), ident)
    event = get_object_or_404(Event, facebook_id=int(ident))
    return render(request, "plansza/event_details.html", {"event": event})


def landing_page(request):
    return render(request, "plansza/landing_page.html")


def ensure_event_import(graph, ident: str):
    # TODO: maybe we could make that threaded
    try:
        Event.objects.get(facebook_id=int(ident))
    except Event.DoesNotExist:
        event = graph.get_object(id=ident)
        image = graph.get_connections(id=ident, connection_name="picture", type="large")
        Event.objects.create(name=event["name"], description=event["description"], facebook_id=int(event["id"]),
                             facebook_data=event, image=(
                image["url"] if "url" in image else requests.head(
                    "https://source.unsplash.com/category/people/1500x550",
                    allow_redirects=True).url),
                             start_time=arrow.get(event["start_time"]).datetime,
                             end_time=arrow.get(event.get("end_time", event["start_time"])).datetime,
                             hidden=(event["start_time"] == event.get("end_time", event["start_time"])))
