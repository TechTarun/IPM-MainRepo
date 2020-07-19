from django.shortcuts import render
from .models import User


def index(request):
    message = ""
    return render(request, 'index/index.html', {'message' : message})

def auth(request):
    user = request.POST.get('user')
    password = request.POST.get('password')
    try:
        authName = User.objects.get(user_name=user, user_password=password).user_name
        print(authName)
        return render(request,'profill/profill.html')
    except:
        message = "Authentication Failed!! Wrong username or password"
        return render(request, 'index/index.html', {'message': message})
