from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .Utils import verify_symbol


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SubscriptionForm(forms.Form):
    symbol = forms.CharField(max_length=5)

    def clean_symbol(self):
        ticker = self.cleaned_data.get("symbol")
        if verify_symbol(ticker):
            return ticker
        else:
            raise forms.ValidationError('Not a valid symbol')
