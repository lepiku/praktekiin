from django.contrib import admin
from antri.models import Pengguna, Keluarga, Pasien, Tempat, Jadwal, Hari, Pendaftaran

# class PenggunaAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'kepala_keluarga', 'user')

# class PendaftarInline(admin.TabularInline):
#     model = Pendaftar
#     extra = 1

# class PendaftaranAdmin(admin.ModelAdmin):
#     list_display = ('pengguna', 'hari')
#     inlines = [PendaftarInline]

admin.site.register([Pengguna, Keluarga, Pasien, Tempat, Jadwal, Hari, Pendaftaran])
# admin.site.register(Pengguna, PenggunaAdmin)
# admin.site.register(Pendaftaran, PendaftaranAdmin)

