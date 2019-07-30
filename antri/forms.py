from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.utils import timezone

from .models import WAKTU_CHOICES, Pasien, Tempat

NAMA_BULAN = {1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei",
              6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober",
              11: "November", 12: "Desember"}


class DateField(forms.DateField):
    input_formats = ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y']
    error_messages = {'invalid': 'Format tanggal: dd/mm/yyyy'}

class PasienForm(forms.ModelForm):
    class Meta:
        model = Pasien
        exclude = ('mrid', 'keluarga')
        labels = {
                'nama': 'Nama Lengkap',
                'telp': 'No. Telp / HP',
                'nik': 'NIK',
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tanggal_lahir = self.fields['tanggal_lahir']
        tanggal_lahir.error_messages = {
                'invalid': 'Format tanggal: dd/mm/yyyy'}

        year = timezone.localtime(timezone.now()).year
        tanggal_lahir.widget = forms.SelectDateWidget(
            years=[y for y in range(year, year - 100, -1)],
            months=NAMA_BULAN)


class UserForm(UserCreationForm):
    error_messages = {
        **UserCreationForm.error_messages,
        'password_mismatch': "Konfirmasi Password tidak sama.",
    }

    def __init__(self, *args, **kwargs):
        # disable autofocus
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields['username'].error_messages = {
                'unique': 'Username sudah dipakai',
                'invalid': 'Username hanya boleh mengandung huruf, angka, dan @/./+/-/_ saja.'
                }
        self.fields['password2'].label = 'Konfirmasi Password'
        self.fields['username'].help_text = 'hanya mengandung huruf, angka, dan @/./+/-/_ saja.'
        self.fields['password1'].help_text = 'Panjang minimal 6 karakter.'
        self.fields['password2'].help_text = 'Ulangi password, untuk konfirmasi.'
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

class UbahPasswordForm(PasswordChangeForm):
    error_messages = {
        **PasswordChangeForm.error_messages,
        'password_incorrect': "Password lama salah",
        'password_mismatch': "Konfirmasi Password Baru tidak sama.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Password Lama'
        self.fields['new_password1'].label = 'Password Baru'
        self.fields['new_password2'].label = 'Konfirmasi Password Baru'
        self.fields['new_password1'].help_text = 'Panjang minimal 6 karakter.'
        self.fields['new_password2'].help_text = 'Ulangi password, untuk konfirmasi.'

    def clean_new_password1(self):
        password = self.data.get('new_password1')
        if len(password) < 6:
            raise forms.ValidationError('Password terlalu pendek.')
        elif str(password).isdigit():
            raise forms.ValidationError('Password tidak boleh angka semua.')
        elif password in 'qwertyuiopasdfghjklzxcvbnm'\
                or password == password[0:1] * len(password):
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


class PendaftaranPasienForm(forms.Form):
    def __init__(self, *args, **kwargs):
        query = kwargs.pop('pasien_set', Pasien.objects.none())
        super().__init__(*args, **kwargs)

        self.fields['pasien_set'] = forms.ModelMultipleChoiceField(query,
                widget=forms.CheckboxSelectMultiple)


class PendaftaranForm(PendaftaranPasienForm):
    tempat = forms.ModelChoiceField(Tempat.objects.all())
    waktu = forms.ChoiceField(choices=WAKTU_CHOICES, widget=forms.HiddenInput)
    hari = forms.IntegerField(widget=forms.HiddenInput)
    tanggal = forms.DateField(widget=forms.HiddenInput)
