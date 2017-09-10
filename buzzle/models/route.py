

class Route:
    def __init__(self, method: str, path: str, handler: callable):
        self.method = method
        self.path = path
        self.handler = handler


class Resource:
    def __init__(self, path: str, route: Route):
        self.path = path
        self.route = route
