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
        labels = {
                'telp': 'No. Telp / HP',
                'nik': 'NIK',
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tanggal_lahir'].input_formats = [
                '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y',
                ]
        self.fields['tanggal_lahir'].error_messages = {
                'invalid': 'Format tanggal: dd/mm/yyyy'}

class KepalaKeluargaForm(forms.ModelForm):
    class Meta:
        model = KepalaKeluarga
        fields = ('nama_kk', 'alamat_kk', 'no_kk')
        labels = {
                'nama_kk': 'Nama Kepala Keluarga',
                'alamat_kk': 'Alamat',
                'no_kk': 'No. Kartu Keluarga'
                }

class UserForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Konfirmasi Password tidak sama.",
    }

    def __init__(self, *args, **kwargs):
        # disable autofocus
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields['username'].error_messages = {
                'unique': 'Username sudah dipakai',
                'invalid': 'Username hanya boleh mengandung huruf, angka, dan @/./+/-/_ saja.'
                }
        self.fields['username'].help_text = 'hanya mengandung huruf, angka, dan @/./+/-/_ saja.'
        self.fields['password1'].help_text = 'Panjang minimal 6 karakter.'
        self.fields['password2'].help_text = 'Ulangi password, untuk konfirmasi.'
        self.fields['password2'].label = 'Konfirmasi Password'
        self.error_messages['password_mismatch'] = "Konfirmasi password tidak sama."

    def clean_password1(self):
        password = self.data.get('password1')
        if len(password) < 6:
            raise forms.ValidationError('Password terlalu pendek.')
        elif str(password).isdigit():
            raise forms.ValidationError('Password tidak boleh angka semua.')
        elif password in 'qwertyuiopasdfghjklzxcvbnm'\
                or password == password[0:1] * len(password):
            raise forms.ValidationError('Password terlalu mudah ditebak.')
        return password

    # disable password verification
    def _post_clean(self):
        super(forms.ModelForm, self)._post_clean()

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
