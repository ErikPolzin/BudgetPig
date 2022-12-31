from datetime import date
from itertools import groupby
import json

from djmoney.money import Money
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, ExpenseCategory, MonthlyBudget
from .forms import ExpenseForm


@login_required
def index(request: HttpRequest) -> HttpResponse:
    now = timezone.now().date()
    return redirect("budget:home", year=now.year, month=now.month)


@login_required
def home(request: HttpRequest, year: int, month: int) -> HttpResponse:
    # Determine previous and next month dates
    if month == 1:
        prev_date = date(year=year-1, month=12, day=1)
    else:
        prev_date = date(year=year, month=month-1, day=1)
    if month == 12:
        next_date = date(year=year+1, month=1, day=1)
    else:
        next_date = date(year=year, month=month+1, day=1)
    # Group expenses by category, for the pie chart
    expenses = Expense.objects \
        .filter(user=request.user, date__month=month, date__year=year) \
        .order_by("-date")
    expenses_sorted = sorted(expenses, key=lambda e: e.category.name if e.category else "Unknown")
    expenses_by_category = []
    for (cat, catexpenses) in groupby(expenses_sorted, key=lambda e: e.categoryName()):
        expenses_by_category.append((cat, float(sum(e.amount for e in catexpenses).amount)))
    expenses_by_category.sort(key=lambda i: i[1], reverse=True)  # Sort by total amount
    # Calculate percentage of monthly budget reached
    monthly_budget = None
    budgets = MonthlyBudget.objects \
        .filter(user=request.user, date__lte=timezone.now()) \
        .order_by("-date")
    if budgets.exists():
        budget = budgets.first()
        if budget:
            monthly_budget = budget.amount
    total_spend = sum(e.amount for e in expenses)
    if monthly_budget is None:
        budget_percentage = 100
    elif total_spend == 0:
        budget_percentage = 0
    else:
        budget_percentage = round(total_spend / monthly_budget * 100)
    context = {
        "expenses": expenses,
        "total_spend": total_spend,
        "budget_percentage": budget_percentage,
        "budget": monthly_budget,
        "data": json.dumps({
            "categories": [i[0] for i in expenses_by_category],
            "amounts": [i[1] for i in expenses_by_category]
        }),
        "categories": ExpenseCategory.objects.all(),
        "today": timezone.now().date().isoformat(),
        "expense_form": ExpenseForm(),
        "prev_date": prev_date,
        "next_date": next_date,
        "current_date": date(year=year, month=month, day=1),
    }
    return render(request, 'budget/index.html', context)


@login_required
def add_expense(request: HttpRequest) -> HttpResponse:
    ex = ExpenseForm(request.POST).save(commit=False)
    ex.user = request.user
    ex.save()
    return HttpResponseRedirect(reverse("budget:index"))


@login_required
def set_budget(request: HttpRequest, year: int, month: int) -> HttpResponse:
    existing_budgets = MonthlyBudget.objects.filter(
        user=request.user, date__month=month, date__year=year)
    existing_budgets.delete()
    new_budget_amt = request.POST["amount"]
    new_budget_currency = request.POST["currency"]
    month_date = date(year=year, month=month, day=1)
    amt = Money(new_budget_amt, new_budget_currency)
    MonthlyBudget.objects.create(date=month_date, amount=amt, user=request.user)
    return HttpResponseRedirect(reverse("budget:index"))
