from django.shortcuts import render, redirect, reverse


# Create your views here.
def index(request, lang='en'):
    if lang.lower() == 'en':
        request.session["lang"] = "en"
        return render(request, 'en/index.html', {})
    elif lang.lower() == 'cn':
        request.session["lang"] = "cn"
        return render(request, 'cn/index.html', {})
    else:
        request.session["lang"] = "en"
        return redirect(reverse('home:index-lang', args=['en']))

