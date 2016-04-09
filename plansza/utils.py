import facebook
import requests

from .models import Event


def get_graph(user) -> facebook.GraphAPI:
    return facebook.GraphAPI(access_token=user.social_auth.get().access_token)


def ensure_event_import(graph, ident: str):
    try:
        Event.objects.get(facebook_id=int(ident))
    except Event.DoesNotExist:
        event = graph.get_object(id=ident)
        image = graph.get_connections(id=ident, connection_name="picture", type="large")
        Event.objects.create(name=event["name"], description=event["description"], facebook_id=int(event["id"]), image=(
            image["url"] if "url" in image else requests.head("https://source.unsplash.com/category/people/1500x550",
                                                              allow_redirects=True).url))
