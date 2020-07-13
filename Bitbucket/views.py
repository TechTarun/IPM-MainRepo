# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def Bitbucket(request):
    return render(request, 'Bitbucket/Bitbucket.html')
