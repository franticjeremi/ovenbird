# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm, MyAuthenticationForm
from django.shortcuts import render_to_response, redirect
from offsite.models import Ovenbird, Adser
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
import logging
logger = logging.getLogger(__name__)

# Create your views here.
@csrf_protect
def registrationUser(request):
    if request.method == 'POST':
        post_values = request.POST.copy()
        checkbox = post_values.getlist('checkbox')
        if len(checkbox) == 2:
            post_values['is_ovenbird'] = True;
            post_values['is_adser'] = True;
        else:
            if checkbox[0] == '1':
                post_values['is_ovenbird'] = True;
            if checkbox[0] == '2':
                post_values['is_adser'] = True;
        form = RegistrationForm(data=post_values)
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
                    if user.is_adser:
                        adser = Adser.objects.get(customuser_id = user.id)
                        if adser is None:
                            Adser.objects.create(balance=0, customuser=user)
                    if user.is_ovenbird:
                        ovenbird = Ovenbird.objects.get(customuser_id = user.id)
                        if ovenbird is None:
                            return redirect('/offsite/CreateOvenbird')
                    return redirect('/offsite/')
    return render_to_response('registration/login.html', {
        'form': form,
    }, context_instance=RequestContext(request))
    
def logout(request):
    django_logout(request)
    return redirect('/offsite/')