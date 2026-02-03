from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Building, Expense

class PropertyAPITests(APITestCase):
    
    def setUp(self):
        # Create a building for ForeignKey dependencies
        self.building = Building.objects.create(
            name="Alpha Tower", 
            address="Test Street 10"
        )

    def test_create_expense(self):
        # Test creating a new expense with correct model fields
        url = reverse('expense-list')
        data = {
            "building": self.building.id,
            "category": "electricity",  # Must match CATEGORY_CHOICES
            "amount": 150.00,
            "date": "2026-02-03"        # Required field
        }
        response = self.client.post(url, data, format='json')
        
        # Professional tip: print errors if the test fails
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Errors: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)