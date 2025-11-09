from django.core.cache import cache
from ip2geotools.databases.noncommercial import DbIpCity
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")

        # Blocked IP check
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Geo lookup with cache
        geo = cache.get(ip)
        if not geo:
            try:
                resp = DbIpCity.get(ip, api_key="free")
                geo = {"country": resp.country, "city": resp.city}
            except:
                geo = {"country": None, "city": None}
            cache.set(ip, geo, 60 * 60 * 24)

        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=geo["country"],
            city=geo["city"]
        )

        return self.get_response(request)
