from django.shortcuts import render
from .models import User


def index(request):
    message = ""
    return render(request, 'index/index.html', {'message' : message})

def auth(request):
        return render(request, 'profill/profill.html')