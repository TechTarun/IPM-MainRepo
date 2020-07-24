from django.shortcuts import render
from InputOutputFiles import Speech_to_Text as listen

def Mailsearcher(request):
    query=""
    return render(request, 'mailsearcher/mailsearcher.html', {'query':query})

def listenMailQuery(request):
    query = listen.listenInput()
    return render(request, 'mailsearcher/mailsearcher.html', {'query':query})


