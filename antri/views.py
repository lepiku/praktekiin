from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import Pengguna, User
from .forms import CreateUserForm, MasukForm

def utama(request):
    if request.user.is_authenticated:
        return render(request, 'antri/utama.html')
    return render(request, 'antri/utama.html')

def tentang(request):
    return render(request, 'antri/tentang.html')

def daftar(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            nama = form.cleaned_data['nama']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            no_hp = form.cleaned_data['no_hp']

            user = User.objects.create_user(username, '', password)
            user.save()
            pengguna = Pengguna(user=user, nama=nama, no_hp=no_hp)
            pengguna.save()
            return HttpResponseRedirect(reverse('antri:masuk'))

    # if a GET (or any other method) we'll create a blank form
    form = CreateUserForm()

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
