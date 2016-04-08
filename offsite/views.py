# -*- coding: utf-8 -*-
from .models import Ovenbird, Object, Photo, Adser, Ads
from django.shortcuts import render, render_to_response, redirect, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse 
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import OvenbirdForm, ObjectForm, FileUploadForm, AdsForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseBadRequest
import json
import logging
from django.contrib.messages.api import success
from django.core import serializers
from django.db.models import Q
import os

logger = logging.getLogger(__name__)

# добавляет для метода диспатч декоратор проверки аутентификации
class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/registration/login'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

# мини авторизация, даёт доступ к данным только для текущего пользователя
class AuthorizationMixin(object):
    def get_queryset(self):
        queryset = self.model.objects.filter(
            pk=self.kwargs['pk'],
            ovenbird_id = self.request.session['ovenbird_id']
        )
        return queryset

class AuthorizationAdserMixin(object):
    def get_queryset(self):
        queryset = self.model.objects.filter(
            pk=self.kwargs['pk'],
            adser_id = self.request.session['adser_id']
        )
        return queryset
    
# main page
def MainPage(request):
    # creating var session, storing id ovenbird
    if request.user.is_authenticated(): 
        if 'ovenbird_id' not in request.session and request.user.is_ovenbird:
            ovenbird = Ovenbird.objects.get(customuser_id = request.user.id)
            if ovenbird is not None:
                request.session['ovenbird_id'] = ovenbird.id
        if 'adser_id' not in request.session and request.user.is_adser:
            adser = Adser.objects.get(customuser_id = request.user.id)
            if adser is not None:
                request.session['adser_id'] = adser.id
    
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

# создание печника
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

# обновление печника
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

 # показ списка печников   
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

# показ объекта
class ShowObject(DetailView):
    model = Object
    template_name = "offsite/showobject.html"
    context_object_name = 'object'
    
    def get_context_data(self, **kwargs):
        context = super(ShowObject, self).get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(object__id=self.kwargs['pk'])
        logger.warn(context['photos'])
        return context

# создание объекты
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

# обновление объекта
class UpdateObject(LoginRequiredMixin, AuthorizationMixin, UpdateView):
    template_name = "offsite/object.html"
    form_class = ObjectForm
    model = Object
   
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

# удаление объекта
class DeleteObject(LoginRequiredMixin, AuthorizationMixin, DeleteView):
    model = Object
    
    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            json = {'status':'success'}
        except Exception as e:
            json = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json)

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

# добавление файлов с изображениями
class AddFile(LoginRequiredMixin, CreateView):
    template_name = "offsite/addfile.html"
    form_class = FileUploadForm
    model = Photo
    
    def post(self, request, *args, **kwargs):
        try:
            post_values = request.POST.copy()
            post_values['ovenbird'] = request.session['ovenbird_id']
            form = FileUploadForm(post_values, request.FILES)
            json_data = {}
            if form.is_valid():
                new_file = form.save()
                object = Photo.objects.filter(pk = new_file.id)
                json_data = serializers.serialize('json', object, fields=('image'))
                json_data = {'status':'success', 'photo':json_data}
            else:
                json_data = {'status':'denied', 'error':'form is not valid'}
        except Exception as e:
            json_data = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json_data,safe=False)

# показ изображений списком
class ShowFile(LoginRequiredMixin, ListView):
    context_object_name = 'photos'
    template_name = "offsite/showfile.html"
    model = Photo
      
    def get_queryset(self):
        photo = Photo.objects.filter(ovenbird_id=self.request.session['ovenbird_id'])
        return photo

# удаление изображений
class DeleteFile(LoginRequiredMixin, AuthorizationMixin, DeleteView):
    model = Photo
    
    def delete(self, request, *args, **kwargs):
        try:
            file = self.get_object()
            path = settings.BASE_DIR + file.image.url
            # удаление связей в промежуточной таблице
            file.object.clear()
            # удаление фотографии
            file.delete()
            # физическое удаление фотографии
            os.remove(path)
            json = {'status':'success'}
        except Exception as e:
            json = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json)

# получение списка объектов  
class GetListObjects(LoginRequiredMixin, ListView):
    
    def get_queryset(self):
        queryset = Object.objects.filter(
            ovenbird_id = self.request.session['ovenbird_id']
        )
        return queryset
    
    def get(self, request, *args, **kwargs):
        try:
            object = self.get_queryset()
            json_data = serializers.serialize('json', object, fields=('title'))
            json_data = {'status':'success', 'objects':json_data}
        except Exception as e:
            json_data = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json_data,safe=False)

# прикрепление фотографии к объекту
class JoinObject(LoginRequiredMixin, AuthorizationMixin, UpdateView):
    model = Photo
    
    def post(self, request, *args, **kwargs):
        try:
            file = self.get_object()
            object = Object.objects.get(id = kwargs['object_id'])
            file.object.add(object)
            json = {'status':'success'}
        except Exception as e:
            json = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json)

# получение списка прикреплённых объектов    
class GetListJoinedObjects(LoginRequiredMixin, ListView):
    
    def get_queryset(self):
        queryset = Object.objects.filter(
            ovenbird_id = self.request.session['ovenbird_id'],
            photo__id = self.kwargs['photo_id']
        )
        return queryset
    
    def get(self, request, *args, **kwargs):
        try:
            object = self.get_queryset()
            json_data = serializers.serialize('json', object, fields=('title'))
            json_data = {'status':'success', 'objects':json_data}
        except Exception as e:
            json_data = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json_data,safe=False)

# открепление объекта
class UnjoinObject(LoginRequiredMixin, AuthorizationMixin, UpdateView):
    model = Photo
    
    def post(self, request, *args, **kwargs):
        try:
            file = self.get_object()
            object = Object.objects.get(id = kwargs['object_id'])
            file.object.remove(object)
            json = {'status':'success'}
        except Exception as e:
            json = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json)

# установка основной фото для объекта
class MakeTitlePhoto(LoginRequiredMixin, AuthorizationMixin, UpdateView):
    model = Photo

    def post(self, request, *args, **kwargs):
        try:
            file = self.get_object()
            object = Object.objects.get(id = kwargs['object_id'])
            object.title_photo_id = file
            object.save()
            json = {'status':'success'}
        except Exception as e:
            json = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json)

# установка основной фото для пол-ля
class SetOvenbirdPhoto(LoginRequiredMixin, AuthorizationMixin, UpdateView):
    model = Photo

    def post(self, request, *args, **kwargs):
        try:
            file = self.get_object()
            ovenbird = Ovenbird.objects.get(id = request.session['ovenbird_id'])
            ovenbird.main_photo_id = file
            ovenbird.save()
            json = {'status':'success'}
        except Exception as e:
            json = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json)
    
# показ изображений списком
class ShowAllFile(LoginRequiredMixin, ListView):
    context_object_name = 'photos'
    template_name = "offsite/showallfile.html"
    model = Photo
      
    def get_queryset(self):
        photo = self.model.objects.filter(
            Q(ovenbird_id=self.request.session['ovenbird_id'])
            & Q(object__id=self.kwargs['object_id'])
            | Q(object__id=None)
        ).order_by('object__id')
        return photo
    
    def get_context_data(self, **kwargs):
        context = super(ShowAllFile, self).get_context_data(**kwargs)
        context['object_id'] = self.kwargs['object_id']
        context['objects'] = Object.objects.all().exclude(id=self.kwargs['object_id'])
        return context

class GetListFiles(LoginRequiredMixin, ListView):
    context_object_name = 'photos'
    def get_queryset(self):
        queryset = Photo.objects.filter(
            ovenbird_id = self.request.session['ovenbird_id'],
            object__id = self.kwargs['object_id']
        ).exclude(object__id = self.kwargs['not_object_id'])
        return queryset
    
    def get(self, request, *args, **kwargs):
        try:
            object = self.get_queryset()
            json_data = serializers.serialize('json', object, fields=('image'))
            json_data = {'status':'success', 'objects':json_data}
        except Exception as e:
            json_data = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json_data,safe=False)
       
class ShowAdser(LoginRequiredMixin, DetailView):
    model = Adser
    template_name = "offsite/adser.html"
    context_object_name = 'adser'
    
    def get_object(self):
        return get_object_or_404(Adser, id=self.request.session['adser_id'])
        
    def get_context_data(self, **kwargs):
        context = super(ShowAdser, self).get_context_data(**kwargs)
        adses = Ads.objects.filter(adser_id=self.request.session['adser_id'])
        paginator = Paginator(adses, 10)
        page = self.request.GET.get('page')
        try:
            adses = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            adses = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            adses = paginator.page(paginator.num_pages)
        context['adses'] = adses
        return context       


#создание рекламы
class CreateAds(LoginRequiredMixin, CreateView):
    template_name = "offsite/ads.html"
    model = Ads
    form_class = AdsForm
        
    def get_success_url(self):
        return reverse('offsite:showadser')

    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        post_values['adser'] = request.session['adser_id']
        form = AdsForm(post_values, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return super(CreateAds, self).post(request, **kwargs)

class UpdateAds(AuthorizationAdserMixin, LoginRequiredMixin, UpdateView):
    template_name = "offsite/ads.html"
    form_class = AdsForm
    model = Ads
   
    def get_success_url(self):
        return reverse('offsite:showadser')

    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        ads = self.get_object()
        path = settings.BASE_DIR + ads.image.url
        post_values = request.POST.copy()
        post_values['adser'] = request.session['adser_id']
        form = AdsForm(post_values, request.FILES, instance=ads)
        if form.is_valid():
            form.save()
            os.remove(path)
            return HttpResponseRedirect(self.get_success_url())
        return super(UpdateAds, self).post(request, **kwargs)
    
class DeleteAds(AuthorizationAdserMixin, LoginRequiredMixin, DeleteView):
    model = Ads
    
    def delete(self, request, *args, **kwargs):
        try:
            ads = self.get_object()
            path = settings.BASE_DIR + ads.image.url
            ads.delete()
            os.remove(path)
            json = {'status':'success'}
        except Exception as e:
            json = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json)