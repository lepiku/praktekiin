from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'antri'

urlpatterns = [
    path('', views.utama, name='utama'),
    path('<int:year>/<int:month>/', views.utama_month, name='utama_month'),
    # path('masuk/', views.masuk, name='masuk'),
    path('masuk/', auth_views.LoginView.as_view(template_name='antri/masuk.html'), name='masuk'),
    path('keluar/', views.keluar, name='keluar'),
    path('daftar/', views.daftar, name='daftar'),
    path('daftarkk/', views.daftar, name='daftarkk'),
    path('tentang/', views.tentang, name='tentang'),
    path('data.json/', views.details, name='details'),
]
