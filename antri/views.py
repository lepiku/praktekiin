from django.contrib.auth import authenticate, login, update_session_auth_hash
# from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
# from django.utils.safestring import mark_safe
from django.utils import timezone
# from django.utils.html import escape
from django.views.generic.edit import UpdateView
# from django.views.generic.detail import DetailView
from .forms import UserForm, UbahPasswordForm, PasienForm
from .models import User, Pengguna, Keluarga, Pasien
# from .utils import Calendar

def utama(request, year=None, month=None, day=None):
    if not request.user.is_authenticated:
        return render(request, 'antri/bukan_utama.html')

    print('youre logged in')

    if year == None and month == None:
        now = timezone.localtime(timezone.now())
        year = now.year
        month = now.month

    # if request.method == 'POST':
    #     form = PendaftarForm(request.POST)

    #     # create Hari if doesn't exist
    #     day = int(request.POST['hari'])
    #     tanggal = timezone.datetime(int(request.POST['tahun']),
    #             int(request.POST['bulan']), day)
    #     if Hari.objects.filter(tanggal=tanggal).exists():
    #         hari = Hari.objects.get(tanggal=tanggal)
    #     else:
    #         hari = Hari.objects.create(tanggal=tanggal)
    #         hari.save()

    #     if form.is_valid():
    #         pendaftar = form.cleaned_data['pendaftar']
    #         pendaftars = pendaftar.split('\n')
    #         pendaftars = [' '.join(p.split()) for p in pendaftars]
    #         pendaftars = [p for p in pendaftars if p != '']

    #         pg = request.user.pengguna
    #         pendaftaran_set = Pendaftaran.objects.filter(
    #                 pengguna__kepala_keluarga=pg.kepala_keluarga, hari=hari)
    #         if pendaftaran_set.exists():
    #             pendaftaran_set.first().delete()

    #         if pendaftars != []:
    #             pendaftaran = Pendaftaran.objects.create(pengguna=pg, hari=hari)
    #             pendaftaran.save()

    #             for p in pendaftars:
    #                 Pendaftar(pendaftaran=pendaftaran, nama=p).save()

    # else:
    #     form = PendaftarForm()

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

    # calendar = Calendar().formatmonth(year, month)
    return render(request, 'antri/utama.html', {'data': data, 'day': day})
    # return render(request, 'antri/utama.html',
    #         {'calendar': mark_safe(calendar), 'data': data, 'form': form,
    #             'day': day})

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
            {'form': form_user, 'button_label': 'Buat Akun'})

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

    data_pasien = [p.nama for p in keluarga.pasien_set.all()]

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
            user = form.save()
            return redirect(reverse('antri:profil'))
    else:
        form = PasienForm(instance=request.user.pengguna.pasien)
    return render(request, 'antri/daftar.html',
            {'form': form, 'button_label': 'Ubah Profil'})

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
            {'form': form, 'button_label': 'Ubah Password'})

# def profil_detail(request, pk):
#     if not request.user.is_staff:
#         return redirect('{}?next=/profil/{}/'.format(reverse('antri:masuk'), pk))
#     context = {'object': Pengguna.objects.get(pk=pk)}
#     return render(request, 'antri/profil_detail.html', context)
