from django.contrib import admin
from .models import User, Building, Apartment, Expense, MeterReading

# Καταχώρηση των μοντέλων
admin.site.register(User)
admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(Expense)
admin.site.register(MeterReading)