from django.db import models
from model_utils.models import TimeStampedModel

class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    is_available = models.BooleanField(default=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_total_price(self):
        return self.price
