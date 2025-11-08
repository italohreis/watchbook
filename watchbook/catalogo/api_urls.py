from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ObraViewSet

router = DefaultRouter()
router.register(r'', ObraViewSet, basename='obra')

urlpatterns = [
    path('', include(router.urls)),
]
