from django import forms
from .models import FbUser
from django.core.validators import MinLengthValidator,validate_email
from .validators import usernameoremailvalidator
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import ASCIIUsernameValidator

class SignUpForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=(("Male", "Male"), ("Female", "Female")), required=True
    )
    password = forms.CharField(widget=forms.PasswordInput,)
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={'placeholder':'Email'}))
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':"First Name"}))
    last_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':"Last Name"}))
    date_of_birth = forms.SelectDateWidget(years=range(1900,2025))
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':"Username"}))
    password = forms.CharField(label="",widget = forms.PasswordInput(attrs={'placeholder':"Password"}))
    class Meta:
        model = FbUser
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "email",
            "username",
            "password",
        ]
        widgets = {
            "date_of_birth": forms.SelectDateWidget(years=range(1900, 2025)),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


    def clean_password(value):
        if len(value.cleaned_data["password"])<8:
            raise ValidationError("password must be atleast 8 characters long1")
        else:
            return value.cleaned_data["password"]

    # def clean_email(value):
    #     unoremail = value.cleaned_data["email"]
    #     try:
    #         validate_email(unoremail)
    #     except ValidationError:
    #         try:
    #             ASCIIUsernameValidator(unoremail)
    #             return unoremail
    #         except:
    #             raise ValidationError("Please enter a valid username or email")

class LoginForm(forms.Form):
    email = forms.CharField(label="",widget=forms.TextInput(attrs={"placeholder":"Email or Username","class":"email-input-field"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"password-input-field"}))

