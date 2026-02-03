from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApartmentViewSet, BuildingViewSet, ExpenseViewSet, MeterReadingViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'buildings', BuildingViewSet)
router.register(r'apartments', ApartmentViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'meter-readings', MeterReadingViewSet)
urlpatterns = [
    # Router URLs include: list, create, retrieve, update, delete AND calculate_bills
    path('', include(router.urls)),
]