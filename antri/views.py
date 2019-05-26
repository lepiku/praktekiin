from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Pengguna, User, KepalaKeluarga
from .forms import DaftarPenggunaForm, DaftarKKForm, MasukForm

def utama(request):
    if request.user.is_authenticated:
        return render(request, 'antri/utama.html')
    return render(request, 'antri/bukan_utama.html')

def tentang(request):
    return render(request, 'antri/tentang.html')

def daftar(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form_pengguna = DaftarPenggunaForm(request.POST)

        if form_pengguna.is_valid():
            form_kk = DaftarKKForm(request.POST)

            if form_kk.data.get('alamat'):
                nama = form_pengguna.cleaned_data['nama']
                tanggal_lahir = form_pengguna.cleaned_data['tanggal_lahir']
                jenis_kelamin = form_pengguna.cleaned_data['jenis_kelamin']
                telp = form_pengguna.cleaned_data['telp']
                nama_kk = form_kk.data['nama_kk']
                alamat = form_kk.data['alamat']

                username = form_pengguna.cleaned_data['username']
                password = form_pengguna.cleaned_data['password']

                user = User.objects.create_user(username, '', password)
                user.save()
                kk = KepalaKeluarga(nama=nama_kk, alamat=alamat)
                kk.save()
                pengguna = Pengguna(nama=nama, tanggal_lahir=tanggal_lahir,
                        jenis_kelamin=jenis_kelamin, telp=telp,
                        kepala_keluarga=kk, user=user)
                pengguna.save()

                login(request, authenticate(request,
                        username=username, password=password))
                return HttpResponseRedirect(reverse('antri:utama'))
            return render(request, 'antri/daftar.html', {'form': form_kk})

    else:
        form_pengguna = DaftarPenggunaForm()
    return render(request, 'antri/daftar.html', {'form': form_pengguna})

def masuk(request):
    message = ""
    if request.method == 'POST':
        form = MasukForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('antri:utama'))
        else:
            message = "Salah Username atau Password"
            # Return an 'invalid login' error message.
    else:
        form = MasukForm()

    return render(request, 'antri/masuk.html',
            {'form': form, 'message': message})

def keluar(request):
    logout(request)
    return render(request, 'antri/keluar.html')
