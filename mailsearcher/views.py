from django.shortcuts import render
import web_speech2text as s2t
import web_text2speech as t2s
import email_searcher as esearch

def mailsearcher(request):
    text="What can I help you with today?"
    mail = ""
    return render(request, 'mailsearcher/mailsearcher.html', {'text':text, 'mail_list':mail})

def listen(request):
    intro = "Hello user,I am IPM,Your Jarvis from Team intelleneur."
    t2s.say(intro)
    t2s.say("Speak your query")
    text = s2t.listen()
    mail = esearch.main(text, [])
    return render(request, 'mailsearcher/mailsearcher.html', {'text': text, 'mail_list':mail})

def search(request):
    query = request.POST.get('query')
    mail = esearch.main(query, [])
    text = ""
    return render(request, 'mailsearcher/mailsearcher.html', {'text': text, 'mail_list':mail})


