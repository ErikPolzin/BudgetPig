from django.urls import path

from . import views

app_name = 'budget'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', views.home, name='home'),
    path('<int:year>/<int:month>/set-budget', views.set_budget, name="set_budget"),
    path('add-expense', views.add_expense, name="add_expense")
]
