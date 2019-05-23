from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Phone(models.Model):
    phone_regex = RegexValidator(regex=r'^(\+62|0)\d{9,15}$', \
            message="Phone number must be entered in the format: '+999999999'. \
                    Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, \
            blank=True)

class Pengguna(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=128)
    no_hp = models.OneToOneField(Phone, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nama)

class Pendaftaran(models.Model):
    watu_daftar = models.DateTimeField(auto_now=true)
    pengguna = models.ForeignKey(Pengguna, on_delete=models.CASCADE)
    hari = models.ForeignKey(Hari, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pengguna) + ": " + str(self.hari)

class Hari(models.Model):
    tanggal = models.DateField()
    waktu_buka = models.TimeField()
    waktu_tutup = models.TimeField()

    def __str__(self):
        return str(self.tanggal)
