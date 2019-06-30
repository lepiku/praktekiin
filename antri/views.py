from django.contrib.auth import authenticate, login, logout, \
        update_session_auth_hash
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.utils.html import escape
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

from .forms import DaftarPenggunaForm, DaftarKKForm, PilihKKForm, \
        UbahPasswordForm, PendaftarForm
from .models import Pengguna, User, KepalaKeluarga, Hari, Pendaftaran, \
        Pendaftar
from .utils import Calendar

def utama(request, year=None, month=None, day=None):
    if not request.user.is_authenticated:
        return render(request, 'antri/bukan_utama.html')

    if year == None and month == None:
        now = timezone.now()
        year = now.year
        month = now.month

    if request.method == 'POST':
        form = PendaftarForm(request.POST)

        # create Hari if doesn't exist
        day = int(request.POST['hari'])
        tanggal = timezone.datetime(int(request.POST['tahun']),
                int(request.POST['bulan']), day)
        if Hari.objects.filter(tanggal=tanggal).exists():
            hari = Hari.objects.get(tanggal=tanggal)
        else:
            hari = Hari.objects.create(tanggal=tanggal)
            hari.save()

        if form.is_valid():
            pendaftar = form.cleaned_data['pendaftar']
            pendaftars = pendaftar.split('\n')
            pendaftars = [' '.join(p.split()) for p in pendaftars]
            pendaftars = [p for p in pendaftars if p != '']

            pg = request.user.pengguna
            pendaftaran_set = Pendaftaran.objects.filter(
                    pengguna__kepala_keluarga=pg.kepala_keluarga, hari=hari)
            if pendaftaran_set.exists():
                pendaftaran_set.first().delete()

            if pendaftars != []:
                pendaftaran = Pendaftaran.objects.create(pengguna=pg, hari=hari)
                pendaftaran.save()

                for p in pendaftars:
                    Pendaftar.objects.create( pendaftaran=pendaftaran, nama=p)\
                            .save()

    else:
        form = PendaftarForm()

    prev_month = month - 1
    next_month = month + 1
    prev_year = next_year = year
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    elif month == 12:
        next_month = 1
        next_year = year + 1

    data = {'month': month, 'year': year,
            'prev_year': prev_year, 'prev_month': prev_month,
            'next_year': next_year, 'next_month': next_month}

    calendar = Calendar().formatmonth(year, month)
    return render(request, 'antri/utama.html',
            {'calendar': mark_safe(calendar), 'data': data, 'form': form,
                'day': day})

def tentang(request):
    return render(request, 'antri/tentang.html')

def daftar(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form_pengguna = DaftarPenggunaForm(request.POST)

        if form_pengguna.is_valid():
            nama_kk = form_pengguna.cleaned_data['nama_kk']

            # TODO error still hidden
            if not KepalaKeluarga.objects.filter(nama=nama_kk).exists() \
                    or 'new' in request.POST or 'alamat' in request.POST:
                form_kk = DaftarKKForm(request.POST)
                kode = 1
            else:
                form_kk = PilihKKForm(request.POST, nama_kk=nama_kk)
                kode = 2

            if form_kk.is_valid():
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
                return redirect(reverse('antri:utama'))

            return render(request, 'antri/daftar.html',
                    {'form': form_kk, 'kode': kode})
    else:
        form_pengguna = DaftarPenggunaForm()

    return render(request, 'antri/daftar.html',
            {'form': form_pengguna, 'kode': 0})

def details(request):
    """
    Show the names who booked that day.
    """
    nama_bulan = ("", "Januari", "Februari", "Maret", "April", "Mei",
            "Juni", "Juli", "Agustus", "September", "Oktober", "November",
            "Desember")

    if request.is_ajax():
        day = int(request.GET.get('day'))
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
        pendaftars_kk = []
        # url = reverse('antri:tambah')

        buka = '17:00'
        tutup = '20:00'
        try:
            hari = Hari.objects.get(tanggal__day=day, tanggal__month=month,
                tanggal__year=year)

        except Hari.DoesNotExist as e:
            data = None

        else:
            data = []
            for q in hari.pendaftaran_set.all().order_by('waktu_daftar'):
                kk = q.pengguna.kepala_keluarga
                option = pengguna = pengguna_id = None

                pendaftars = [p.nama for p in q.pendaftar_set.all()]

                if kk == request.user.pengguna.kepala_keluarga:
                    pendaftars_kk = pendaftars
                    option = 1

                if request.user.is_staff:
                    pengguna = str(q.pengguna)
                    pengguna_id = q.pengguna.id

                data.append({
                    'kepala_keluarga': kk.nama,
                    'pengguna': pengguna,
                    'pengguna_id': pengguna_id,
                    'pendaftars': pendaftars,
                    'option': option})

            buka = hari.waktu_buka
            tutup = hari.waktu_tutup

        return JsonResponse({
            'data': data, 'month_name': nama_bulan[month], 'buka': buka,
            'tutup': tutup, 'pendaftar': '\n'.join(pendaftars_kk)})

    raise Http404('no data on views.details')

def profil(request):
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
    template_name = 'antri/ubah.html'
    extra_context = {'button_label': 'Ubah Profil'}

    def get_object(self):
        return self.request.user.pengguna

    def get_success_url(self):
        return reverse('antri:profil')

class KepalaKeluargaUpdate(ProfilUpdate):
    model = KepalaKeluarga
    fields = '__all__'
    template_name = 'antri/ubah.html'
    extra_context = {'button_label': 'Ubah Kepala Keluarga'}

    def get_object(self):
        return self.request.user.pengguna.kepala_keluarga

def ubah_password(request):
    if request.method == 'POST':
        form = UbahPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect(reverse('antri:profil'))
    else:
        form = UbahPasswordForm(request.user)
    return render(request, 'antri/ubah.html',
            {'form': form, 'button_label': 'Ubah Password'})

def profil_detail(request, pk):
    if not request.user.is_staff:
        return redirect('{}?next=/profil/{}/'.format(reverse('antri:masuk'), pk))
    context = {'object': Pengguna.objects.get(pk=pk)}
    return render(request, 'antri/profil_detail.html', context)
