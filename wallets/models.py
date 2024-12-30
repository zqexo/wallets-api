from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)

    def __str__(self):
        return self.uuid

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"
