from django.shortcuts import render

def Github(request):
    return render(request, 'Github/github.html')
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
    repo_list = query_searcher.execute(text)
    if('mail' in text or 'email' in text):
        create_email.send_mail(repo_list)
    return render(request, 'Github/Github.html', {'repo' : repo_list})

