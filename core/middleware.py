from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from datetime import timedelta
from .models import Visit
from .geoip_utils import get_location_from_ip

class UniqueVisitMiddleware(MiddlewareMixin):
    CACHE_TIME = timedelta(minutes=30)

    def process_request(self, request):
        exclude_paths = ['/admin/', '/static/', '/media/', '/api/']
        if any(request.path.startswith(ex) for ex in exclude_paths):
            return

        ip = self.get_client_ip(request)
        session_key = request.session.session_key
        now = timezone.now()

        recent_visit = Visit.objects.filter(
            ip_address=ip,
            created_at__gte=now - self.CACHE_TIME
        ).exists()

        if not recent_visit and session_key:
            city, country = get_location_from_ip(ip)
            Visit.objects.create(
                ip_address=ip,
                city=city,
                country=country,
                session_key=session_key,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip.strip()
