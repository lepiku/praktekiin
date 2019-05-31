from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Pengguna, User, KepalaKeluarga, Hari
from .forms import DaftarPenggunaForm, DaftarKKForm
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from datetime import datetime

def utama(request):
    now = datetime.now()
    return utama_month(request, now.year, now.month)

def utama_month(request, year, month):
    prev_month = month - 1
    next_month = month + 1
    prev_year = next_year = year
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    elif month == 12:
        next_month = 1
        next_year = year + 1

    data = {'prev_year': prev_year, 'prev_month': prev_month,
            'next_year': next_year, 'next_month': next_month}

    if request.user.is_authenticated:
        calendar = Calendar().formatmonth(year, month)
        return render(request, 'antri/utama.html', {'calendar': mark_safe(calendar),
            'data': data})
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
            return render(request, 'antri/daftar.html',
                    {'form': form_kk, 'kk': True})

    else:
        form_pengguna = DaftarPenggunaForm()
    return render(request, 'antri/daftar.html',
            {'form': form_pengguna, 'kk': False})

def details(request):
    if request.is_ajax():
        day = int(request.GET.get('day'))
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))

        try:
            data = list(Hari.objects.get(
                    tanggal__day=day,
                    tanggal__month=month,
                    tanggal__year=year).pendaftaran_set.all().values())
        except Hari.DoesNotExist as e:
            return JsonResponse({'data': None})
        for i in range(len(data)):
            data[i]['nama_pendaftar'] = Pengguna.objects.get(id=data[i]['pengguna_id']).nama
        return JsonResponse({'data': data})

    return JsonResponse({'data': None})
