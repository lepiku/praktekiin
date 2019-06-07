from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Pengguna, User, KepalaKeluarga, Hari, Pendaftaran
from .forms import DaftarPenggunaForm, DaftarKKForm, UbahPasswordForm, \
        PilihKKForm
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic.edit import UpdateView
# from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from datetime import date

def utama(request):
    now = timezone.now()
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
        print(request.POST)

        if form_pengguna.is_valid():
            nama_kk = form_pengguna.cleaned_data['nama_kk']
            kode = 1
            if not KepalaKeluarga.objects.filter(nama=nama_kk) \
                    or 'new' in request.POST \
                    or request.POST['kode'] == '1':
                form_kk = DaftarKKForm(request.POST)
                # TODO error still hidden
            else:
                form_kk = PilihKKForm(request.POST, nama_kk=nama_kk)
                kode = 2

            if form_kk.is_valid(): #.data.get('alamat'):
                nama = form_pengguna.cleaned_data['nama']
                tanggal_lahir = form_pengguna.cleaned_data['tanggal_lahir']
                jenis_kelamin = form_pengguna.cleaned_data['jenis_kelamin']
                telp = form_pengguna.cleaned_data['telp']
                nama_kk = form_kk.cleaned_data['nama_kk']
                kk = request.POST.get('kk', 0)

                username = form_pengguna.cleaned_data['username']
                password = form_pengguna.cleaned_data['password']

                if not kk:
                    alamat = form_kk.cleaned_data['alamat']
                    kk = KepalaKeluarga(nama=nama_kk, alamat=alamat)
                    kk.save()
                else:
                    kk = KepalaKeluarga.objects.get(id=kk)

                user = User.objects.create_user(username, '', password)
                user.save()

                pengguna = Pengguna(nama=nama, tanggal_lahir=tanggal_lahir,
                        jenis_kelamin=jenis_kelamin, telp=telp,
                        kepala_keluarga=kk, user=user)
                pengguna.save()

                login(request, authenticate(request,
                        username=username, password=password))
                return HttpResponseRedirect(reverse('antri:utama'))

            return render(request, 'antri/daftar.html',
                    {'form': form_kk, 'kode': kode})
    else:
        form_pengguna = DaftarPenggunaForm()

    return render(request, 'antri/daftar.html',
            {'form': form_pengguna, 'kode': 0})

def details(request):
    nama_bulan = ("", "Januari", "Februari", "Maret", "April", "Mei",
            "Juni", "Juli", "Agustus", "September", "Oktober", "November",
            "Desember")

    if request.is_ajax():
        day = int(request.GET.get('day'))
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
        booked = 'Tambah'
        url = reverse('antri:tambah')

        buka = '17.00'
        tutup = '20.00'
        try:
            hari = Hari.objects.get(tanggal__day=day, tanggal__month=month,
                tanggal__year=year)

        except Hari.DoesNotExist as e:
            data = None

        else:
            data = list(hari.pendaftaran_set.all().values())
            for i in range(len(data)):
                pengguna = Pengguna.objects.get(id=data[i]['pengguna_id'])
                data[i]['nama_pendaftar'] = pengguna.nama
                if pengguna == request.user.pengguna:
                    booked = 'Kurang'
                    url = reverse('antri:kurang')
                    print(url)

            buka = hari.waktu_buka
            tutup = hari.waktu_tutup

        return JsonResponse({'data': data, 'month_name': nama_bulan[month],
            'booked': booked, 'url': url, 'buka': buka, 'tutup': tutup})

    return HttpResponseRedirect(reverse('antri:404'))

def profil(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('antri:utama'))

    user = request.user
    pengguna = user.pengguna
    kepala_keluarga = pengguna.kepala_keluarga

    data_pengguna = [
            ('Nama Lengkap', pengguna.nama),
            ('Tanggal Lahir', pengguna.tanggal_lahir),
            ('Jenis Kelamin', pengguna.jenis_kelamin),
            ('No. HP / Telp', pengguna.telp),
            ]

    data_kepala_keluarga = [
            ('Nama Kepala Keluarga', kepala_keluarga.nama),
            ('Alamat', kepala_keluarga.alamat),
            ]

    data_user = [
            ('Username', user.username),
            ]

    data = {'pengguna': data_pengguna, 'user': data_user,
            'kepala_keluarga': data_kepala_keluarga}

    return render(request, 'antri/profil.html', data)

class ProfilUpdate(UpdateView):
    model = Pengguna
    fields = ['nama', 'tanggal_lahir', 'jenis_kelamin', 'telp']
    template_name = 'antri/ubah_profil.html'

    def get_object(self):
        return self.request.user.pengguna

    def get_success_url(self):
        return reverse('antri:profil')

class KepalaKeluargaUpdate(UpdateView):
    model = KepalaKeluarga
    fields = '__all__'
    template_name = 'antri/ubah_kk.html'

    def get_object(self):
        return self.request.user.pengguna.kepala_keluarga

    def get_success_url(self):
        return reverse('antri:profil')


def ubah_password(request):
    if request.method == 'POST':
        form = UbahPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('antri:profil'))
        # else:
            # messages.error(request, 'Please correct the error below.')
    else:
        form = UbahPasswordForm(request.user)
    return render(request, 'antri/ubah_password.html', {'form': form})

def tambah(request):
    if request.method == 'POST':
        tahun = int(request.POST['tahun'])
        bulan = int(request.POST['bulan'])
        hari = int(request.POST['hari'])

        tanggal = date(year=tahun, month=bulan, day=hari)
        if Hari.objects.filter(tanggal=tanggal):
            hari = Hari.objects.get(tanggal=tanggal)
        else:
            hari = Hari.objects.create(tanggal=tanggal)
            hari.save()

        pengguna = request.user.pengguna
        tambah = Pendaftaran.objects.create(pengguna=pengguna, hari=hari)
        tambah.save()

        return HttpResponseRedirect(reverse('antri:utama_month',
            kwargs={'year':tahun, 'month':bulan}))
    # return HttpResponseRedirect(reverse('antri:utama'))

def kurang(request):
    if request.method == 'POST':

        tahun = int(request.POST['tahun'])
        bulan = int(request.POST['bulan'])
        hari = int(request.POST['hari'])

        tanggal = date(year=tahun, month=bulan, day=hari)
        hari = Hari.objects.get(tanggal=tanggal)
        pengguna = request.user.pengguna

        hari.pendaftaran_set.get(pengguna=pengguna).delete()

        return HttpResponseRedirect(reverse('antri:utama_month',
            kwargs={'year':tahun, 'month':bulan}))
    # return HttpResponseRedirect(reverse('antri:utama'))
