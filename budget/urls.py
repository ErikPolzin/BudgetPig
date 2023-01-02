from django.urls import path

from . import views

app_name = 'budget'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', views.home, name='home'),
    path('<int:year>/<int:month>/set-budget', views.set_budget, name="set_budget"),
    path('expenses/', views.expenses, name="expenses"),
    path('expenses/<int:expense_id>', views.expense, name="expense")
]
