import facebook
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def get_graph(request):
    return facebook.GraphAPI(access_token=request.user.social_auth.get().access_token)

@login_required
def list_events(request):
    events = get_graph(request).get_connections(id="me", connection_name="events")["data"]
    return render(request, "plansza/list_events.html", {"events": events})


@login_required
def event_details(request, ident):
    event = get_graph(request).get_object(id=ident)
    return render(request, "plansza/event_details.html")
