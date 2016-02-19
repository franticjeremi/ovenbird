# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm, MyAuthenticationForm
from django.shortcuts import render_to_response, redirect
from offsite.models import Ovenbird
from django.template import RequestContext
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

def login(request):
    if request.method == 'POST':
        form = MyAuthenticationForm(data=request.POST)
        logger.warning(request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    ovenbird = Ovenbird.objects.filter(customuser_id = user.id).first()
                    django_login(request, user)
                    if ovenbird is None:
                        return redirect('/offsite/CreateOvenbird')
                    return redirect('/offsite/')
                        
    else:
        form = MyAuthenticationForm()
    return render_to_response('registration/login.html', {
        'form': form,
    }, context_instance=RequestContext(request))
    
def logout(request):
    django_logout(request)
    return redirect('/offsite/')