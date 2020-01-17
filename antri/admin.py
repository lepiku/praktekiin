from django.contrib import admin
from antri.models import Pengguna, Keluarga, Pasien, Tempat, Jadwal, Hari, Pendaftaran

@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    list_display = ('nama', 'keaktifan', 'keluarga', 'waktu_buat')
    list_filter = ('keaktifan',)

admin.site.register([Pengguna, Keluarga, Tempat, Jadwal, Hari, Pendaftaran])
