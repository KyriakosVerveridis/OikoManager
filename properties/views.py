from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Building, Apartment, Expense, MeterReading
from .serializers import BuildingSerializer, ApartmentSerializer, ExpenseSerializer, MeterReadingSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default CRUD actions for the Building model,
    along with a custom action to calculate bills for apartments in the building.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    @action(detail=True, methods=['get'])
    def calculate_bills(self, request, pk=None):
        """
        Custom action to calculate expenses per apartment based on square meters.
        """
        building = self.get_object()
        apartments = building.apartments.all()
        expenses = building.expenses.all()

        # Calculate total expense amount and total building square meters
        # Uses Django aggregation for database efficiency
        total_expense_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_sq_meters = apartments.aggregate(Sum('sq_meters'))['sq_meters__sum'] or 1

        results = []
        for apt in apartments:
            # Formula: (Apartment Sqm / Total Building Sqm) * Total Expenses
            share = (apt.sq_meters / total_sq_meters) * total_expense_amount
            
            results.append({
                "apartment_number": apt.number,
                "sq_meters": float(apt.sq_meters),
                "share_amount": round(float(share), 2)
            })

        return Response({
            "building_name": building.name,
            "total_expenses": float(total_expense_amount),
            "total_sq_meters": float(total_sq_meters),
            "bills": results
        })


class ApartmentViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default CRUD actions for the Apartment model.
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default CRUD actions for the Expense model.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class MeterReadingViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default CRUD actions for the MeterReading model.
    """
    queryset = MeterReading.objects.all()
    serializer_class = MeterReadingSerializer    