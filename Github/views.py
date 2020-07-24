from django.shortcuts import render

def Github(request):
    return render(request, 'Github/github.html')
def search(request):
    query = request.POST.get('query')
    return render(request, 'Github/Github.html', {'repo' : repo_list})

def listen(request):
    intro = "Hello user,I am IPM,Your Jarvis from Team intelleneur."
    return render(request, 'Github/Github.html', {'repo' : repo_list})

