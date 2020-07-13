# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def Confluence(request):
    return render(request, 'Confluence/Confluence.html')
