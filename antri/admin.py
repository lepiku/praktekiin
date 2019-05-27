from django.contrib import admin
from antri import models

# Register your models here.
admin.site.register([
    models.Pengguna, models.KepalaKeluarga, models.Pendaftaran, models.Hari
    ])

