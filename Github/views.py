from django.shortcuts import render
from InputOutputFiles import Speech_to_Text as listen

def Github(request):
    return render(request, 'Github/github.html', {'query':"", 'output':""})

def listenGithubQuery(request):
    query = listen.listenInput()
    return render(request, 'Github/Github.html', {'query' : query, 'output':""})

def searchGithubQuery(request):
    query = request.POST.get('query')
    output = base.getAPIOutput(query, "Github")
    speak.say(output)
    return render(request, 'Github/Github.html', {'query':query, 'output':output})