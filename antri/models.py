from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Pengguna(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=128)
    regex_hp = RegexValidator(regex=r'^(\+62|0)\d{9,15}$', \
            message="Nomor Handphone harus mengikuti format: \
                    '+628...' or '08...' maksimal 15 digit.")
    no_hp = models.CharField(validators=[regex_hp], max_length=18)

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

