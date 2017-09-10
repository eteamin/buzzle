from buzzle.models.route import Route, Resource
from buzzle.controllers.content import post, get


def routes():
    # Declare application routes here
    return [
        Route('POST', '/api/contents', post)
    ]


def resources():
    return [
        Resource('/api/contents/{content_uid}', Route('GET', '/api/contents/', get)),
    ]