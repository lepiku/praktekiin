from django.contrib.auth.models import User
from antri.models import Pengguna, Keluarga, Pasien, Tempat, Jadwal

user = User(username='dimas', is_staff=True, is_superuser=True)
user.set_password('okto')
user.save()

kel = Keluarga()
kel.save()

p = Pasien(
        nama="Muhammad Oktoluqman Fakhrianto",
        tanggal_lahir="2000-10-24",
        jenis_kelamin="L",
        mrid="000101",
        keluarga=kel,
        kepala_keluarga='Eko Winarso',
        )
p.save()

Pasien(
        nama="Adinda Natasya Maharani",
        tanggal_lahir="2002-2-10",
        jenis_kelamin="P",
        mrid="000102",
        keluarga=kel,
        kepala_keluarga='Eko Winarso',
        ).save()

Pasien(
        nama="Fabiola Nadhira Maharani",
        tanggal_lahir="2002-2-17",
        jenis_kelamin="P",
        mrid="000103",
        keluarga=kel,
        kepala_keluarga='Eko Winarso',
        ).save()

Pengguna(
        user=user,
        keluarga=kel,
        pasien=p,
        ).save()

rumah = Tempat(nama_tempat="Rumah",
               alamat_tempat="Depok Maharaja Blok O4")
rumah.save()

ruko = Tempat(nama_tempat="Ruko",
              alamat_tempat="Jl. Raya Sawangan")
ruko.save()

for hari in range(5):
    Jadwal(tempat=rumah,
           hari=hari,
           waktu='SR',
           waktu_mulai='17:30:00',
           waktu_selesai='20:00:00').save()

Jadwal(tempat=ruko,
       hari=5,
       waktu='SR',
       waktu_mulai='17:00:00',
       waktu_selesai='20:30:00').save()


