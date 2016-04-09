import facebook
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Event


def get_graph(request):
    return facebook.GraphAPI(access_token=request.user.social_auth.get().access_token)


def ensure_event_import(request, ident):
    try:
        Event.objects.get(facebook_id=int(ident))
    except Event.DoesNotExist:
        event = get_graph(request).get_object(id=ident)
        image = get_graph(request).get_connections(id=ident, connection_name="picture", type="large")
        Event.objects.create(name=event["name"], description=event["description"], facebook_id=int(event["id"]), image=(
            image["url"] if "url" in image else requests.head("https://source.unsplash.com/category/people/1500x550",
                                                              allow_redirects=True).url))


@login_required
def list_events(request):
    events = get_graph(request).get_connections(id="me", connection_name="events")["data"]
    return render(request, "plansza/list_events.html", {"events": events})


@login_required
def event_details(request, ident):
    ensure_event_import(request, ident)
    event = get_object_or_404(Event, facebook_id=int(ident))
    return render(request, "plansza/event_details.html", {"event": event})


def landing_page(request):
    return render(request, "plansza/landing_page.html")
