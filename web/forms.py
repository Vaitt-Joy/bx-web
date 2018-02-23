# coding=utf-8
from django import forms

"""表单"""


class AccountForm(forms.Form):
    """form 表单"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'username', 'class': 'form-control', 'placeholder': 'Enter Your Account',
                                      'data-validate': 'required:Enter Your Account Please',
                                      'name': 'username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'id': 'password', 'class': 'form-control', 'name': 'password', 'placeholder': 'Enter Your Password',
               'data-validate': 'required:Enter Your Password Please'}))
