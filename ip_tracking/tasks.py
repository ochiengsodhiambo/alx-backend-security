from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def flag_suspicious_ips():
    """
    Flags suspicious IPs:
    - More than 100 requests/hour
    - Accessed sensitive paths
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # 1. Flag IPs with >100 requests/hour
    heavy = logs.values('ip_address').annotate(count=Count('id')).filter(count__gt=100)
    for entry in heavy:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            reason=">100 requests/hour"
        )

    # 2. Flag IPs accessing sensitive paths
    sensitive_paths = ['/admin', '/login', '/login-public/', '/login-auth/']
    for log in logs.filter(path__in=sensitive_paths):
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f"Accessed {log.path}"
        )
