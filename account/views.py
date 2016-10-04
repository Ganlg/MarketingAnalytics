from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm


# Create your views here.
def account_register(request):
    form = RegisterForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            cd = form.cleaned_data

    return render(request, 'account/register.html', {'form': form})

def account_login(request):
    form = LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.email_verified:
                    # login successfully
                    login(request, user)
                    pass
                else:
                    # email has not been verified
                    messages.add_message("Please validate your email address first")
            else:
                messages.add_message("Incorrect username or password")

    return render(request, 'account/login.html', {'form': form})

