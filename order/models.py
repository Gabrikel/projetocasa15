from product.models import Product
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import ProtectedError
from localflavor.br.models import BRCPFField, BRPostalCodeField, BRStateField
from model_utils.models import TimeStampedModel

from account.models import UserBase
from product.models import Product

class Order(TimeStampedModel):
    user = models.ForeignKey(UserBase, related_name="orders", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, default="", related_name="orders", on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def get_total_price(self):
        return self.product.get_total_price()
    