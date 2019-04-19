
from django.utils.deprecation import MiddlewareMixin
class CorsMiddleware(MiddlewareMixin):
    def process_response(self, req, resp):
        resp["access-control-allow-origin"] = "*"
        resp["access-control-allow-headers"] = "Origin"
        resp["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
        return resp