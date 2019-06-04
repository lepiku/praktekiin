from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import UpdateView

app_name = 'antri'

urlpatterns = [
    path('', views.utama, name='utama'),
    path('<int:year>/<int:month>/', views.utama_month, name='utama_month'),
    path('masuk/', LoginView.as_view(template_name='antri/masuk.html'), name='masuk'),
    path('keluar/', LogoutView.as_view(template_name='antri/keluar.html'), name='keluar'),
    path('daftar/', views.daftar, name='daftar'),
    path('tentang/', views.tentang, name='tentang'),
    path('data.json/', views.details, name='details'),
    path('profil/', views.profil, name='profil'),
    path('ubah/profil/', views.ProfilUpdate.as_view(), name='ubah_profil'),
    path('ubah/kepala-keluarga/', views.KepalaKeluargaUpdate.as_view(), name='ubah_kk'),
    path('ubah/password/', views.ubah_password, name='ubah_password'),
]

