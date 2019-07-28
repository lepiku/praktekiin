from django.contrib.auth.models import User
from antri.models import Pengguna, Keluarga, Pasien, Tempat, Jadwal

user = User(username='dimas', is_staff=True, is_superuser=True)
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


