from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TestimonialViewSet, FAQCategoryViewSet, FAQViewSet,
    TransferViewSet, AgentViewSet, CurrencyViewSet,
    NotificationViewSet, ReferralViewSet
)

router = DefaultRouter()
router.register(r'testimonials', TestimonialViewSet)
router.register(r'faq-categories', FAQCategoryViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'transferts', TransferViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'currencies', CurrencyViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'referrals', ReferralViewSet)

urlpatterns = [
    path('', include(router.urls)),
]