from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required

app_name = 'antri'

urlpatterns = [
    path('', views.utama, name='utama'),
    path('tentang/', views.tentang, name='tentang'),
    path('daftar/', views.daftar, name='daftar'),
    path('masuk/', LoginView.as_view(template_name='antri/masuk.html'),
        name='masuk'),
    path('keluar/', LogoutView.as_view(template_name='antri/keluar.html'),
        name='keluar'),
    path('profil/', login_required(views.profil), name='profil'),
    path('ubah/profil/', login_required(views.ubah_profil), name='ubah_profil'),
    path('ubah/password/', login_required(views.ubah_password), name='ubah_password'),
    path('pasien/daftar/', login_required(views.pasien_daftar), name='pasien_daftar'),
    path('pasien/<int:pk>/', login_required(views.pasien_detail),
        name='pasien_detail'),
]
