from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Expense


class ExpenseForm(ModelForm):

    class Meta:
        model = Expense
        fields = ("date", "description", "amount", "category")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'budget:add_expense'
        self.helper.layout.append(Submit('save', 'Add'))
