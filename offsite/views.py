from django.shortcuts import render, render_to_response
from django.views.generic import ListView, TemplateView
from django.template import RequestContext
import logging
logger = logging.getLogger(__name__)
# Create your views here.
    
#class AboutView(TemplateView):
#    template_name = "jinja2/index.jinja"

def myview(request):
    username = None
    logger.warning(request)
    if request.user.is_authenticated():
        username = request.user.email
        logger.warning(username)
    return render_to_response('offsite/index.html', context_instance=RequestContext(request,{'username': username}))
