from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

REGEX_TELP = RegexValidator(regex=r'^(\+62|0)\d{9,15}$',
        message="Format nomor telepon: '+628...' atau '08...', 9-15 digit.")
REGEX_NAMA = RegexValidator(regex=r'[`~!@#$%^&*()_+=\[\]{}\\|;:",<>/?\d]',
        message="Nama tidak boleh mengandung simbol yang aneh.",
        inverse_match=True)
REGEX_ALAMAT = RegexValidator(regex=r'[`~!@#$%^&*()_+=\[\]{}\\|;:"<>/?]',
        message="Alamat tidak boleh mengandung simbol yang aneh.",
        inverse_match=True)
JENIS_KELAMIN = (('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan'))
NAME_LENGTH = 128

def regex_no_id(nama, digit=16):
    return RegexValidator(regex=r'^\d{' + str(digit) + r'}$',
            message="{} harus memiliki {} digit.".format(nama, digit))


class Keluarga(models.Model):
    waktu_buat = models.DateTimeField(auto_now_add=True)
    waktu_ubah = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Keluarga ' + str(self.pengguna_set.first())

class Pasien(models.Model):
    # wajib
    nama = models.CharField(max_length=NAME_LENGTH, validators=[REGEX_NAMA])
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=9, choices=JENIS_KELAMIN)
    mrid = models.CharField(max_length=6)
    keluarga = models.ForeignKey(Keluarga, on_delete=models.CASCADE)
    # gak wajib
    telp = models.CharField(max_length=18, blank=True, validators=[REGEX_TELP])
    nik = models.CharField(max_length=16, blank=True,
            validators=[regex_no_id('Nomor Induk Kependudukan')])

    waktu_buat = models.DateTimeField(auto_now_add=True)
    waktu_ubah = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

    def clean_first_name(self):
        return str.title(self.nama)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

class Pengguna(models.Model):
    # wajib ada
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    keluarga = models.ForeignKey(Keluarga, on_delete=models.CASCADE)
    # gak wajib
    pasien = models.OneToOneField(Pasien, on_delete=models.SET_NULL, null=True)

    waktu_buat = models.DateTimeField(auto_now_add=True)
    waktu_ubah = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.pasien:
            return self.pasien.nama
        return user.username

class Hari(models.Model):
    tanggal = models.DateField()
    waktu_buka = models.TimeField(default='17:00:00')
    waktu_tutup = models.TimeField(default='20:00:00')

    # def __str__(self):
    #     return '{} ({})'.format(self.tanggal, self.jumlah_pendaftar())

    # def jumlah_pendaftar(self):
    #     counter = 0
    #     for p in self.pendaftaran_set.all():
    #         counter += len(p.pendaftar_set.all())
    #     return counter

# class Pendaftaran(models.Model):
#     pengguna = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
#     hari = models.ForeignKey(Hari, on_delete=models.CASCADE)
#     waktu_buat = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.pengguna) + ": " + str(self.hari.tanggal)

# class Pendaftar(models.Model):
#     pendaftaran = models.ForeignKey(Pendaftaran, on_delete=models.CASCADE)
#     nama = models.CharField(max_length=NAME_LENGTH, validators=[REGEX_NAMA])

#     def __str__(self):
#         return str(self.nama)

class Pesan(models.Model):
    pengguna = models.ForeignKey(Pengguna, on_delete=models.SET_NULL, null=True)
    pesan = models.TextField()
    waktu_buat = models.DateTimeField(auto_now_add=True)
