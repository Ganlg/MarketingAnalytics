from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.
def account_registration(request):
    lang = request.session.get("lang", "en")
    form = RegisterForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            cd = form.cleaned_data

    if lang == 'cn':
        return render(request, 'account/cn/registration.html', {'form': form})
    else:
        return render(request, 'account/base.html', {'form': form})