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
JENIS_KELAMIN_CHOICES = (('L', 'Laki-Laki'), ('P', 'Perempuan'))
WAKTU_CHOICES = (('PG', 'Pagi'), ('SG', 'Siang'), ('SR', 'Sore'))
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
    nama = models.CharField(max_length=NAME_LENGTH, validators=[REGEX_NAMA])
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=9,
            choices=JENIS_KELAMIN_CHOICES)
    mrid = models.CharField(max_length=6)
    keluarga = models.ForeignKey(Keluarga, on_delete=models.CASCADE)

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


class Pengguna(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    keluarga = models.ForeignKey(Keluarga, on_delete=models.CASCADE)
    pasien = models.OneToOneField(Pasien, on_delete=models.SET_NULL, null=True)

    waktu_buat = models.DateTimeField(auto_now_add=True)
    waktu_ubah = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.pasien:
            return self.pasien.nama
        return user.username


class Tempat(models.Model):
    """
    Tempat Praktek
    """
    nama_tempat = models.CharField(max_length=NAME_LENGTH,
            validators=[REGEX_ALAMAT])
    alamat_tempat = models.TextField(validators=[REGEX_ALAMAT])

    def __str__(self):
        return self.nama_tempat


class Hari(models.Model):
    tanggal = models.DateField()
    waktu = models.CharField(max_length=2, choices=WAKTU_CHOICES)
    waktu_buka = models.TimeField()
    waktu_tutup = models.TimeField()


class Pendaftaran(models.Model):
    hari = models.ForeignKey(Hari, on_delete=models.CASCADE)
    tempat = models.ForeignKey(Tempat, on_delete=models.CASCADE)
    pasien_set = models.ManyToManyField(Pasien)
    waktu_buat = models.DateTimeField(auto_now_add=True)


class Pesan(models.Model):
    pengguna = models.ForeignKey(Pengguna, on_delete=models.SET_NULL, null=True)
    pesan = models.TextField()
    waktu_buat = models.DateTimeField(auto_now_add=True)
