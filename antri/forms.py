from django import forms

class CreateUserForm(forms.Form):
    nama = forms.CharField(label='Nama Lengkap', max_length=128)
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())
    # TODO username, password, no hp
