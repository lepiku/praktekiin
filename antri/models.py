from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

regex_telp = RegexValidator(regex=r'^(\+62|0)\d{9,15}$', \
        message="Nomor Handphone harus mengikuti format: \
                '+628...' or '08...' maksimal 15 digit.")

class KepalaKeluarga(models.Model):
    nama = models.CharField(max_length=128)
    alamat = models.TextField()

    def __str__(self):
        return str(self.nama)

class Pengguna(models.Model):
    JENIS_KELAMIN_CHOICES = (('l', 'Laki-Laki'), ('p', 'Perempuan'))

    nama = models.CharField(max_length=128)
    tanggal_lahir= models.DateField()
    jenis_kelamin = models.CharField(max_length=1,
            choices=JENIS_KELAMIN_CHOICES)
    telp = models.CharField(validators=[regex_telp], max_length=18)
    kepala_keluarga = models.ForeignKey(KepalaKeluarga,
            on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nama)

class Hari(models.Model):
    tanggal = models.DateField()
    waktu_buka = models.TimeField()
    waktu_tutup = models.TimeField()

    def __str__(self):
        return str(self.tanggal)

class Pendaftaran(models.Model):
    watu_daftar = models.DateTimeField(auto_now=True)
    pengguna = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    hari = models.ForeignKey(Hari, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pengguna) + ": " + str(self.hari)

