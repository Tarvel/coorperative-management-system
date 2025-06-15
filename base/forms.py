from django.forms import ModelForm, BooleanField
from .models import User, Member, Transaction, Loan
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    is_staff = BooleanField(required=False, label="Register as staff?")

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "is_staff"]


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "type"]
