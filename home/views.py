from django.shortcuts import render, redirect, reverse


# Create your views here.
def index(request):
    if 'lang' not  in request.session:
        request.session['lang'] = 'en'

    return render(request, 'home/index.html', {})


def set_language(request, lang='en'):
    if lang.lower() == 'en':
        request.session["lang"] = "en"
    elif lang.lower() == 'cn':
        request.session["lang"] = "cn"
    else:
        request.session["lang"] = "en"
    return redirect(reverse('home:index'))