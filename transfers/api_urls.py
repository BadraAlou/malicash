from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransferViewSet

router = DefaultRouter()
router.register(r'transferts', TransferViewSet, basename='transfert')

urlpatterns = [
    path('', include(router.urls)),
]