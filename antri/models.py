from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

REGEX_TELP = RegexValidator(regex=r'^(\+62|0)\d{9,15}$',
        message="Format nomor telepon: '+628...' atau '08...', \
        maksimal 15 digit.")
REGEX_NAMA = RegexValidator(regex=r'[`~!@#$%^&*()_+=\[\]{}\\|;:",<>/?\d]',
        message="Nama tidak boleh mengandung simbol yang aneh.",
        inverse_match=True)
REGEX_ALAMAT = RegexValidator(regex=r'[`~!@#$%^&*()_+=\[\]{}\\|;:"<>/?]',
        message="Alamat tidak boleh mengandung simbol yang aneh.",
        inverse_match=True)
JENIS_KELAMIN = (('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan'))
NAME_LENGTH = 64

class KepalaKeluarga(models.Model):
    nama = models.CharField(max_length=NAME_LENGTH, validators=[REGEX_NAMA])
    alamat = models.TextField(validators=[REGEX_ALAMAT])
    waktu_daftar = models.DateTimeField(auto_now_add=True)
    waktu_ubah = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.nama, self.pengguna_set.first())

class Pengguna(models.Model):
    nama = models.CharField(max_length=NAME_LENGTH, validators=[REGEX_NAMA])
    tanggal_lahir= models.DateField()
    jenis_kelamin = models.CharField(max_length=9, choices=JENIS_KELAMIN)
    telp = models.CharField(validators=[REGEX_TELP], max_length=18)
    kepala_keluarga = models.ForeignKey(KepalaKeluarga,
            on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    waktu_daftar = models.DateTimeField(auto_now_add=True)
    waktu_ubah = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.nama) > 32:
            return self.nama[:32] + '...'
        return self.nama

class Hari(models.Model):
    tanggal = models.DateField()
    waktu_buka = models.TimeField(default='17:00:00')
    waktu_tutup = models.TimeField(default='20:00:00')

    def __str__(self):
        return '{} ({})'.format(self.tanggal, self.jumlah_pendaftar())

    def jumlah_pendaftar(self):
        counter = 0
        for p in self.pendaftaran_set.all():
            counter += len(p.pendaftar_set.all())
        return counter

class Pendaftaran(models.Model):
    waktu_daftar = models.DateTimeField(auto_now_add=True)
    kepala_keluarga = models.ForeignKey(KepalaKeluarga,
            on_delete=models.CASCADE)
    hari = models.ForeignKey(Hari, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.kepala_keluarga) + ": " + str(self.hari.tanggal)

class Pendaftar(models.Model):
    pendaftaran = models.ForeignKey(Pendaftaran, on_delete=models.CASCADE,
            validators=[REGEX_NAMA])
    nama = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return str(self.nama)
