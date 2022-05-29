from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='symbols', null=False)
    symbol = models.CharField(max_length=5, null=False)

    class Meta:
        unique_together = ("user", "symbol")

    def __str__(self):
        return self.symbol
