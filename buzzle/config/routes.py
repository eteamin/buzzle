from buzzle.models.route import Route
from buzzle.controllers.content import post


def routes():
    # Declare application routes here
    return [
        Route('POST', '/api/content', post)
    ]
