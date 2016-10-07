from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils import timezone

from .models import User
from .forms import RegisterForm, LoginForm, ResetPasswordConfirmForm

from product.models import Service
import hashlib
import random
import datetime


# Create your views here.
def account_register(request):
    form = RegisterForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            default_service = Service.objects.get(id=1)
            new_user.service = default_service
            # randomly generate a activation key
            usernamesalt = new_user.username
            if not isinstance(usernamesalt, str):
                usernamesalt = usernamesalt.encode('utf-8')
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            new_user.activation_key = hashlib.sha1((salt+usernamesalt).encode('utf-8')).hexdigest()[0:40]
            # activation key expires in 1 day
            new_user.key_expires = datetime.datetime.strftime(
                datetime.datetime.now() + datetime.timedelta(days=1), "%Y-%m-%d %H:%M:%S"
            )
            new_user.save()

            link = 'http://' + request.META['HTTP_HOST'] + \
                   reverse('account:activate', kwargs={
                       'key': new_user.activation_key
                   })
            data = {
                'email': new_user.email,
                'site_name': 'Company',
                'user': new_user,
                'link': link
            }
            html_content = render_to_string('account/activate_email.html', data)
            send_mail('test', html_content, 'marketinganalytics2016@gmail.com', ['liugannankai@gmail.com'])
            return render(request, 'account/register_done.html', {'user': new_user})

    return render(request, 'account/register.html', {'form': form})

#
# def account_register_done(request):
#     return render(request, 'account/register_done.html')


def account_activate(request, key):
    success = False
    # try:
    user = User.objects.get(activation_key=key)
    # except:
    #     user = None
    if user is not None:

        if not user.email_verified and user.key_expires > timezone.now():
            user.email_verified = True
            user.save()
            success = True

    return render(request, 'account/activate_done.html', {'success': success})


def account_send_activation(request):
    pk = request.session.get('email_user_pk', None)
    if pk is None:
        # username and password required
        return redirect(reverse('account:login'))
    else:
        # no need to retype username and password
        user = User.objects.get(pk=pk)
        if user.email_verified:
            return redirect(reverse('home:index'))

        usernamesalt = user.username
        if not isinstance(usernamesalt, str):
            usernamesalt = usernamesalt.encode('utf-8')

        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
        user.activation_key = hashlib.sha1((salt + usernamesalt).encode('utf-8')).hexdigest()[0:40]
        # activation key expires in 1 day
        user.key_expires = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=1), "%Y-%m-%d %H:%M:%S"
        )
        user.save()

        link = 'http://' + request.META['HTTP_HOST'] + \
               reverse('account:activate', kwargs={
                   'key': user.activation_key
               })
        data = {
            'email': user.email,
            'site_name': 'Company',
            'user': user,
            'link': link
        }
        html_content = render_to_string('account/activate_email.html', data)
        send_mail('test', html_content, 'marketinganalytics2016@gmail.com', ['liugannankai@gmail.com'])
        return render(request, 'account/register_done.html', {'user': user})



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
                    request.session['email_user_pk'] = user.pk
                    return render(request, 'account/email_not_verified.html', {'user': user})
            else:
                print('wrong user')
                messages.add_message("Incorrect username or password")

    return render(request, 'account/login.html', {'form': form})


def account_forget_password(request):
    return render(request, 'account/forget_password.html', {})


def account_forget_username(request):
    return render(request, 'account/forget_username.html', {})


def account_reset_password(request):
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        try:
            user = User.objects.get(username=username, email=email)
            link = 'http://' + request.META['HTTP_HOST']+ \
                   reverse('account:reset-password-confirm', kwargs={
                       'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                       'token':default_token_generator.make_token(user)
                   })
            data = {
                'email': user.email,
                'site_name': 'Company',
                'user': user,
                'link': link
            }
            html_content = render_to_string('account/reset_password_email.html', data)
            send_mail('test', html_content, 'marketinganalytics2016@gmail.com', ['liugannankai@gmail.com'])
        except:
            pass
        return redirect(reverse('account:reset-password-done'))

    return render(request, 'account/reset_password.html')

def account_reset_password_done(request):
    return render(request, 'account/reset_password_done.html')

def account_reset_password_confirm(request, uidb64=None, token=None):

    assert uidb64 is not None and token is not None
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        form = ResetPasswordConfirmForm(request.POST or None)
        if request.POST:
            if form.is_valid():
                new_password = form.cleaned_data['password']
                user.set_password(new_password)
                user.save()
                return render(request, 'account/reset_password_confirm_done.html')

        return render(request, 'account/reset_password_confirm.html', {'form': form})
    else:
        return render(request, 'account/reset_password_confirm.html')


def account_get_username(request):
    if request.POST:
        email = request.POST['email']
        print(email)
        try:
            user = User.objects.get(email=email)
        except:
            user = None
        if user is not None:
            html_content = render_to_string('account/get_username_email.html', {'username': user.username})
            send_mail('test', html_content, 'marketinganalytics2016@gmail.com', ['liugannankai@gmail.com'])

        return render(request, 'account/get_username_done.html')

    return render(request, 'account/get_username.html')