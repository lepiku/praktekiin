from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'antri'
urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('tentang/', views.tentang, name='tentang'),
    path('daftar/', views.daftar, name='daftar'),
    path('new-user/', views.new_user, name='new-user'),
    path('daftar-pasien/', login_required(views.daftar_pasien), name='daftar-pasien'),
    path('daftar-antri/', login_required(views.daftar_antri), name='daftar-antri'),
    path('antri.json', views.get_antri, name='get-antri'),
    path('times.json', login_required(views.get_times), name='get-times'),
    path('dates.json', login_required(views.get_dates), name='get-dates'),
    path('pasien.json', login_required(views.get_pasien), name='get-pasien'),
    path('masuk/', LoginView.as_view(template_name='antri/masuk.html'), name='masuk'),
    path('keluar/', LogoutView.as_view(template_name='antri/keluar.html'), name='keluar'),
    path('profil/', login_required(views.profil), name='profil'),
    path('ubah/pasien/<int:pk>/', login_required(views.ubah_pasien), name='ubah-pasien'),
    path('ubah/username/', login_required(views.ubah_username), name='ubah-username'),
    path('ubah/password/', login_required(views.ubah_password), name='ubah-password'),
    path('pasien/<int:pk>/', login_required(views.pasien_detail),
         name='pasien-detail'),
    path('hapus/pasien/', login_required(views.hapus_pasien), name='hapus-pasien'),
    path('pendaftaran/', login_required(views.pendaftaran_list), name='pendaftaran-list')
]
