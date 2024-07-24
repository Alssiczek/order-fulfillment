from django import forms
from .models import Order
from django.contrib.auth.forms import AuthenticationForm


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['part_no', 'serial_number']
        labels = {
            'part_no': 'Nr. Produktu',
            'serial_number': 'Numer Seryjny',
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Login",
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Hasło",
        strip=False,
        widget=forms.PasswordInput
    )