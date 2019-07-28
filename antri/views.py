from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import PasienForm, PendaftaranForm, UbahPasswordForm, UserForm
from .models import (WAKTU_CHOICES, Hari, Jadwal, Keluarga, Pasien, Tempat,
                     User, Pendaftaran)

# from django.utils.safestring import mark_safe
# from django.utils.html import escape
# from django.views.generic.detail import DetailView
# from .utils import Calendar

DEFAULT_WAKTU = {
        'PG': ('08:00', '12:00'),
        'SG': ('13:00', '16:00'),
        'SR': ('16:00', '20:00'),
        }
nama_bulan = ("", "Januari", "Februari", "Maret", "April", "Mei",
              "Juni", "Juli", "Agustus", "September", "Oktober",
              "November", "Desember")


def beranda(request, year=None, month=None, day=None):
    """Homepage."""
    if not request.user.is_authenticated:
        return render(request, 'antri/bukan_utama.html')

    date = timezone.localtime(timezone.now())

    context = {
        'date': '{} {} {}'.format(
            date.day,
            nama_bulan[date.month],
            date.year),
        }

    return render(request, 'antri/beranda.html', context)


def get_antri(request):
    if request.is_ajax():
        date = timezone.localtime(timezone.now())
        if date.weekday() == 6:
            date += timezone.timedelta(days=1)

        hari = Hari.objects.filter(tanggal=date.date())

        if not hari.exists():
            return JsonResponse({'data': None})
        hari = hari.first()

        return JsonResponse({
            'data': 1,
            })
    return None


@login_required
def daftar_antri(request):
    pasien_set = request.user.pengguna.keluarga.pasien_set.all()
    if request.method == 'POST':
        form = PendaftaranForm(request.POST, pasien_set=pasien_set)
        if form.is_valid():
            print('VALID')
            print(request.POST)
            form.cleaned_data['tempat']

            jadwal = Jadwal.objects.get(
                tempat=form.cleaned_data['tempat'],
                waktu=form.cleaned_data['waktu'],
                hari=form.cleaned_data['hari'])

            hari, _ = Hari.objects.get_or_create(
                jadwal=jadwal,
                tanggal=form.cleaned_data['tanggal'])

            pendaftaran = Pendaftaran(
                user=request.user,
                hari=hari)
            pendaftaran.save()
            pendaftaran.pasien_set.set(form.cleaned_data['pasien_set'])

            return redirect('antri:beranda')
        else:
            print('NOT VALID')
            print(form.errors)
    else:
        form = PendaftaranForm(pasien_set=pasien_set)

    context = {'form': form}

    return render(request, 'antri/daftar-antri.html', context)

def tentang(request):
    return render(request, 'antri/tentang.html')

def daftar(request):
    if request.method == 'POST':
        user = User()

        form_user = UserForm(request.POST, instance=user)
        if form_user.is_valid():
            user.keluarga = Keluarga()
            form_user.save()

            login(request, user)
            return redirect(reverse('antri:utama'))
    else:
        form_user = UserForm()

    return render(request, 'antri/daftar.html',
                  {'form': form_user, 'button': 'Buat Akun'})


def get_times(request):
    '''
    return hour and day of the week of the place.
    '''
    if request.is_ajax():
        id_tempat = request.GET.get('id_tempat')
        if id_tempat != '':
            print(id_tempat)
            nama_hari = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

            tempat = Tempat.objects.get(id=id_tempat)
            id_hari = []
            total_hari = []
            total_jadwal = {}

            for x in range(6):
                if tempat.jadwal_set.filter(hari=x).exists():
                    total_hari.append(nama_hari[x])
                    id_hari.append(x)

            for waktu, nama_waktu in WAKTU_CHOICES:
                if tempat.jadwal_set.filter(waktu=waktu).exists():
                    total_jadwal[nama_waktu] = []

                    for ha in id_hari:
                        query = tempat.jadwal_set.filter(waktu=waktu, hari=ha)

                        if query.exists():
                            jadwal = query.first()
                            data = {
                                'id': jadwal.id,
                                'jam': jadwal.get_waktu_ms(),
                                }
                            total_jadwal[nama_waktu].append(data)

            print(total_jadwal)

            return JsonResponse({'hari': total_hari, 'jadwal': total_jadwal})
        return JsonResponse({'hari': None})
    return None


def get_dates(request):
    if request.is_ajax():
        id_jadwal = request.GET.get('id_jadwal')
        jadwal = Jadwal.objects.filter(id=id_jadwal)
        if jadwal.exists():
            jadwal = jadwal.first()
            total_tanggal = []
            next_date = jadwal.get_next_date()
            for num in range(6):
                total_tanggal.append({
                    'tanggal': next_date + timezone.timedelta(days=num * 7),
                    'jumlah': 0,
                    })
            return JsonResponse({'tanggal': total_tanggal})

        return JsonResponse({'tanggal': None})
    return None


def details(request):
    """
    Show the names who booked that day.
    """
    nama_bulan = ("", "Januari", "Februari", "Maret", "April", "Mei",
                  "Juni", "Juli", "Agustus", "September", "Oktober",
                  "November", "Desember")

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
    keluarga = pengguna.keluarga

    if pengguna.pasien != None:
        data_pengguna = [
            ('Nama Lengkap', pengguna.pasien.nama),
            ('Tanggal Lahir', pengguna.pasien.tanggal_lahir),
            ('Jenis Kelamin', pengguna.pasien.jenis_kelamin),
            ('No. HP / Telp', pengguna.pasien.telp),
            ('NIK', pengguna.pasien.nik),
            ('MRID', pengguna.pasien.mrid)]
    else:
        data_pengguna = []

    data_pasien = [{'nama': p.nama, 'pk': p.pk} for p in keluarga.pasien_set.all()]

    data_user = [
        ('Username', user.username),
        ('Email', user.email),
        ]

    data = {'pengguna': data_pengguna, 'user': data_user,
            'pasien': data_pasien}

    return render(request, 'antri/profil.html', data)

def ubah_profil(request):
    if request.method == 'POST':
        form = PasienForm(request.POST, instance=request.user.pengguna.pasien)
        if form.is_valid():
            form.save()
            return redirect(reverse('antri:profil'))
    else:
        form = PasienForm(instance=request.user.pengguna.pasien)
    return render(request, 'antri/daftar.html',
                  {'form': form, 'button': 'Ubah Profil'})

def ubah_password(request):
    if request.method == 'POST':
        form = UbahPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect(reverse('antri:profil'))
    else:
        form = UbahPasswordForm(request.user)
    return render(request, 'antri/daftar.html',
                  {'form': form, 'button': 'Ubah Password'})

def pasien_daftar(request):
    if request.method == 'POST':
        pasien = Pasien()
        form = PasienForm(request.POST, instance=pasien)
        if form.is_valid():
            pasien.mrid = '000102' # TODO generate mrid
            pasien.keluarga = request.user.pengguna.keluarga
            form.save()
            return redirect(reverse('antri:profil'))
    else:
        form = PasienForm()
    return render(request, 'antri/daftar.html',
                  {'form': form, 'button': 'Buat Pasien'})

def pasien_detail(request, pk):
    if not request.user.is_staff:
        return redirect('{}?next=/profil/{}/'.format(reverse('antri:masuk'), pk))
    return render(request, 'antri/pasien_detail.html',
            {'pasien': get_object_or_404(Pasien, pk=pk)})
