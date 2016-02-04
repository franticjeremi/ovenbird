from .models import Ovenbird, Object
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import OvenbirdForm, ObjectForm
import logging
logger = logging.getLogger(__name__)
# Create your views here.
    
#class AboutView(TemplateView):
#    template_name = "jinja2/index.jinja"

def MainPage(request):
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
    
def CreateObject(request, type):
    #object_to_edit = get_object_or_404(Object,id=id)
    if request.method == 'POST':
        form = ObjectForm(data=request.POST)
        #form.field["type"].initial = type
        logger.warn(form.type)
        logger.warn(form)
        if form.is_valid():
            object = form.save()
            return redirect('/offsite/')
    else:
        form = ObjectForm()
    return render_to_response('offsite/object.html', {
        'form': form,
        }, context_instance=RequestContext(request))