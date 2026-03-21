# api/health.py
from django.http import HttpResponse
from django.views.decorators.http import require_safe   # or require_GET


@require_safe  # Allows GET & HEAD only (good for health checks)
def health_check( request ):
    return HttpResponse( status=200 )