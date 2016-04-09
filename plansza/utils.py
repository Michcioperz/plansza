import facebook


def get_graph(user) -> facebook.GraphAPI:
    return facebook.GraphAPI(access_token=user.social_auth.get().access_token)


