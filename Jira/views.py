from django.shortcuts import render
from InputOutputFiles import Speech_to_Text as listen

def Jira(request):
    return render(request, 'Jira/Jira.html', {'query':""})

def listenJiraQuery(request):
    query = listen.listenInput()
    return render(request, 'Jira/Jira.html', {'query':query})

