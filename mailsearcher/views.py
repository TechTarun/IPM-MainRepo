from django.shortcuts import render

def mailsearcher(request):
    text="What can I help you with today?"
    mail = ""
    return render(request, 'mailsearcher/mailsearcher.html', {'text':text, 'mail_list':mail})

def listen(request):
    intro = "Hello user,I am IPM,Your Jarvis from Team intelleneur."
    return render(request, 'mailsearcher/mailsearcher.html', {'text': text, 'mail_list':mail})

def search(request):
    query = request.POST.get('query')
    return render(request, 'mailsearcher/mailsearcher.html', {'text': text, 'mail_list':mail})


