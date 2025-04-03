from django import forms 
from .models import FbUser


class SignUpForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=(("Male","Male"),("Female","Female")), required=True)
    class Meta:
        model = FbUser
        fields = ["first_name","last_name","date_of_birth","gender","email","password"]
        widgets = {"password":forms.PasswordInput,"date_of_birth":forms.SelectDateWidget(years=range(1900,2025))}


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)