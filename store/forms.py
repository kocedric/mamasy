# coding=utf-8
from store.models import *
from django import forms
from django.forms import ModelForm


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "First Name",
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Last Name",
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Address de Livraison",
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Email",
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Mot de passe",
                }
            ),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['address', 'mobile', 'gender', 'profile_pic']
        widgets = {
            'gender': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Address de Livraison",
                }
            ),
            'mobile': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Phone",
                }
            ),
            'profile_pic': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Votre image de profile",
                }
            ),

        }


class RegisterFormUpdate(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# class AddAddress(ModelForm):
#     class Meta:
#         model = Address
#         fields = ['gender', 'first_name', 'last_name', 'address', 'phone']
#         widgets = {
#             'gender': forms.NullBooleanSelect(
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#             'first_name': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#             'last_name': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#             'address': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#             'phone': forms.TextInput(
#                 attrs={
#                     'class': 'form-control',
#                 }
#             ),
#         }
