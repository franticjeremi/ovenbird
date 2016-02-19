# -*- coding: utf-8 -*-
from .models import Ovenbird, Object
from django.shortcuts import render, render_to_response, redirect, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse 
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import OvenbirdForm, ObjectForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import logging
logger = logging.getLogger(__name__)
# Create your views here.
    
#class AboutView(TemplateView):
#    template_name = "jinja2/index.jinja"

# добавляет для метода диспатч декоратор проверки аутентификации
class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/registration/login'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
    
# main page
def MainPage(request):
    # creating var session, storing id ovenbird
    if request.user.is_authenticated() and 'ovenbird_id' not in request.session:
        ovenbird = Ovenbird.objects.filter(customuser_id = request.user.id).first()
        if ovenbird is not None:
            request.session['ovenbird_id'] = ovenbird.id
    
    ovenbird_list = Ovenbird.objects.all()
    paginator = Paginator(ovenbird_list, 2)
    page = request.GET.get('page')
    try:
        ovenbirds = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ovenbirds = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ovenbirds = paginator.page(paginator.num_pages)
    return render_to_response('offsite/index.html', 
        context_instance=RequestContext(request,{'ovenbirds':ovenbirds}))

class CreateOvenbird(LoginRequiredMixin, CreateView):
    template_name = "offsite/myprofile.html"
    model = Ovenbird
    form_class = OvenbirdForm

      
    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        post_values['customuser'] = request.user.id
        form = OvenbirdForm(data=post_values)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/offsite/')
        return super(CreateOvenbird, self).post(request, **kwargs)
    
class UpdateOvenbird(LoginRequiredMixin, UpdateView):
    template_name = "offsite/myprofile.html"
    form_class = OvenbirdForm
    model = Ovenbird
    
    def get_object(self):
        return Ovenbird.objects.get(customuser_id=self.request.user.id)

    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        ovenbird = Ovenbird.objects.get(customuser_id = request.user.id)
        post_values = request.POST.copy()
        post_values['customuser'] = ovenbird.customuser_id
        form = OvenbirdForm(data=post_values, instance=ovenbird)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/offsite/')
        return super(UpdateOvenbird, self).post(request, **kwargs)

    
class ShowOvenbird(ListView):
    context_object_name = 'ovenbird'
    template_name = "offsite/ovenbird.html"
    
    model = Ovenbird
    
    def get_queryset(self):
        ovenbird = get_object_or_404(Ovenbird, id = self.kwargs['ovenbird_id'])
        return ovenbird
    
    def get_context_data(self, **kwargs):
        context = super(ShowOvenbird, self).get_context_data(**kwargs)
        context['objects'] = Object.objects.filter(ovenbird_id = self.kwargs['ovenbird_id'], type = 1)
        context['articles'] = Object.objects.filter(ovenbird_id = self.kwargs['ovenbird_id'], type = 2)
        return context
    
class ShowObject(DetailView):
    model = Object
    template_name = "offsite/showobject.html"
    
    def get_context_data(self, **kwargs):
        context = super(ShowObject, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(Object,
            id = self.kwargs['pk']
        )
        return context

class CreateObject(LoginRequiredMixin, CreateView):
    template_name = "offsite/object.html"
    form_class = ObjectForm
    model = Object
    
    def get_success_url(self, ovenbird_id):
        return reverse('offsite:showovenbird', kwargs={'ovenbird_id' : ovenbird_id} )
    
    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        post_values['type'] = 1
        post_values['ovenbird'] = request.session['ovenbird_id']
        form = ObjectForm(data=post_values)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url(request.session['ovenbird_id']))
        return super(UpdateObject, self).post(request, **kwargs)
    
# update objects
class UpdateObject(LoginRequiredMixin, UpdateView):
    template_name = "offsite/object.html"
    form_class = ObjectForm
    model = Object

    def get_queryset(self):
        queryset = Object.objects.filter(
            id = self.kwargs['pk'], 
            ovenbird_id = self.request.session['ovenbird_id']
        )
        return queryset

    def get_success_url(self, ovenbird_id):
        return reverse(
            'offsite:showovenbird', 
            kwargs={'ovenbird_id' : ovenbird_id}
        )

    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        object = Object.objects.get(
            id = self.kwargs['pk'], 
            ovenbird_id = self.request.session['ovenbird_id']
        )
        post_values = request.POST.copy()
        post_values['type'] = object.type
        post_values['ovenbird'] = object.ovenbird_id
        form = ObjectForm(data=post_values, instance=object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url(object.ovenbird_id))
        return super(UpdateObject, self).post(request, **kwargs)

class DeleteObject(LoginRequiredMixin, DeleteView):
    model = Object
    
    def get_success_url(self):
        success_url = reverse(
            'offsite:showovenbird', 
            kwargs={'ovenbird_id': self.request.session['ovenbird_id']}
        )
    
    def get_queryset(self):
        queryset = Object.objects.filter(
            id = self.kwargs['pk'], 
            ovenbird_id = self.request.session['ovenbird_id']
        )
        return queryset

def CreateArticle(request):
    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['type'] = 2
        post_values['ovenbird'] = request.session['ovenbird_id']
        form = ObjectForm(data=post_values)
        if form.is_valid():
            object = form.save()
            return redirect('/offsite/')
    else:
        form = ObjectForm()
    return render_to_response('offsite/object.html', {
        'form': form,
        }, context_instance=RequestContext(request))

def ShowArticle(request, pk):
    object = get_object_or_404(Object, pk=pk)
    return render_to_response('offsite/object.html', {
        'form': form,
        }, context_instance=RequestContext(request))

