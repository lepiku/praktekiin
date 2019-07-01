from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import REGEX_TELP, REGEX_NAMA, REGEX_ALAMAT, JENIS_KELAMIN, \
        NAME_LENGTH, Pengguna, KepalaKeluarga
import re
from django.contrib.auth import authenticate, get_user_model, \
        password_validation

class DateField(forms.DateField):
    input_formats = ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y']
    error_messages = {'invalid': 'Format tanggal: dd/mm/yyyy'}

class PenggunaForm(forms.ModelForm):
    class Meta:
        model = Pengguna
        fields = ('nama', 'tanggal_lahir', 'jenis_kelamin', 'telp', 'nik')

class KepalaKeluargaForm(forms.ModelForm):
    class Meta:
        model = KepalaKeluarga
        fields = ('nama_kk', 'alamat_kk', 'no_kk')

class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,
        help_text='Password jangan terlalu gampang',
    )
    password2 = forms.CharField(
        label='Konfirmasi Password',
        strip=False,
        widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification.',
    )

    # disable password verification
    def _post_clean(self):
        super(forms.ModelForm, self)._post_clean()

class DaftarPenggunaForm(forms.Form):
    nama = forms.CharField(label='Nama Lengkap', max_length=NAME_LENGTH)
    tanggal_lahir = DateField()
    jenis_kelamin = forms.ChoiceField(choices=JENIS_KELAMIN)
    email = forms.CharField(required=False)
    telp = forms.CharField(label='No. HP / Telp', max_length=18, required=False)
    nik = forms.CharField(label='NIK', max_length=16, required=False)
    nama_kk = forms.CharField(label='Nama Kepala Keluarga',
            max_length=NAME_LENGTH, required=False)
    alamat = forms.CharField(required=False)
    no_kk = forms.CharField(label='No. Kepala Keluarga', max_length=16,
            required=False)

    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())
    ulangi_password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.data.get('username')
        if Pengguna.objects.filter(username=username): # if username already exist
            raise forms.ValidationError('Username sudah dipakai.')
        elif len(username) < 3:
            raise forms.ValidationError('Username terlalu pendek. Minimal 3 karakter')
        return username

    def clean_password(self):
        password = self.data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('Password terlalu pendek. Minimal 6 karakter.')
        elif password.isdigit():
            raise forms.ValidationError('Password tidak boleh angka semua.')
        elif password == password[0] * len(password):
            raise forms.ValidationError('Password terlalu mudah ditebak.')
        return password

    def clean_ulangi_password(self):
        password = self.data.get('password')
        ulangi_password = self.data.get('ulangi_password')
        if password != ulangi_password:
            raise forms.ValidationError('Password tidak sama.')
        return ulangi_password

# class PendaftarForm(forms.Form):
#     pendaftar = forms.CharField(required=False, widget=forms.Textarea,
#             validators=[REGEX_NAMA])
#     def clean_pendaftar(self):
#         pendaftar = self.data.get('pendaftar')
#         return str.title(pendaftar)

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
