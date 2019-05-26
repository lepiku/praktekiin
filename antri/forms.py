from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .models import regex_telp

class DaftarPenggunaForm(forms.Form):
    JENIS_KELAMIN_CHOICES = (('l', 'Laki-Laki'), ('p', 'Perempuan'))

    nama = forms.CharField(label='Nama Lengkap', max_length=128)
    tanggal_lahir = forms.DateField(label='Tanggal Lahir')
    jenis_kelamin = forms.ChoiceField(label='Jenis Kelamin',
            choices=JENIS_KELAMIN_CHOICES)
    telp = forms.CharField(label='No. HP / Telp', validators=[regex_telp],
            max_length=18)
    nama_kk = forms.CharField(label='Nama Kepala Keluarga', max_length=128)

    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())
    ulangi_password = forms.CharField(widget=forms.PasswordInput())

    def clean_nama(self):
        return str.capitalize(self.data.get('nama'))

    # TODO cek kk udah ada apa blom? kalo udah, tanya itu sama gk?
    def clean_username(self):
        username = self.data.get('username')
        if User.objects.filter(username=username): # if username already exist
            raise forms.ValidationError('Username sudah dipakai.')
        elif len(username) < 3:
            raise forms.ValidationError('Username terlalu pendek. Minimal 3 karakter')
        return username

    def clean_password(self):
        password = self.data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('Password terlalu pendek. Minimal 6 karakter.')
        return password

    def clean_ulangi_password(self):
        password = self.data.get('password')
        ulangi_password = self.data.get('ulangi_password')
        print(password, " == ", ulangi_password)
        if password != ulangi_password:
            raise forms.ValidationError('Password tidak sama.')
        return ulangi_password

class DaftarKKForm(forms.Form):
    nama_kk = forms.CharField(label='Nama Kepala Keluarga', max_length=128)
    alamat = forms.TextInput()

class MasukForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())
