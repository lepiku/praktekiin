from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import (Hari, Jadwal, Keluarga, Pasien, Pendaftaran, Pengguna,
                     Tempat)

# Create your tests here.
class ModelUsersTest(TestCase):
    def test_user(self):
        user = User(username='dimas', is_staff=True, is_superuser=True)
        user.save()

        all_user = User.objects.all()

        self.assertEqual(all_user.count(), 1)
        self.assertIn(user, all_user)

    def test_pengguna(self):
        kel = Keluarga()
        kel.save()
        user = User(username='dimas', is_staff=True, is_superuser=True)
        user.save()
        pengguna = Pengguna(
            user=user,
            keluarga=kel,
        )
        pengguna.save()

        all_pengguna = Pengguna.objects.all()

        self.assertEqual(all_pengguna.count(), 1)
        self.assertIn(pengguna, all_pengguna)

    def test_keluarga(self):
        user = User(username='dimas', is_staff=True, is_superuser=True)
        user.save()
        kel = Keluarga()
        kel.save()
        pengguna = Pengguna(
            user=user,
            keluarga=kel,
        )
        pengguna.save()

        all_keluarga = Keluarga.objects.all()

        self.assertEqual(all_keluarga.count(), 1)
        self.assertIn(kel, all_keluarga)
        self.assertEqual(str(kel), 'Keluarga dimas')

    def test_pasien(self):
        kel = Keluarga()
        kel.save()
        pasien = Pasien(
            nama="Muhammad Oktoluqman Fakhrianto",
            tanggal_lahir="2000-10-10",
            jenis_kelamin="L",
            keluarga=kel,
            kepala_keluarga='Bapak',
        )
        pasien.save()

        all_pasien = Pasien.objects.all()

        self.assertEqual(all_pasien.count(), 1)
        self.assertIn(pasien, all_pasien)
        self.assertEqual(str(pasien), "Muhammad Oktoluqman Fakhrianto")
        self.assertEqual(pasien.clean_first_name(),
                         "Muhammad Oktoluqman Fakhrianto")


class ModelAntriTest(TestCase):
    def test_tempat(self):
        rumah = Tempat(nama_tempat="Rumah",
                       alamat_tempat="Perumahan di Depok")
        rumah.save()
        ruko = Tempat(nama_tempat="Ruko",
                      alamat_tempat="Jl. Raya Sawangan")
        ruko.save()

        all_tempat = Tempat.objects.all()

        self.assertEqual(all_tempat.count(), 2)
        self.assertIn(rumah, all_tempat)
        self.assertIn(ruko, all_tempat)
        self.assertEqual(str(rumah), 'Rumah')

    def test_jadwal(self):
        rumah = Tempat(nama_tempat="Rumah",
                       alamat_tempat="Perumahan di Depok")
        rumah.save()

        for hari in range(5):
            Jadwal(tempat=rumah,
                   hari=hari,
                   waktu='SR',
                   waktu_mulai='17:30:00',
                   waktu_selesai='20:00:00').save()

        all_jadwal = Jadwal.objects.all()
        jadwal = all_jadwal.first()

        self.assertEqual(all_jadwal.count(), 5)
        self.assertEqual(str(jadwal), 'Rumah: Mon SR')
        self.assertEqual(jadwal.get_waktu_ms(), '17-20')

        delta = (jadwal.hari - timezone.now().weekday()) % 7
        date = timezone.localtime(
            timezone.now() + timezone.timedelta(days=delta)).date()
        self.assertEqual(jadwal.get_next_date(), date)

    def test_hari(self):
        rumah = Tempat(nama_tempat="Rumah",
                       alamat_tempat="Perumahan di Depok")
        rumah.save()
        jadwal = Jadwal(tempat=rumah,
                        hari=0,
                        waktu='SR',
                        waktu_mulai='17:30:00',
                        waktu_selesai='20:00:00')
        jadwal.save()

        hari = Hari(jadwal=jadwal, tanggal=jadwal.get_next_date())
        hari.full_clean()
        hari.save()

        all_hari = Hari.objects.all()

        self.assertEqual(all_hari.count(), 1)
        self.assertIn(hari, all_hari)
        self.assertEqual(str(hari), str(hari.tanggal) + ': ' + str(jadwal.waktu))

    def test_pendaftaran(self):
        kel = Keluarga()
        kel.save()
        pasien = Pasien(
            nama="Muhammad Oktoluqman Fakhrianto",
            tanggal_lahir="2000-10-10",
            jenis_kelamin="L",
            keluarga=kel,
            kepala_keluarga='Bapak',
        )
        pasien.save()
        rumah = Tempat(nama_tempat="Rumah",
                       alamat_tempat="Perumahan di Depok")
        rumah.save()
        jadwal = Jadwal(tempat=rumah,
                        hari=0,
                        waktu='SR',
                        waktu_mulai='17:30:00',
                        waktu_selesai='20:00:00')
        jadwal.save()
        hari = Hari(jadwal=jadwal, tanggal=timezone.now())
        hari.save()
        pdft = Pendaftaran(pasien=pasien,
                           hari=hari)
        pdft.save()

        all_pdft = Pendaftaran.objects.all()

        self.assertEqual(all_pdft.count(), 1)
        self.assertIn(pdft, all_pdft)
        self.assertEqual(str(pdft), str(pasien) + ': ' + str(hari))
