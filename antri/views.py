from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Pengguna, User
from .forms import DaftarPenggunaForm, DaftarKKForm, MasukForm

def utama(request):
    if request.user.is_authenticated:
        return render(request, 'antri/utama.html')
    return render(request, 'antri/bukan_utama.html')

def tentang(request):
    return render(request, 'antri/tentang.html')

def daftar(request):
    # if this is a POST request we need to process the form data
    """

    if request.method == 'POST':
        form = CreatePenggunaForm(request.POST)
        if form.is_valid():
            # nama = form.cleaned_data['nama']
            # tanggal_lahir = form.cleaned_data['tanggal_lahir']
            # jenis_kelamin = form.cleaned_data['jenis_kelamin']
            # telp = form.cleaned_data['telp']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # TODO bikin kk, cek kk
            # user = User.objects.create_user(username, '', password)
            # user.save()
            # pengguna = Pengguna(user=user, nama=nama, telp=telp)
            # pengguna.save()

            # login(request, authenticate(request,
                    # username=username, password=password))
            return HttpResponseRedirect(reverse('antri:daftarkk'), request)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreatePenggunaForm()

    return render(request, 'antri/daftar.html', {'form': form})
    """

    if request.method == 'POST':
        form = DaftarKKForm(request.POST)
        if form.is_valid():
            nama = form.cleaned_data['nama']
            tanggal_lahir = form.cleaned_data['tanggal_lahir']
            jenis_kelamin = form.cleaned_data['jenis_kelamin']
            telp = form.cleaned_data['telp']
            nama_kk = form.cleaned_data['nama_kk']
            alamat = form.cleaned_data['alamat']

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username, '', password)
            user.save()
            kk = KepalaKeluarga(nama=nama_kk, alamat=alamat)
            kk.save()
            pengguna = Pengguna(nama=nama, tanggal_lahir=tanggal_lahir,
                    jenis_kelamin=jenis_kelamin, telp=telp, kepala_keluarga=kk,
                    user=user)
            pengguna.save()

            login(request, authenticate(request,
                    username=username, password=password))
            return HttpResponseRedirect(reverse('antri:utama'))

        form = DaftarPenggunaForm(request.POST)
        if form.is_valid():
            return render(request, 'antri/daftarkk.html')
    else:
        form = DaftarPenggunaForm()
    return render(request, 'antri/daftar.html', {'form': form})

def masuk(request):
    message = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('antri:utama'))
        else:
            message = "Salah Username atau Password"
            # Return an 'invalid login' error message.

    form = MasukForm()
    return render(request, 'antri/masuk.html',
            {'form': form, 'message': message})

def keluar(request):
    logout(request)
    return render(request, 'antri/keluar.html')
