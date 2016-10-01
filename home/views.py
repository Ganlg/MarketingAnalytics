from django.shortcuts import render, redirect, reverse


# Create your views here.
def index(request, lang='en'):
    if lang.lower() == 'en':
        return render(request, 'en/index.html', {})
    elif lang.lower() == 'cn':
        return render(request, 'cn/index.html', {})
    else:
        return redirect(reverse('home:index-lang', args=['en']))

