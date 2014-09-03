from django.contrib import admin

# Register your models here.
from homepage.models import Orders,Parking,Weeks,User
admin.site.register(Weeks)
admin.site.register(Parking)
admin.site.register(Orders)
admin.site.register(User)