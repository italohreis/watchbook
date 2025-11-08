from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import AmizadeViewSet

router = DefaultRouter()
router.register(r'', AmizadeViewSet, basename='amizade')

urlpatterns = [
    path('', include(router.urls)),
]
