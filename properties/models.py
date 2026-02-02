from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User Model (Για τα 3 επίπεδα χρηστών)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='manager')

# 2. Building Model
class Building(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# 3. Apartment Model
class Apartment(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='apartments')
    number = models.CharField(max_length=10)
    sq_meters = models.DecimalField(max_digits=6, decimal_places=2)
    heating_coeff = models.DecimalField(max_digits=5, decimal_places=4, default=0.0)
    elevator_coeff = models.DecimalField(max_digits=5, decimal_places=4, default=0.0)

    def __str__(self):
        return f"{self.building.name} - Apt {self.number}"

# 4. Expense Model
class Expense(models.Model):
    CATEGORY_CHOICES = (
        ('cleaning', 'Cleaning'),
        ('elevator', 'Elevator'),
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('repairs', 'Repairs'),
    )
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

# 5. Meter Reading Model
class MeterReading(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='readings')
    hours = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()