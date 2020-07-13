from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def profill(request):
    return render(request, 'profill/profill.html')


# Create your views here.
