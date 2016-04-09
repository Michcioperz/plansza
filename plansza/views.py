import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Event
from .utils import get_graph


@login_required
def list_events(request):
    events = get_graph(request.user).get_connections(id="me", connection_name="events")["data"]
    for event in events:
        ensure_event_import(get_graph(request.user), event["id"])
    return render(request, "plansza/list_events.html", {"events": events})


@login_required
def event_details(request, ident: str):
    ensure_event_import(get_graph(request.user), ident)
    event = get_object_or_404(Event, facebook_id=int(ident))
    return render(request, "plansza/event_details.html", {"event": event})


def landing_page(request):
    return render(request, "plansza/landing_page.html")


def ensure_event_import(graph, ident: str):
    try:
        Event.objects.get(facebook_id=int(ident))
    except Event.DoesNotExist:
        event = graph.get_object(id=ident)
        image = graph.get_connections(id=ident, connection_name="picture", type="large")
        Event.objects.create(name=event["name"], description=event["description"], facebook_id=int(event["id"]),
                             facebook_data=event, image=(
            image["url"] if "url" in image else requests.head("https://source.unsplash.com/category/people/1500x550",
                                                              allow_redirects=True).url))
