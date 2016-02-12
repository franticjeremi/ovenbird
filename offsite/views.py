from .models import Ovenbird, Object
from django.shortcuts import render, render_to_response, redirect, get_object_or_404, HttpResponseRedirect
from django.core.urlresolvers import reverse 
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
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

def MainPage(request):
    if request.user.is_authenticated() and 'ovenbird_id' not in request.session:
        ovenbird = Ovenbird.objects.get(customuser_id = request.user.id)
        if ovenbird:
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

def ChangeOvenbird(request):
    object_to_edit = get_object_or_404(Ovenbird,customuser_id=request.user.id)
    if request.method == 'POST':
        form = OvenbirdForm(data=request.POST, instance=object_to_edit)
        user = form.save()
        return redirect('/offsite/')
    else:
        form = OvenbirdForm()
    return render_to_response('offsite/myprofile.html', {
        'form': form,
        }, context_instance=RequestContext(request))
    
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
    
def ShowObject(request, pk):
    object = get_object_or_404(Object, pk=pk)
    return render_to_response('offsite/object.html', {
        'form': form,
        }, context_instance=RequestContext(request))
     
def CreateObject(request):
    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['type'] = 1
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

class UpdateObject(UpdateView):
    template_name = "offsite/object.html"
    form_class = ObjectForm
    model = Object

    @method_decorator(login_required(login_url='/registration/login'))
    def dispatch(self, request, *args, **kwargs):
        queryset = Object.objects.filter(ovenbird_id = request.session['ovenbird_id'])
        self.object = get_object_or_404(queryset, id = self.kwargs['pk'])
        return super(UpdateObject, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self, ovenbird_id):
        return reverse('offsite:showovenbird', kwargs={'ovenbird_id' : ovenbird_id} )
    
    def get(self, request, *args, **kwargs):
        queryset = Object.objects.filter(ovenbird_id = request.session['ovenbird_id'])
        self.object = get_object_or_404(queryset, id = self.kwargs['pk'])
        return super(UpdateObject, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        object = self.object
        logger.warn(object)
        post_values = request.POST.copy()
        post_values['type'] = object.type
        post_values['ovenbird'] = object.ovenbird_id
        form = ObjectForm(data=post_values, instance=object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url(object.ovenbird_id))
        return super(UpdateObject, self).post(request, **kwargs)
    
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