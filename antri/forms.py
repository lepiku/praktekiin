from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class CreateUserForm(forms.Form):
    regex_hp = RegexValidator(regex=r'^(\+62|0)\d{9,15}$', \
            message="Nomor Handphone harus mengikuti format: \
                    '+628...' or '08...' maksimal 15 digit.")
    nama = forms.CharField(label='Nama Lengkap', max_length=128)
    # TODO username, password, no hp
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())
    no_hp = forms.CharField(validators=[regex_hp], max_length=18)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username): # if username already exist
            raise forms.ValidationError('Username sudah dipakai.')
        else:
            return username
