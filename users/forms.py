from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    matricula = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    sexo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )


    sexo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )


    class Meta:
        model = User
<<<<<<< HEAD
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name' ,'is_client', 'is_admin','matricula','sexo','phone')
=======
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name' ,'is_client', 'is_admin','sexo','phone')
>>>>>>> origin





class editUserForm(forms.Form):

    username = forms.CharField( max_length=255, min_length=2, 
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    firstname = forms.CharField( max_length= 100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )


    def clean_username(self):
        username = self.cleaned_data['username']
        if username == "nombre":
            print("igual")
            ValidationError('""')
        else:
            print("no igual")
            return username

