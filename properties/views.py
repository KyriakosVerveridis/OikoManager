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
        building = self.get_object()
        apartments = building.apartments.all()
        expenses = building.expenses.all()

        if not apartments.exists():
            return Response({"error": "No apartments found in this building."}, status=400)

        # 1. Split expenses into groups
        total_general = sum(e.amount for e in expenses if e.category not in ['heating', 'elevator'])
        total_heating = sum(e.amount for e in expenses if e.category == 'heating')
        total_elevator = sum(e.amount for e in expenses if e.category == 'elevator')

        # 2. Calculate denominators with safety checks
        total_sq_meters = sum(a.sq_meters for a in apartments)
        total_heating_coeff = sum(a.heating_coeff for a in apartments)
        total_elevator_coeff = sum(a.elevator_coeff for a in apartments)

        bills = []
        warnings = []

        # Check for zero denominators to avoid ZeroDivisionError
        if total_heating > 0 and total_heating_coeff == 0:
            warnings.append("Heating expenses exist but all apartments have 0 heating coefficient.")
        if total_elevator > 0 and total_elevator_coeff == 0:
            warnings.append("Elevator expenses exist but all apartments have 0 elevator coefficient.")

        for apt in apartments:
            # General Share (always based on sq_meters)
            share_general = (total_general * apt.sq_meters) / total_sq_meters if total_sq_meters > 0 else 0
            
            # Heating Share (safety check)
            share_heating = (total_heating * apt.heating_coeff) / total_heating_coeff if total_heating_coeff > 0 else 0
            
            # Elevator Share (safety check)
            share_elevator = (total_elevator * apt.elevator_coeff) / total_elevator_coeff if total_elevator_coeff > 0 else 0
            
            total_apt_bill = share_general + share_heating + share_elevator

            bills.append({
                "apartment_number": apt.number,
                "general_share": round(float(share_general), 2),
                "heating_share": round(float(share_heating), 2),
                "elevator_share": round(float(share_elevator), 2),
                "total_amount": round(float(total_apt_bill), 2)
            })

        return Response({
            "building_name": building.name,
            "total_expenses_all": float(total_general + total_heating + total_elevator),
            "warnings": warnings,
            "bills": bills
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