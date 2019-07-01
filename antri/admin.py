from django.contrib import admin
from antri.models import Pengguna, KepalaKeluarga, Hari

# class PenggunaAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'kepala_keluarga', 'user')

# class PendaftarInline(admin.TabularInline):
#     model = Pendaftar
#     extra = 1

# class PendaftaranAdmin(admin.ModelAdmin):
#     list_display = ('pengguna', 'hari')
#     inlines = [PendaftarInline]

# Register your models here.
admin.site.register([Pengguna, KepalaKeluarga, Hari])
# admin.site.register(Pengguna, PenggunaAdmin)
# admin.site.register(Pendaftaran, PendaftaranAdmin)

