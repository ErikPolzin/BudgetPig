from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from djmoney.models.fields import MoneyField
from colorfield.fields import ColorField


class ExpenseCategory(models.Model):
    """Category for various expenses."""

    name = models.CharField(max_length=50)
    color = ColorField(default='#FF0000')

    def __str__(self) -> str:
        return f"Category: {self.name}"


class Expense(models.Model):
    """Expense of a certain amount."""

    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(ExpenseCategory, blank=True, null=True, on_delete=models.SET_NULL)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency="ZAR")
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Expense: {self.amount} on {self.date} ({self.description})"


class MonthlyBudget(models.Model):
    """Monthly budget goal."""

    date = models.DateField()
    amount = MoneyField(max_digits=14, decimal_places=0, default_currency="ZAR")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
