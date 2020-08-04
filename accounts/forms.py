from django import forms
from .models import *
from django.db import transaction

class UserSignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )
    class Meta:
        model = User
        fields = ('email','first_name','last_name','phone')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user