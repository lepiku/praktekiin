from django.urls import path
from . import views

app_name = 'antri'

urlpatterns = [
    path('', views.utama, name='utama'),
    path('masuk/', views.masuk, name='masuk'),
    path('keluar/', views.keluar, name='keluar'),
    path('daftar/', views.daftar, name='daftar'),
    path('tentang/', views.tentang, name='tentang'),
]
