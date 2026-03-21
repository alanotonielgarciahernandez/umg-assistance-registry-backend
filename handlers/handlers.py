from django.urls import path

from routers.health import health_check

urlpatterns = [
    path( 'health', health_check, name='health' ),
]