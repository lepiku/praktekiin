from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import CreateUserForm
from django.urls import reverse
from .models import Pengguna, User, Phone

# Create your views here.
def utama(request):
    return render(request, 'antri/utama.html')

def masuk(request):
    return render(request, 'antri/masuk.html')

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
            phone = Phone(phone_number=no_hp)
            phone.save()
            pengguna = Pengguna(user=user, nama=nama, no_hp=phone)
            pengguna.save()
            return HttpResponseRedirect(reverse('antri:masuk'))
        else:
            print('form is not valid')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateUserForm()

    return render(request, 'antri/daftar.html', {'form': form})
