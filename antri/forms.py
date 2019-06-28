from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import REGEX_TELP, REGEX_NAMA, REGEX_ALAMAT, JENIS_KELAMIN, \
        NAME_LENGTH, KepalaKeluarga
import re
from django.contrib.auth import authenticate, get_user_model, \
        password_validation

class DateField(forms.DateField):
    input_formats = ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y']
    error_messages = {'invalid': 'Format tanggal: dd/mm/yyyy'}

class DaftarPenggunaForm(forms.Form):
    nama = forms.CharField(label='Nama Lengkap', max_length=NAME_LENGTH,
            validators=[REGEX_NAMA])
    tanggal_lahir = DateField()
    # TODO error meesage still 'Enter a valid date'
    jenis_kelamin = forms.ChoiceField(choices=JENIS_KELAMIN)
    telp = forms.CharField(label='No. HP / Telp', validators=[REGEX_TELP],
            max_length=18)
    nama_kk = forms.CharField(label='Nama Kepala Keluarga',
            max_length=NAME_LENGTH, validators=[REGEX_NAMA])

    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())
    ulangi_password = forms.CharField(widget=forms.PasswordInput())

    def clean_nama(self):
        nama = self.data.get('nama')
        return str.title(nama)

    def clean_nama_kk(self):
        nama_kk = self.data.get('nama_kk')
        return str.title(nama_kk)

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
        elif password in ['123456'] or password == password[0] * len(password):
            raise forms.ValidationError('Password terlalu mudah ditebak.')
        return password

    def clean_ulangi_password(self):
        password = self.data.get('password')
        ulangi_password = self.data.get('ulangi_password')
        if password != ulangi_password:
            raise forms.ValidationError('Password tidak sama.')
        return ulangi_password

class DaftarKKForm(forms.Form):
    nama = forms.CharField(widget=forms.HiddenInput)
    tanggal_lahir = DateField(widget=forms.HiddenInput)
    jenis_kelamin = forms.ChoiceField(widget=forms.HiddenInput,
            choices=JENIS_KELAMIN)
    telp = forms.CharField(widget=forms.HiddenInput)
    username = forms.CharField(widget=forms.HiddenInput)
    password = forms.CharField(widget=forms.HiddenInput)
    ulangi_password = forms.CharField(widget=forms.HiddenInput)

    nama_kk = forms.CharField(label='Nama Kepala Keluarga',
            max_length=NAME_LENGTH, validators=[REGEX_NAMA])
    alamat = forms.CharField(label='Alamat', max_length=256,
            widget=forms.Textarea, validators=[REGEX_ALAMAT])

    def clean_nama_kk(self):
        nama_kk = self.data.get('nama_kk')
        return str.title(nama_kk)

class PilihKKForm(forms.Form):
    nama = forms.CharField(widget=forms.HiddenInput)
    tanggal_lahir = DateField(widget=forms.HiddenInput)
    jenis_kelamin = forms.ChoiceField(widget=forms.HiddenInput,
            choices=JENIS_KELAMIN)
    telp = forms.CharField(widget=forms.HiddenInput)
    username = forms.CharField(widget=forms.HiddenInput)
    password = forms.CharField(widget=forms.HiddenInput)
    ulangi_password = forms.CharField(widget=forms.HiddenInput)
    nama_kk = forms.CharField(widget=forms.HiddenInput)

    # TODO get data from last post
    def __init__(self, *args, **kwargs):
        nama_kk = kwargs.pop('nama_kk', '')
        super().__init__(*args, **kwargs)

        self.fields['kk'] = forms.ModelChoiceField(
                KepalaKeluarga.objects.filter(nama=nama_kk),
                label='Kepala Keluarga')

class PendaftarForm(forms.Form):
    pendaftar = forms.CharField(required=False, widget=forms.Textarea)

    def clean_pendaftar(self):
        pendaftar = self.data.get('pendaftar')
        return str.title(pendaftar)

class UbahPasswordForm(PasswordChangeForm):
    error_messages = {
        **PasswordChangeForm.error_messages,
        'password_incorrect': "Password lama salah",
    }

    old_password = forms.CharField(
            label="Password Lama",
            strip=False,
            widget=forms.PasswordInput(attrs={'autofocus': True}),
            )
    new_password1 = forms.CharField(
            label="Password Baru",
            widget=forms.PasswordInput,
            strip=False,
            )
    new_password2 = forms.CharField(
            label="Ulangi Password Baru",
            strip=False,
            widget=forms.PasswordInput,
            )

    def clean_new_password1(self):
        password = self.data.get('new_password1')
        if len(password) < 6:
            raise forms.ValidationError('Password terlalu pendek. Minimal 6 karakter.')
        elif password in ['123456'] or password == password[0:1] * len(password):
            raise forms.ValidationError('Password terlalu mudah ditebak.')
        return password

    def clean_new_password2(self):
        password1 = self.data.get('new_password1')
        password2 = self.data.get('new_password2')
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
