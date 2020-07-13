# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import query_searcher
import web_text2speech as t2s
import web_speech2text as s2t
import create_email

def Github(request):
    repo_list = []
    return render(request, 'Github/Github.html', {'repo' : repo_list})

def search(request):
    query = request.POST.get('query')
    repo_list = query_searcher.execute(query)
    if('mail' in query or 'email' in query):
        create_email.send_mail(repo_list)
    return render(request, 'Github/Github.html', {'repo' : repo_list})

def listen(request):
    intro = "Hello user,I am IPM,Your Jarvis from Team intelleneur."
    t2s.say(intro)
    t2s.say("Speak your query")
    text = s2t.listen()
    repo_list = []
    repo_list = query_searcher.execute(text)
    if('mail' in text or 'email' in text):
        create_email.send_mail(repo_list)
    return render(request, 'Github/Github.html', {'repo' : repo_list})