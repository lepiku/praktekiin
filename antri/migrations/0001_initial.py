# Generated by Django 2.1.7 on 2019-07-03 03:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hari',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField()),
                ('waktu_buka', models.TimeField(default='17:00:00')),
                ('waktu_tutup', models.TimeField(default='20:00:00')),
            ],
        ),
        migrations.CreateModel(
            name='Keluarga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_buat', models.DateTimeField(auto_now_add=True)),
                ('waktu_ubah', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pasien',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(inverse_match=True, message='Nama tidak boleh mengandung simbol yang aneh.', regex='[`~!@#$%^&*()_+=\\[\\]{}\\\\|;:",<>/?\\d]')])),
                ('tanggal_lahir', models.DateField()),
                ('jenis_kelamin', models.CharField(choices=[('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan')], max_length=9)),
                ('mrid', models.CharField(max_length=6)),
                ('telp', models.CharField(blank=True, max_length=18, validators=[django.core.validators.RegexValidator(message="Format nomor telepon: '+628...' atau '08...', 9-15 digit.", regex='^(\\+62|0)\\d{9,15}$')])),
                ('nik', models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message='Nomor Induk Kependudukan harus memiliki 16 digit.', regex='^\\d{16}$')])),
                ('waktu_buat', models.DateTimeField(auto_now_add=True)),
                ('waktu_ubah', models.DateTimeField(auto_now=True)),
                ('keluarga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='antri.Keluarga')),
            ],
        ),
        migrations.CreateModel(
            name='Pengguna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_buat', models.DateTimeField(auto_now_add=True)),
                ('waktu_ubah', models.DateTimeField(auto_now=True)),
                ('keluarga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='antri.Keluarga')),
                ('pasien', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='antri.Pasien')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pesan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pesan', models.TextField()),
                ('waktu_buat', models.DateTimeField(auto_now_add=True)),
                ('pengguna', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='antri.Pengguna')),
            ],
        ),
    ]
