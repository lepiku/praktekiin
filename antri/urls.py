from django.urls import path
from . import views

app_name = 'antri'

urlpatterns = [
    path('', views.homepage, name='homepage'),
]
