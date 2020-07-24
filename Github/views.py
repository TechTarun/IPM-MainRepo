from django.shortcuts import render
from InputOutputFiles import Speech_to_Text as listen

def Github(request):
    return render(request, 'Github/github.html')

def listenGithubQuery(request):
    query = listen.listenInput()
    return render(request, 'Github/Github.html', {'query' : query})


