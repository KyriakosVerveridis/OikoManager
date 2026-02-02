from django.urls import path
from .views import BuildingList, ApartmentList, ExpenseList, MeterReadingList

urlpatterns = [
    path('buildings/', BuildingList.as_view(), name='building-list'),
    path('apartments/', ApartmentList.as_view(), name='apartment-list'),
    path('expenses/', ExpenseList.as_view(), name='expense-list'),
    path('meter-readings/', MeterReadingList.as_view(), name='meter-reading-list'),
]