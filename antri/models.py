from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

REGEX_TELP = RegexValidator(regex=r'^(\+62|0)\d{9,15}$', \
        message="Nomor Handphone harus mengikuti format: \
                '+628...' or '08...' maksimal 15 digit.")
JENIS_KELAMIN = (('l', 'Laki-Laki'), ('p', 'Perempuan'))

class KepalaKeluarga(models.Model):
    nama = models.CharField(max_length=128)
    alamat = models.TextField()

    def __str__(self):
        return str(self.id) + ": " + str(self.nama)

class Pengguna(models.Model):
    nama = models.CharField(max_length=128)
    tanggal_lahir= models.DateField()
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN)
    telp = models.CharField(validators=[REGEX_TELP], max_length=18)
    kepala_keluarga = models.ForeignKey(KepalaKeluarga,
            on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nama)

class Hari(models.Model):
    tanggal = models.DateField()
    waktu_buka = models.TimeField(default='17:00:00')
    waktu_tutup = models.TimeField(default='20:00:00')

    def __str__(self):
        return str(self.tanggal)
    # def get_absolute_url(self):
        # return

class Pendaftaran(models.Model):
    watu_daftar = models.DateTimeField(auto_now=True)
    pengguna = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    hari = models.ForeignKey(Hari, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pengguna) + ": " + str(self.hari)

