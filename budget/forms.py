from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Expense


class NewExpenseForm(ModelForm):
    """Form for creating new expenses."""

    class Meta:
        model = Expense
        fields = ("date", "description", "amount", "category")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'budget:expenses'
        self.helper.layout.append(Submit('save', 'Save'))


class EditExpenseForm(ModelForm):
    """Form for editing expense objects."""

    class Meta:
        model = Expense
        fields = ("date", "description", "amount", "category")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Apply'))
