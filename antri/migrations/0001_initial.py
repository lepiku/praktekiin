# Generated by Django 2.2.1 on 2019-07-11 00:38

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
                ('waktu', models.CharField(choices=[('PG', 'Pagi'), ('SG', 'Siang'), ('SR', 'Sore')], max_length=2)),
                ('waktu_mulai', models.TimeField()),
                ('waktu_selesai', models.TimeField()),
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
                ('jenis_kelamin', models.CharField(choices=[('L', 'Laki-Laki'), ('P', 'Perempuan')], max_length=9)),
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
                ('pasien', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='antri.Pasien')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tempat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_tempat', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(inverse_match=True, message='Alamat tidak boleh mengandung simbol yang aneh.', regex='[`~!@#$%^&*()_+=\\[\\]{}\\\\|;:"<>/?]')])),
                ('alamat_tempat', models.TextField(validators=[django.core.validators.RegexValidator(inverse_match=True, message='Alamat tidak boleh mengandung simbol yang aneh.', regex='[`~!@#$%^&*()_+=\\[\\]{}\\\\|;:"<>/?]')])),
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
        migrations.CreateModel(
            name='Pendaftaran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_buat', models.DateTimeField(auto_now_add=True)),
                ('hari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='antri.Hari')),
                ('keluarga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='antri.Keluarga')),
                ('pasien_set', models.ManyToManyField(to='antri.Pasien')),
                ('tempat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='antri.Tempat')),
            ],
        ),
    ]
