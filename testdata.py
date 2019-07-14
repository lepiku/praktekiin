from django.contrib.auth.models import User
from antri.models import Pengguna, Keluarga, Pasien, Tempat

user = User(username='dimas')
user.set_password('okto')
user.save()

kel = Keluarga()
kel.save()

p = Pasien(
        nama="Muhammad Oktoluqman Fakhrianto",
        tanggal_lahir="2019-10-11",
        jenis_kelamin="L",
        mrid="000101",
        keluarga=kel,
        )
p.save()

Pasien(
        nama="Ariq Basyar",
        tanggal_lahir="2019-10-7",
        jenis_kelamin="L",
        mrid="000102",
        keluarga=kel,
        ).save()

Pengguna(
        user=user,
        keluarga=kel,
        pasien=p,
        ).save()

Tempat(
        nama_tempat="Rumah",
        alamat_tempat="Depok Maharaja Blok O4",
        ).save()
Tempat(
        nama_tempat="Ruko",
        alamat_tempat="Jl. Raya Sawangan",
        ).save()

