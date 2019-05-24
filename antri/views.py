from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import CreateUserForm
from django.urls import reverse

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
            return HttpResponseRedirect(reverse('antri:masuk'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateUserForm()

    return render(request, 'antri/daftar.html', {'form': form})
