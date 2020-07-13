from django.shortcuts import render
from django.http import HttpResponse
from .models import User
import web_text2speech as t2s
# Create your views here.

def index(request):
    message = ""
    return render(request, 'index/index.html', {'message' : message})

def auth(request):
    user = request.POST.get('user')
    password = request.POST.get('password')
    try:
        authName = User.objects.get(user_name=user, user_password=password).user_name
        print(authName)
        message = "Hello user,I am IPM, Your Jarvis from Team Intelleneur. I am a smart voice assistant, that can help you do various tasks on platforms like Github. Jira, Bitbucket and Confluence. Press IPM to begin!!"
        t2s.say(message)
        return render(request, 'profill/profill.html')
    except:
        message = "Authentication Failed!! Wrong username or password"
        t2s.say(message)
        return render(request, 'index/index.html', {'message': message})
