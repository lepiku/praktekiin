from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .models import REGEX_TELP, JENIS_KELAMIN

class DaftarPenggunaForm(forms.Form):
    nama = forms.CharField(label='Nama Lengkap', max_length=128)
    tanggal_lahir = forms.DateField()
    jenis_kelamin = forms.ChoiceField(choices=JENIS_KELAMIN)
    telp = forms.CharField(label='No. HP / Telp', validators=[REGEX_TELP],
            max_length=18)
    nama_kk = forms.CharField(label='Nama Kepala Keluarga', max_length=128)

    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())
    ulangi_password = forms.CharField(widget=forms.PasswordInput())

    def clean_nama(self):
        return str.title(self.data.get('nama'))

    def clean_nama_kk(self):
        return str.title(self.data.get('nama_kk'))

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
        if password != ulangi_password:
            raise forms.ValidationError('Password tidak sama.')
        return ulangi_password

class DaftarKKForm(forms.Form):
    nama = forms.CharField(widget=forms.HiddenInput)
    tanggal_lahir = forms.DateField(widget=forms.HiddenInput)
    jenis_kelamin = forms.ChoiceField(widget=forms.HiddenInput,
            choices=JENIS_KELAMIN)
    telp = forms.CharField(widget=forms.HiddenInput)
    username = forms.CharField(widget=forms.HiddenInput)
    password = forms.CharField(widget=forms.HiddenInput)
    ulangi_password = forms.CharField(widget=forms.HiddenInput)

    nama_kk = forms.CharField(label='Nama Kepala Keluarga', max_length=128)
    alamat = forms.CharField(label='Alamat', max_length=256,
            widget=forms.Textarea)

class MasukForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())
