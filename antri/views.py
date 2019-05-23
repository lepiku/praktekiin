from django.shortcuts import render

# Create your views here.
def utama(request):
    return render(request, 'antri/utama.html')

def masuk(request):
    return render(request, 'antri/masuk.html')

def daftar(request):
    return render(request, 'antri/daftar.html')

