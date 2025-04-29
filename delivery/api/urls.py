from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..api.views import AddressViewSet, DriverViewSet, ServiceViewSet, ServiceRequestView, ServiceCompleteView

router = DefaultRouter()
router.register(r'addresses', AddressViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/service-request/', ServiceRequestView.as_view(), name='service-request'),
    path('api/service-complete/<int:pk>/', ServiceCompleteView.as_view(), name='service-complete'),
]
