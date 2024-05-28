from django.http import HttpResponse
from django.shortcuts import render

def susi(request):
 return HttpResponse("Labas, pasauli!")


def home(request):
    return render(request, 'app/home.html')
