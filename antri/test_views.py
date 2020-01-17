from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Jadwal, Pasien, Pendaftaran, Tempat


class LoggedOutTest(TestCase):
    def test_index(self):
        response = self.client.get('/')

        self.assertContains(response, 'Fibrianti')
        self.assertContains(response, 'Silahkan masuk terlebih dahulu.', html=True)

    def test_masuk(self):
        response = self.client.get('/masuk/')

        self.assertContains(response, '<a href="/daftar/')

    def test_tentang(self):
        response = self.client.get('/tentang/')

        self.assertContains(response, '<h1>Tentang Bu Dokter</h1>', html=True)
        self.assertContains(response, 'Fakultas Kedokteran Gigi Universitas Gajah Mada')

    def test_daftar(self):
        response = self.client.get('/daftar/')

        self.assertContains(response, '<form method="POST">')
        self.assertContains(response, '<input type="text" name="username"')
        self.assertContains(response, '<input type="password" name="password1"')
        self.assertContains(response, '<input type="password" name="password2"')

        response = self.client.post('/daftar/', follow=True, data={
            'username': 'dimas',
            'password1': 'q12we34',
            'password2': 'q12we34',
        })

        self.assertContains(response, 'Daftar Pasien')
        self.assertContains(response, 'Tambah Pasien')

    def test_daftar_invalid(self):
        response = self.client.post('/daftar/', follow=True, data={
            'username': 'dimas',
            'password1': 'abc',
            'password2': 'abc',
        })
        self.assertContains(response, 'Password terlalu pendek.', html=True)

        response = self.client.post('/daftar/', follow=True, data={
            'username': 'dimas',
            'password1': '123456',
            'password2': '123456',
        })
        self.assertContains(response, 'Password tidak boleh angka semua.', html=True)

        response = self.client.post('/daftar/', follow=True, data={
            'username': 'dimas',
            'password1': 'qwerty',
            'password2': 'qwerty',
        })
        self.assertContains(response, 'Password terlalu mudah ditebak.', html=True)

class LoggedInTest(TestCase):
    def setUp(self):
        rumah = Tempat(nama_tempat="Rumah",
                       alamat_tempat="Perumahan")
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

        self.client.post('/daftar/', follow=True, data={
            'username': 'user',
            'password1': 'secret',
            'password2': 'secret',
        })

        self.client.post('/daftar-pasien/', follow=True, data={
            'nama': 'Dimas',
            'tanggal_lahir_month': 1,
            'tanggal_lahir_day': 1,
            'tanggal_lahir_year': 2000,
            'jenis_kelamin': 'L',
            'kepala_keluarga': 'Ayah',
            'status': 'B',
        })
        self.client.post('/daftar-pasien/', follow=True, data={
            'nama': 'Adek',
            'tanggal_lahir_month': 2,
            'tanggal_lahir_day': 2,
            'tanggal_lahir_year': 2001,
            'jenis_kelamin': 'P',
            'kepala_keluarga': 'Ayah',
            'status': 'B',
        })

    def test_index(self):
        response = self.client.get('/')

        self.assertContains(response, 'Fibrianti')
        self.assertNotContains(response, 'Silahkan masuk terlebih dahulu.', html=True)
        self.assertContains(response, 'user', html=True)

    def test_daftar_pasien(self):
        response = self.client.get('/daftar-pasien/')

        self.assertContains(response, 'Daftar Pasien')
        self.assertContains(response, 'Nama Lengkap')
        self.assertContains(response, 'Tanggal Lahir')
        self.assertContains(response, 'Jenis Kelamin')
        self.assertContains(response, 'Nama Kepala Keluarga')
        self.assertContains(response, 'Status')
        self.assertContains(response, 'No. Telp / HP')
        self.assertContains(response, 'NIK')
        self.assertEqual(Pasien.objects.count(), 2)

        response = self.client.post('/daftar-pasien/', follow=True, data={
            'nama': 'Kakak',
            'tanggal_lahir_month': 3,
            'tanggal_lahir_day': 3,
            'tanggal_lahir_year': 1999,
            'jenis_kelamin': 'P',
            'kepala_keluarga': 'Ayah',
            'status': 'L',
        })

        self.assertRedirects(response, '/profil/')
        self.assertContains(response, 'Dimas', html=True)
        self.assertContains(response, 'Adek', html=True)
        self.assertContains(response, 'Kakak', html=True)
        self.assertContains(response, 'Ayah', count=3, html=True)
        self.assertContains(response, 'Ubah', html=True)
        self.assertEqual(Pasien.objects.count(), 3)

    def test_daftar_antri(self):
        response = self.client.get('/daftar-antri/')

        self.assertContains(response, '<th>Tempat:</th>', html=True)
        self.assertContains(response, '<th>Waktu:</th>', html=True)
        self.assertContains(response, 'Tanggal')
        self.assertContains(response, '<th>Pasien:</th>', html=True)

        response = self.client.post('/daftar-antri/', follow=True, data={
            'tempat': 1,
            'jadwal': 1,
            'tanggal': timezone.now().date(),
            'pasien_set': [1, 2],
        })

        self.assertEqual(Pendaftaran.objects.count(), 2)
        self.assertRedirects(response, '/pendaftaran/')
        self.assertContains(response, 'Dimas', html=True)
        self.assertContains(response, 'Adek', html=True)

        response = self.client.post('/daftar-antri/', follow=True, data={
            'tempat': 1,
            'jadwal': 1,
            'tanggal': timezone.now().date(),
            'pasien_set': [2],
        })

        self.assertEqual(Pendaftaran.objects.count(), 1)
        self.assertRedirects(response, '/pendaftaran/')
        self.assertNotContains(response, 'Dimas', html=True)
        self.assertContains(response, 'Adek', html=True)

    def test_pendaftaran_hari_ini(self):
        self.client.post('/', follow=True, data={
            'pasien_set': [1, 2],
        })

        self.assertEqual(Pendaftaran.objects.count(), 2)

        self.client.post('/', follow=True, data={
            'pasien_set': [1],
        })
        self.assertEqual(Pendaftaran.objects.count(), 1)

    def test_ubah_pasien(self):
        response = self.client.get('/ubah/pasien/1/')

        self.assertContains(response, '<input type="text" name="nama" value="Dimas"')

        response = self.client.post('/ubah/pasien/1/', follow=True, data={
            'nama': 'Okto',
            'tanggal_lahir_month': 1,
            'tanggal_lahir_day': 1,
            'tanggal_lahir_year': 2000,
            'jenis_kelamin': 'L',
            'kepala_keluarga': 'Ayah',
            'status': 'B',
        })

        self.assertRedirects(response, '/profil/')
        self.assertContains(response, 'Okto', html=True)

    def test_ubah_username(self):
        response = self.client.get('/ubah/username/')

        self.assertContains(response, '<input type="text" name="username" value="user"')

        response = self.client.post('/ubah/username/', follow=True, data={
            'username': 'username_baru',
        })

        self.assertRedirects(response, '/profil/')
        self.assertContains(response, 'username_baru', html=True)

    def test_ubah_password(self):
        user_id = self.client.session['_auth_user_id']
        response = self.client.get('/ubah/password/')

        self.assertContains(response, '<input type="password" name="old_password"')
        self.assertContains(response, '<input type="password" name="new_password1"')
        self.assertContains(response, '<input type="password" name="new_password2"')

        user = User.objects.get(id=user_id)
        old_password = user.password

        response = self.client.post('/ubah/password/', follow=True, data={
            'old_password': 'secret',
            'new_password1': 'passwordbaru',
            'new_password2': 'passwordbaru',
        })

        user = User.objects.get(id=user_id)
        self.assertNotEqual(old_password, user.password)
        self.assertRedirects(response, '/profil/')

    def test_ubah_password_invalid(self):
        response = self.client.post('/ubah/password/', follow=True, data={
            'old_password': 'secret',
            'new_password1': 'abc',
            'new_password2': 'abc',
        })
        self.assertContains(response, 'Password terlalu pendek.', html=True)

        response = self.client.post('/ubah/password/', follow=True, data={
            'old_password': 'secret',
            'new_password1': '123456',
            'new_password2': '123456',
        })
        self.assertContains(response, 'Password tidak boleh angka semua.', html=True)

        response = self.client.post('/ubah/password/', follow=True, data={
            'old_password': 'secret',
            'new_password1': 'qwerty',
            'new_password2': 'qwerty',
        })
        self.assertContains(response, 'Password terlalu mudah ditebak.', html=True)

        response = self.client.post('/ubah/password/', follow=True, data={
            'old_password': 'secret',
            'new_password1': 'password1',
            'new_password2': 'paasword1',
        })
        self.assertContains(response, 'Konfirmasi Password Baru tidak sama.', html=True)

    def test_pasien_detail(self):
        response = self.client.get('/pasien/1/')

        self.assertContains(response, 'Dimas', html=True)
        self.assertContains(response, 'L', html=True)
        self.assertContains(response, '000101', html=True)
        self.assertContains(response, 'Ayah', html=True)

    def test_hapus_pasien(self):
        response = self.client.post('/hapus/pasien/', follow=True, data={
            'delete_id': 1,
        })

        self.assertRedirects(response, '/profil/')
        self.assertEqual(Pasien.objects.count(), 2)
        self.assertEqual(Pasien.objects.filter(keaktifan=True).count(), 1)
