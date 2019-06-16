from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

REGEX_TELP = RegexValidator(regex=r'^(\+62|0)\d{9,15}$', \
        message="Nomor Handphone harus mengikuti format: \
                '+628...' or '08...' maksimal 15 digit.")
JENIS_KELAMIN = (('l', 'Laki-Laki'), ('p', 'Perempuan'))
NAME_LENGTH = 64

class KepalaKeluarga(models.Model):
    nama = models.CharField(max_length=NAME_LENGTH)
    alamat = models.TextField()
    waktu_daftar = models.DateTimeField(auto_now_add=True)
    waktu_ubah = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.nama, self.pengguna_set.first())

class Pengguna(models.Model):
    nama = models.CharField(max_length=NAME_LENGTH)
    tanggal_lahir= models.DateField()
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN)
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
    watu_daftar = models.DateTimeField(auto_now_add=True)
    kepala_keluarga = models.ForeignKey(KepalaKeluarga,
            on_delete=models.CASCADE)
    hari = models.ForeignKey(Hari, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.kepala_keluarga) + ": " + str(self.hari.tanggal)

class Pendaftar(models.Model):
    pendaftaran = models.ForeignKey(Pendaftaran, on_delete=models.CASCADE)
    nama = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return str(self.nama)
