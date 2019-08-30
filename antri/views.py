from django.contrib.auth import login, update_session_auth_hash
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from .forms import (PasienForm, PendaftaranForm, PendaftaranPasienForm,
                    UbahPasswordForm, UbahUsernameForm, UserForm, NAMA_BULAN)
from .models import (Hari, Jadwal, Keluarga, Pasien, Pendaftaran, Pengguna,
                     Tempat, User, WAKTU_CHOICES)

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
        pasien_set = []
        if request.user.is_authenticated:
            staff = request.user.is_staff

        if date.weekday() == 6:
            date += timezone.timedelta(days=1)

        hari = Hari.objects.filter(tanggal=date.date())

        if not hari.exists() or not hari.get().pendaftaran_set.exists():
            return JsonResponse({'data': None})
        hari = hari.get()

        if request.user.is_authenticated:
            kel = request.user.pengguna.keluarga
            for pend in hari.pendaftaran_set.filter(pasien__keluarga=kel):
                pasien_set.append(pend.pasien.id)

        data = []
        if not staff:
            table_head = ['No.', 'Nama Pasien', 'Nama Kepala Keluarga']
            for counter, pendaftaran in enumerate(hari.pendaftaran_set.all()):
                data.append({'number': counter + 1,
                             'nama': pendaftaran.pasien.nama,
                             'kk': pendaftaran.pasien.kepala_keluarga})
        else:
            table_head = ['No.', 'Nama Pasien', 'Status', 'Nama Kepala Keluarga']
            for counter, pendaftaran in enumerate(hari.pendaftaran_set.all()):
                data.append({
                    'number': counter + 1,
                    'pasien_url': reverse('antri:pasien-detail',
                                          kwargs={'pk': pendaftaran.pasien.pk}),
                    'nama': pendaftaran.pasien.nama,
                    'status': pendaftaran.pasien.status,
                    'kk': pendaftaran.pasien.kepala_keluarga})

        return JsonResponse({
            'table_head': table_head,
            'data': data,
            'staff': staff,
            'pasien_set': pasien_set})
    return None


def tentang(request):
    return render(request, 'antri/tentang.html')


def daftar(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            user = User()

            form_user = UserForm(request.POST, instance=user)
            if form_user.is_valid():
                user = form_user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('antri:new-user')
        else:
            form_user = UserForm()

        return render(request, 'antri/daftar.html', {
            'form': form_user,
            'button': 'Buat Akun',
            'card_title': 'Daftar Pengguna',
            'card_desc': 'Username dan password digunakan untuk masuk kembali sebagai Pengguna.',
            })

    context = {'pasien_set': request.user.pengguna.keluarga.pasien_set.all()}
    return render(request, 'antri/daftar-pasien-list.html', context)


def new_user(request):
    if request.user.is_authenticated and not hasattr(request.user, 'pengguna'):
        keluarga = Keluarga()
        keluarga.save()
        pengguna = Pengguna(user=request.user, keluarga=keluarga)
        pengguna.save()

    return redirect('antri:daftar')


def daftar_pasien(request):
    prev = request.GET.get('prev', reverse('antri:profil'))
    if request.method == 'POST':
        pasien = Pasien()
        form = PasienForm(request.POST, instance=pasien)
        if form.is_valid():
            pasien.mrid = '000102' # TODO generate mrid
            pasien.keluarga = request.user.pengguna.keluarga
            form.save()
            return redirect(prev)
    else:
        form = PasienForm()

    return render(request, 'antri/daftar.html', {
        'form': form,
        'button': 'Buat Pasien',
        'card_title': 'Daftar Pasien',
        'card_desc': 'Mengisi data diri seorang pasien.',
        })


def daftar_antri(request):
    pasien_set = request.user.pengguna.keluarga.pasien_set.all()
    if request.method == 'POST':
        form = PendaftaranForm(request.POST, pasien_set=pasien_set)
        if form.is_valid():
            jadwal = form.cleaned_data['jadwal']

            hari, _ = Hari.objects.get_or_create(
                jadwal=jadwal,
                tanggal=form.cleaned_data['tanggal'])

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
        form = PendaftaranForm(pasien_set=pasien_set)

    context = {'form': form}

    return render(request, 'antri/daftar-antri.html', context)


def get_times(request):
    '''
    return hour and day of the week of the place.
    '''
    if request.is_ajax():
        id_tempat = request.GET.get('id_tempat')
        try:
            tempat = Tempat.objects.get(id=id_tempat)
        except Tempat.DoesNotExist:
            return JsonResponse({'html': None})
        else:
            nama_hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', "Jum'at", 'Sabtu',
                         'Minggu']
            id_hari = []
            total_hari = []
            total_jadwal = {}

            for index in range(6):
                if tempat.jadwal_set.filter(hari=index).exists():
                    total_hari.append(nama_hari[index])
                    id_hari.append(index)

            for waktu, nama_waktu in WAKTU_CHOICES:
                if tempat.jadwal_set.filter(waktu=waktu).exists():
                    total_jadwal[nama_waktu] = []

                    for hari in id_hari:
                        query = tempat.jadwal_set.filter(waktu=waktu, hari=hari)

                        if query.exists():
                            jadwal = query.first()
                            data = {
                                'id': jadwal.id,
                                'jam': jadwal.get_waktu_ms(),
                                }
                            total_jadwal[nama_waktu].append(data)

            html = render_to_string(
                'antri/ajax/waktu.html',
                {'total_hari': total_hari, 'jadwal': total_jadwal})
            return JsonResponse({'html': html})
    return None


def get_dates(request):
    if request.is_ajax():
        id_jadwal = request.GET.get('id_jadwal')
        try:
            jadwal = Jadwal.objects.get(id=id_jadwal)
        except Jadwal.DoesNotExist:
            return JsonResponse({'html': None})
        else:
            total_tanggal = []
            next_date = jadwal.get_next_date()
            for num in range(6):
                date = next_date + timezone.timedelta(days=num * 7)
                total_tanggal.append({
                    'tanggal': date,
                    'jumlah': 0, # TODO and implementation
                    })

            html = render_to_string(
                'antri/ajax/dates.html',
                {'total_tanggal': total_tanggal})
            return JsonResponse({'html': html})
    return None


def get_pasien(request):
    if request.is_ajax():
        kel = request.user.pengguna.keluarga
        tanggal = request.GET.get('tanggal')
        try:
            p_set = Pendaftaran.objects.filter(hari__tanggal=tanggal,
                                               pasien__keluarga=kel)
        except ValidationError:
            return JsonResponse({'pasien_set': None})
        else:
            pasien_set = []
            for pend in p_set:
                pasien_set.append(pend.pasien.id)

            return JsonResponse({'pasien_set': pasien_set})
    return None


def profil(request):
    return render(request, 'antri/profil.html')

def ubah_pasien(request, pk):
    prev = request.GET.get('prev', reverse('antri:profil'))
    pasien = get_object_or_404(request.user.pengguna.keluarga.pasien_set.all(),
                               pk=pk)
    if request.method == 'POST':
        form = PasienForm(request.POST, instance=pasien)
        if form.is_valid():
            form.save()
            return redirect(prev)
    else:
        form = PasienForm(instance=pasien)

    return render(request, 'antri/daftar.html', {
        'form': form,
        'button': 'Ubah Pasien',
        'card_title': 'Ubah Pasien',
        'card_desc': 'Mengubah data diri seorang pasien.',
        })


def ubah_username(request):
    prev = request.GET.get('prev', reverse('antri:profil'))
    if request.method == 'POST':
        form = UbahUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(prev)
    else:
        form = UbahUsernameForm(instance=request.user)

    return render(request, 'antri/daftar.html', {
        'form': form,
        'button': 'Simpan',
        'card_title': 'Ubah Username',
        })


def ubah_password(request):
    if request.user.social_auth.exists():
        return redirect(reverse('antri:masuk') + '?next=' + request.path)

    if request.method == 'POST':
        form = UbahPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect(reverse('antri:profil'))
    else:
        form = UbahPasswordForm(request.user)
    return render(request, 'antri/daftar.html', {
        'form': form,
        'button': 'Simpan',
        'card_title': 'Ubah Password',
        })


def pasien_detail(request, pk):
    pasien = get_object_or_404(Pasien, pk=pk)
    if (not request.user.is_staff
            and pasien.keluarga != request.user.pengguna.keluarga):
        return redirect('{}?next=/profil/{}/'.format(reverse('antri:masuk'), pk))

    data_pasien = [
        ('Nama Lengkap', pasien.nama),
        ('Tanggal Lahir', pasien.tanggal_lahir),
        ('Jenis Kelamin', pasien.jenis_kelamin),
        ('No. HP / Telp', pasien.telp),
        ('NIK', pasien.nik),
        ('MRID', pasien.mrid),
        ('Nama Kepala Keluarga', pasien.kepala_keluarga)]

    return render(request, 'antri/pasien_detail.html',
            {'data': data_pasien})


def hapus_pasien(request):
    pasien = get_object_or_404(request.user.pengguna.keluarga.pasien_set.all(),
                               pk=request.GET.get('id'))
    pasien.delete()
    return redirect('antri:profil')
