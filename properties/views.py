from rest_framework import generics
from .models import Building, Apartment, Expense, MeterReading
from .serializers import BuildingSerializer, ApartmentSerializer, ExpenseSerializer, MeterReadingSerializer

class BuildingList(generics.ListCreateAPIView):
    """
    API endpoint that allows buildings to be viewed or created.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class ApartmentList(generics.ListCreateAPIView):
    """
    API endpoint that allows apartments to be viewed or created.
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


class ExpenseList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating expenses.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class MeterReadingList(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating meter readings.
    """
    queryset = MeterReading.objects.all()
    serializer_class = MeterReadingSerializer    