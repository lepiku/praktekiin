from django import forms
from django.core.validators import RegexValidator

class CreateUserForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^(\+62|0)\d{9,15}$', \
            message="Phone number must be entered in the format: \
                    '+628...' or '08...'. Up to 15 digits allowed.")
    nama = forms.CharField(label='Nama Lengkap', max_length=128)
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())
    no_hp = forms.CharField(validators=[phone_regex], max_length=18)
    # TODO username, password, no hp
