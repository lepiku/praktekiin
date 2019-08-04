from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import (PasienForm, PendaftaranForm, PendaftaranPasienForm,
                    UbahPasswordForm, UserForm, NAMA_BULAN)
from .models import (Hari, Jadwal, Keluarga, Pasien, Pendaftaran, Tempat,
                     User, WAKTU_CHOICES)

# from django.utils.safestring import mark_safe
# from django.utils.html import escape
# from django.views.generic.detail import DetailView
# from .utils import Calendar

NAMA_HARI = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu")


def beranda(request, year=None, month=None, day=None):
    """Homepage."""
    date = timezone.localtime(timezone.now())
    if date.weekday() == 6:
        date += timezone.timedelta(days=1)

    form = None
    if request.user.is_authenticated:
        pasien_set = request.user.pengguna.keluarga.pasien_set.all()

        if request.method == 'POST':
            form = PendaftaranPasienForm(request.POST, pasien_set=pasien_set)
            if form.is_valid():
                hari, _ = Hari.objects.get_or_create(
                    jadwal=Jadwal.objects.get(hari=date.weekday()),
                    tanggal=date.date())
                p_set = hari.pendaftaran_set.all()

                cleaned_pasien_set = form.cleaned_data['pasien_set']
                for pasien in pasien_set:
                    p_pasien = p_set.filter(pasien=pasien).exists()
                    if pasien in cleaned_pasien_set and not p_pasien:
                        Pendaftaran(pasien=pasien, hari=hari).save()
                    elif pasien not in cleaned_pasien_set and p_pasien:
                        p_set.filter(pasien=pasien).delete()
                return redirect('antri:beranda')
        else:
            form = PendaftaranPasienForm(pasien_set=pasien_set)

    context = {
        'date': '{}, {} {} {}'.format(
            NAMA_HARI[date.weekday()],
            date.day,
            NAMA_BULAN[date.month],
            date.year),
        'form': form,
        'logged_in': request.user.is_authenticated}

    return render(request, 'antri/beranda.html', context)


def get_antri(request):
    """get today's antrian."""
    if request.is_ajax():
        date = timezone.localtime(timezone.now())
        staff = False
        if request.user.is_authenticated:
            staff = request.user.is_staff

        if date.weekday() == 6:
            date += timezone.timedelta(days=1)

        hari = Hari.objects.filter(tanggal=date.date())

        if not hari.exists():
            return JsonResponse({'data': None})
        hari = hari.get()

        data = []
        if not staff:
            table_head = ['No.', 'Nama Pasien', 'Nama Kelapa Keluarga']
            for counter, pendaftaran in enumerate(hari.pendaftaran_set.all()):
                data.append({'number': counter + 1,
                             'nama': pendaftaran.pasien.nama,
                             'kk': pendaftaran.pasien.kepala_keluarga})
        else:
            table_head = ['No.', 'Nama Pasien', 'Status', 'Nama Kepala Keluarga']
            for counter, pendaftaran in enumerate(hari.pendaftaran_set.all()):
                data.append({'number': counter + 1,
                             'nama': pendaftaran.pasien.nama,
                             'status': pendaftaran.pasien.status,
                             'kk': pendaftaran.pasien.kepala_keluarga})

        return JsonResponse({
            'table_head': table_head,
            'data': data,
            'staff': staff})
    return None


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


@login_required
def daftar_antri(request):
    pasien_set = request.user.pengguna.keluarga.pasien_set.all()
    if request.method == 'POST':
        form = PendaftaranForm(request.POST, pasien_set=pasien_set)
        if form.is_valid():
            form.cleaned_data['tempat']

            jadwal = Jadwal.objects.get(
                tempat=form.cleaned_data['tempat'],
                waktu=form.cleaned_data['waktu'],
                hari=form.cleaned_data['hari'])

            hari, _ = Hari.objects.get_or_create(
                jadwal=jadwal,
                tanggal=form.cleaned_data['tanggal'])

            for pasien in form.cleaned_data['pasien_set']:
                Pendaftaran(pasien=pasien, hari=hari).save()

            return redirect('antri:beranda')
    else:
        form = PendaftaranForm(pasien_set=pasien_set)

    context = {'form': form}

    return render(request, 'antri/daftar-antri.html', context)


def get_times(request):
    '''
    return hour and day of the week of the place.
    '''
    if request.is_ajax():
        id_tempat = request.GET.get('id_tempat')
        if id_tempat != '':
            nama_hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', "Jum'at", 'Sabtu',
                         'Minggu']

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
                date = next_date + timezone.timedelta(days=num * 7)
                date_repr = '{}/{}'.format(date.day, date.month)
                total_tanggal.append({
                    'tanggal': date_repr,
                    'jumlah': 0,
                    })
            return JsonResponse({
                'tanggal': total_tanggal,
                'hari': jadwal.hari})

        return JsonResponse({'tanggal': None})
    return None


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
