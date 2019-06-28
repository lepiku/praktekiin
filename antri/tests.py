from django.test import TestCase
from .models import KepalaKeluarga

# Create your tests here.
class ViewsTest(TestCase):
    def test_daftar_kk_new(self):
        data = {
            'nama': 'Someone',
            'tanggal_lahir': '1/1/2000',
            'jenis_kelamin': 'Laki-Laki',
            'telp': '081111111111',
            'nama_kk': 'Father',
            'username': 'someone',
            'password': 'theone',
            'ulangi_password': 'theone'}
        response = self.client.post('/daftar/', data)
        self.assertIn(b'Alamat', response.content)

    def test_daftar_kk_old(self):
        KepalaKeluarga.objects.create(nama="Father", alamat="Home Sweet Home")\
                .save()
        data = {
            'nama': 'Someone',
            'tanggal_lahir': '1/1/2000',
            'jenis_kelamin': 'Laki-Laki',
            'telp': '081111111111',
            'nama_kk': 'Father',
            'username': 'someone',
            'password': 'theone',
            'ulangi_password': 'theone'}
        response = self.client.post('/daftar/', data)
        self.assertIn(b'<select name="kk"', response.content)
