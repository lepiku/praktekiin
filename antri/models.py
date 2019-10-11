from django.contrib.auth.models import User
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.utils import timezone

REGEX_TELP = RegexValidator(
    regex=r'^(\+62|0)\d{9,15}$',
    message="Format nomor telepon: '+628...' atau '08...', 9-15 digit.",
)
REGEX_NAMA = RegexValidator(
    regex=r'[`~!@#$%^&*()_+=\[\]{}\\|;:",<>/?\d]',
    message="Nama tidak boleh mengandung simbol yang aneh.",
    inverse_match=True,
)
REGEX_ALAMAT = RegexValidator(
    regex=r'[`~!@#$%^&*()_+=\[\]{}\\|;:"<>/?]',
    message="Alamat tidak boleh mengandung simbol yang aneh.",
    inverse_match=True,
)
JENIS_KELAMIN_CHOICES = (('L', 'Laki-Laki'), ('P', 'Perempuan'))
WAKTU_CHOICES = (('PG', 'Pagi'), ('SG', 'Siang'), ('SR', 'Sore'))
STATUS_CHOICES = (('B', 'Baru'), ('L', 'Lama'))
PENDAFTARAN_STATUS_CHOICES = (('N', 'Not Done'), ('W', 'Worked On'), ('D', 'Done'))
NAME_LENGTH = 128


def regex_no(nama, digit=16):
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
    kepala_keluarga = models.CharField(max_length=NAME_LENGTH,
                                       validators=[REGEX_NAMA])

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='B')
    telp = models.CharField(max_length=18, blank=True, validators=[REGEX_TELP])
    nik = models.CharField(max_length=16, blank=True,
                           validators=[regex_no('Nomor Induk Kependudukan')])

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

    def __str__(self):
        return self.user.username


class Tempat(models.Model):
    """
    Tempat Praktek
    """
    nama_tempat = models.CharField(max_length=NAME_LENGTH,
                                   validators=[REGEX_ALAMAT])
    alamat_tempat = models.TextField(validators=[REGEX_ALAMAT])

    def __str__(self):
        return self.nama_tempat


class Jadwal(models.Model):
    tempat = models.ForeignKey(Tempat, on_delete=models.CASCADE)
    hari = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(6)])
    waktu = models.CharField(max_length=2, choices=WAKTU_CHOICES)
    waktu_mulai = models.TimeField()
    waktu_selesai = models.TimeField()

    def __str__(self):
        nama_hari = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        return str(self.tempat) + ': ' + nama_hari[self.hari] + ' ' + self.waktu

    def get_waktu_ms(self):
        mulai = str(self.waktu_mulai.hour)
        selesai = str(self.waktu_selesai.hour)
        return mulai + '-' + selesai

    def get_next_date(self):
        delta = (self.hari - timezone.datetime.today().weekday()) % 7
        return timezone.localtime(
            timezone.now() + timezone.timedelta(days=delta)).date()


class Hari(models.Model):
    jadwal = models.ForeignKey(Jadwal, related_name='hari_set',
                               on_delete=models.CASCADE)
    tanggal = models.DateField()

    def __str__(self):
        return str(self.tanggal) + ': ' + str(self.jadwal.waktu)


class Pendaftaran(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE)
    hari = models.ForeignKey(Hari, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=PENDAFTARAN_STATUS_CHOICES,
                              default='N')
    waktu_buat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pasien) + ': ' + str(self.hari)


class Pesan(models.Model):
    pengguna = models.ForeignKey(Pengguna, on_delete=models.SET_NULL, null=True)
    pesan = models.TextField()
    waktu_buat = models.DateTimeField(auto_now_add=True)
