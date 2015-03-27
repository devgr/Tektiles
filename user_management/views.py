from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail

from user_management.forms import *
import user_management.utils as utils
from user_management.models import *

import random
import string

def index(request):
    if request.user.is_authenticated():
        return redirect('/user/profile')
    else:
        return redirect('/user/login')

def login_form(request, notice=None, form=None):
    if request.user.is_authenticated():
        return redirect('/user/profile')

    f = form or LoginForm()
    redirect_url = request.GET.get('next')

    if redirect_url is not None:
        f.helper.form_action += '?next=' + redirect_url

    return render(request, 'user_management/form.html',
                  {'notice': notice, 'form': f, 'title': 'Log In'})

def login_index(request, notice=None):
    if 'submit' in request.POST:
        return handle_login(request)

    return login_form(request)

def handle_login(request):
    form = LoginForm(request.POST)

    if not form.is_valid():
        return login_form(request, form=form)

    # we're now successfully authenticated, since the form validated
    login(request, form.cleaned_data.get('user'))
    if 'next' in request.REQUEST:
        return redirect(request.REQUEST['next'])
    else:
        return redirect('/user/profile')

# The best thing about this: if a user visits /user/logout and
# they're not logged in, they'll be prompted to log in, whereupon
# they'll be redirected immediately to log out.
# Hey, it's what they requested!
@login_required
def logout_user(request):
    logout(request)
    return login_form(request, 'Logged out successfully')

def changepw_form(request, notice=None, form=None):
    f = form or PasswordChangeForm(request.user)
    return render(request, 'user_management/form.html',
                  {'notice': notice, 'form': f, 'title': 'Change Password'})

@login_required
def profile(request):
    return render(request, 'user_management/profile.html')

@login_required
def changepw_index(request):
    if 'submit' in request.POST:
        return handle_password_change(request)

    return changepw_form(request)

@login_required
def handle_password_change(request):
    form = PasswordChangeForm(request.user, request.POST)

    if not form.is_valid():
        return changepw_form(request, form=form)

    new_pw = form.cleaned_data['new_password']

    request.user.set_password(new_pw)
    request.user.save()
    return changepw_form(request, 'Password updated successfully')

def register_form(request, notice=None, form=None):
    f = form or RegistrationForm()
    return render(request, 'user_management/form.html',
                  {'notice': notice, 'form': f, 'title': 'Register'})

def register_index(request):
    if 'submit' in request.POST:
        return handle_registration(request)

    return register_form(request)

def handle_registration(request):
    form = RegistrationForm(request.POST)

    if not form.is_valid():
        return register_form(request, form=form)

    user = form.save()
    user.is_active = False # Not active until email is confirmed
    user.set_password(form.cleaned_data.get('password'))
    user.save()

    user_profile = UserProfile()
    user_profile.user = user

    user_profile.confirmation_code = ''.join(
        random.choice(string.ascii_letters + string.digits)
        for x in range(33)
    )

    user_profile.save()

    title = "Textile Fabric Consultants, Inc. Account Activation"
    # TODO: Change this domain
    content = """Someone has recently registered at Textilefabric.com. We hope it was you.
    If so, please follow the link below. If not please disregard this email.\n
    """ + "theftp.dyndns.org:8000/user/activate/" + str(user_profile.confirmation_code) + "/" + user.username
    send_mail(title, content, 'no-reply@gsick.com', [user.email], fail_silently=False)

    return login_form(request,
                      '''Your account has been registered. Please
                      verify your email by clicking on the link
                      sent to you.''')

def activate(request, confirmation_code, username):
    user = User.objects.get(username=username)
    profile = user.get_profile()
    if profile.confirmation_code == confirmation_code:
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
    return redirect('/')

def change_email_form(request, notice=None, form=None):
    f = form or EmailChangeForm(instance=request.user)
    return render(request, 'user_management/form.html',
                  {'notice': notice, 'form': f, 'title': 'Change Email'})

@login_required
def change_email_index(request):
    if 'submit' in request.POST:
        return handle_email_change(request)

    return change_email_form(request)

@login_required
def handle_email_change(request):
    form = EmailChangeForm(request.POST, instance=request.user)

    if not form.is_valid():
        return change_email_form(request, form=form)

    form.save()

    return change_email_form(request, 'Successfully changed email')

@login_required
def order_history(request):
    # To be implemented
    user_profile = request.user.get_profile()
    orders = user_profile.order_set.all()
    return HttpResponse(len(orders))
