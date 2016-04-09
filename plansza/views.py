import facebook
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def list_events(request):
    events = \
    facebook.GraphAPI(request.user.social_auth.get().access_token).get_connections(id="me", connection_name="events")[
        "data"]
    return render(request, "plansza/list_events.html", {"events": events})


@login_required
def event_details(request, ident):
    return HttpResponse("ej cześć siema tu nic nie ma")
