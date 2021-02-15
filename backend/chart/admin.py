from django.contrib import admin

# Register your models here.
from .models import Company, RawPrices

admin.site.register(Company)
admin.site.register(RawPrices)
