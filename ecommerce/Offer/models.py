from django.db import models

# Create your models here.
class Offers(models.Model):
    offer_name=models.CharField(max_length=50,unique=True)
    discout=models.IntegerField()

    def __str__(self):
        return self.offer_name
        