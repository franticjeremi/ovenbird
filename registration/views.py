# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm, MyAuthenticationForm
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from offsite.models import Ovenbird
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
import logging
logger = logging.getLogger(__name__)

# Create your views here.
@csrf_protect
def registrationUser(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/offsite/')
    else:
        form = RegistrationForm()
    return render_to_response('registration/register.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@csrf_protect
@never_cache
def login(request):
    form = MyAuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    if user.is_staff:
                        return redirect('/admin')
                    return redirect('/offsite/')
    return render_to_response('registration/login.html', {
        'form': form,
    }, context_instance=RequestContext(request))
    
def logout(request):
    django_logout(request)
    return redirect('/offsite/')