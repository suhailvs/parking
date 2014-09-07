from django.contrib import admin

# Register your models here.
from homepage.models import Parking,Weeks,User,Order
admin.site.register(Weeks)
admin.site.register(Parking)
admin.site.register(User)

admin.site.register(Order)