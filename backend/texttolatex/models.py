from django.db import models

# Create your models here.
class Convert(models.Model):
	picture = models.ImageField(upload_to='images/',default="")
	identifier = models.CharField(max_length=100)