from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser



class MyUser(AbstractUser):
    licenseplate = models.CharField(max_length=10, blank=True)
    state=models.CharField(max_length=2)