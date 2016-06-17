# -*- coding: utf-8 -*-
from ..models import Ovenbird, Object, Photo, Ads, Filter
from registration.models import CustomUser
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.shortcuts import render, render_to_response, redirect, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse 
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import OvenbirdForm, ObjectForm, FileUploadForm, AdsForm
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
from functools import reduce
import operator
import os
from braces.views import GroupRequiredMixin

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
            customuser = self.request.user.id
        )
        return queryset
    
class GroupRequiredMixin(GroupRequiredMixin):
    def check_membership(self, group):
        """ Check required group(s) """
        if self.request.user.is_superuser:
            return True
        user_groups = self.request.user.group.values_list("name", flat=True)
        return set(group).intersection(set(user_groups))
    
# main page
def MainPage(request):
    
    ovenbird_list = Ovenbird.objects.filter(customuser=CustomUser.objects.filter(group__name='Печники'))
    paginator = Paginator(ovenbird_list, 10)
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
    
    def get_initial(self):
        initial = super(UpdateOvenbird, self).get_initial()
        initial = initial.copy()
        initial['group'] = Group.objects.filter(customuser__id = self.request.user.id).values_list('id',flat=True)
        return initial
    
    def get_object(self):
        return Ovenbird.objects.get(customuser_id=self.request.user.id)

    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        ovenbird = self.get_object()
        post_values = request.POST.copy()
        post_values['customuser'] = ovenbird.customuser_id
        form = OvenbirdForm(data=post_values, instance=ovenbird)
        if form.is_valid():
            form.save()
            print(form.cleaned_data['group'].values_list('id',flat=True))
            group_queryset = Group.objects.all().values_list('id',flat=True)
            # добавление связей фильтров к объекту и получение тех, которых надо будет удалить
            customuser = CustomUser.objects.get(id=ovenbird.customuser_id)
            for new_group in form.cleaned_data['group'].values_list('id',flat=True):
                for old_group in group_queryset:
                    if new_group == old_group:
                        group_queryset = group_queryset.exclude(id=old_group)
                        break
                customuser.group.add(Group.objects.get(pk=new_group))
            for group in group_queryset:
                customuser.group.remove(Group.objects.get(pk=group))
            return HttpResponseRedirect('/offsite/')
        return super(UpdateOvenbird, self).post(request, **kwargs)

# показ списка печников   
class ShowOvenbird(DetailView):
    context_object_name = 'ovenbird'
    template_name = "offsite/ovenbird.html"
    
    model = Ovenbird
    
    def get_context_data(self, **kwargs):
        context = super(ShowOvenbird, self).get_context_data(**kwargs)
        context['objects'] = Object.objects.filter(customuser = self.kwargs['pk'], type = 1)
        context['articles'] = Object.objects.filter(customuser = self.kwargs['pk'], type = 2)
        context['items'] = Object.objects.filter(customuser = self.kwargs['pk'], type = 3)
        context['adses'] = Ads.objects.filter(customuser = self.kwargs['pk'])
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
class CreateObject(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "offsite/object.html"
    form_class = ObjectForm
    model = Object
    group_required = "Печники"
   
    def get_initial(self):
        initial = super(CreateObject, self).get_initial()
        initial = initial.copy()
        initial['type'] = 1
        return initial
   
    def get_success_url(self):
        return reverse('offsite:showovenbird', kwargs={'pk' : self.request.session['ovenbird_id']} )
    
    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        post_values['type'] = 1
        post_values['customuser'] = request.user.id
        form = ObjectForm(data=post_values)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return super(CreateObject, self).post(request, **kwargs)

# обновление объекта
class UpdateObject(GroupRequiredMixin, LoginRequiredMixin, AuthorizationMixin, UpdateView):
    template_name = "offsite/object.html"
    form_class = ObjectForm
    model = Object
    group_required = "Печники"
   
    def get_success_url(self):
        return reverse('offsite:showovenbird', kwargs={'pk' : self.request.session['ovenbird_id']})

    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        object = self.get_object()
        post_values = request.POST.copy()
        post_values['type'] = object.type
        post_values['customuser'] = object.customuser_id
        form = ObjectForm(data=post_values, instance=object)
        if form.is_valid():
            form.save()
            filter_queryset = Filter.objects.all().values_list('id',flat=True)
            # добавление связей фильтров к объекту и получение тех, которых надо будет удалить
            for new_filter in form.cleaned_data['filter_link'].values_list('id',flat=True):
                for old_filter in filter_queryset:
                    if new_filter == old_filter:
                        filter_queryset = filter_queryset.exclude(id=old_filter)
                        break
                object.filter_link.add(Filter.objects.get(pk=new_filter))
            for filter in filter_queryset:
                object.filter_link.remove(Filter.objects.get(pk=filter))
            return HttpResponseRedirect(self.get_success_url())
        return super(UpdateObject, self).post(request, **kwargs)

# удаление объекта
class DeleteObject(GroupRequiredMixin, LoginRequiredMixin, AuthorizationMixin, DeleteView):
    model = Object
    group_required = "Печники"
    
    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            json = {'status':'success'}
        except Exception as e:
            json = {'status':'denied', 'error':str(e)}
            logger.error(str(e))
        return JsonResponse(json)
# создание статьи   
class CreateArticle(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "offsite/object.html"
    form_class = ObjectForm
    model = Object
    group_required = "Печники"
   
    def get_initial(self):
        initial = super(CreateArticle, self).get_initial()
        initial = initial.copy()
        initial['type'] = 2
        return initial
   
    def get_success_url(self):
        return reverse('offsite:showovenbird', kwargs={'pk' : self.request.session['ovenbird_id']} )
    
    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        post_values['type'] = 2
        post_values['customuser'] = request.user.id
        form = ObjectForm(data=post_values)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return super(CreateArticle, self).post(request, **kwargs)
# создание товара    
class CreateItem(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "offsite/object.html"
    form_class = ObjectForm
    model = Object
    group_required = ["Печники","Рекламодатели"]
   
    def get_initial(self):
        initial = super(CreateItem, self).get_initial()
        initial = initial.copy()
        initial['type'] = 3
        return initial
   
    def get_success_url(self):
        return reverse('offsite:showovenbird', kwargs={'pk' : self.request.session['ovenbird_id']} )
    
    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        post_values['type'] = 3
        post_values['customuser'] = request.user.id
        form = ObjectForm(data=post_values)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return super(CreateItem, self).post(request, **kwargs)
# создание заявки
class CreateRequest(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "offsite/object.html"
    form_class = ObjectForm
    model = Object
    group_required = []
   
    def get_initial(self):
        initial = super(CreateRequest, self).get_initial()
        initial = initial.copy()
        initial['type'] = 4
        return initial
   
    def get_success_url(self):
        return reverse('offsite:showovenbird', kwargs={'pk' : self.request.session['ovenbird_id']} )
    
    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        post_values['type'] = 4
        post_values['customuser'] = request.user.id
        form = ObjectForm(data=post_values)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return super(CreateRequest, self).post(request, **kwargs)
# добавление файлов с изображениями
class AddFile(LoginRequiredMixin, CreateView):
    template_name = "offsite/addfile.html"
    form_class = FileUploadForm
    model = Photo
    
    def post(self, request, *args, **kwargs):
        try:
            post_values = request.POST.copy()
            post_values['customuser'] = request.user.id
            form = FileUploadForm(post_values, request.FILES)
            json_data = {}
            if form.is_valid():
                new_file = form.save()
                object = self.model.objects.filter(pk = new_file.id)
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
        photo = self.model.objects.filter(customuser_id=self.request.user.id)
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
    
    model = Object
    
    def get_queryset(self):
        queryset = self.model.objects.filter(
            customuser_id = self.request.user.id
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
    model = Object
    
    def get_queryset(self):
        queryset = self.model.objects.filter(
            customuser_id = self.request.user.id,
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
            Q(customuser_id=self.request.user.id)
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
            customuser_id = self.request.user.id,
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
    model = Ovenbird
    template_name = "offsite/adser.html"
    context_object_name = 'adser'
    
    def get_object(self):
        return get_object_or_404(self.model, id=self.request.session['ovenbird_id'])
        
    def get_context_data(self, **kwargs):
        context = super(ShowAdser, self).get_context_data(**kwargs)
        adses = Ads.objects.filter(ovenbird_id=self.request.session['ovenbird_id'])
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
class CreateAds(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "offsite/ads.html"
    model = Ads
    form_class = AdsForm
    group_required = "Рекламодатели"
        
    def get_success_url(self):
        return reverse('offsite:showovenbird', kwargs={'pk' : self.request.session['ovenbird_id']} )

    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        post_values['customuser'] = request.user.id
        form = AdsForm(post_values, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return super(CreateAds, self).post(request, **kwargs)

class UpdateAds(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = "offsite/ads.html"
    form_class = AdsForm
    model = Ads
    group_required = "Рекламодатели"
   
    def get_success_url(self):
        return reverse('offsite:showovenbird', kwargs={'pk' : self.request.session['ovenbird_id']} )

    # saving in DB after posting
    def post(self, request, *args, **kwargs):
        ads = self.get_object()
        path = settings.BASE_DIR + ads.image.url
        post_values = request.POST.copy()
        post_values['customuser'] = ads.customuser_id
        form = AdsForm(post_values, request.FILES, instance=ads)
        if form.is_valid():
            form.save()
            os.remove(path)
            return HttpResponseRedirect(self.get_success_url())
        return super(UpdateAds, self).post(request, **kwargs)
    
class DeleteAds(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Ads
    group_required = "Рекламодатели"
    
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

@method_decorator(login_required(login_url='/registration/login'))
def BillPayment(object):
    pass

def VoteUp(request, pk):
    if request.method == 'POST':
        try:
            review = Object.objects.get(pk=pk)
            vote = review.votes.exists(request.user)
            if vote:
                review.votes.down(request.user)
            else:
                review.votes.up(request.user)
            json = {'status':'success'}
        except Exception as e:
            json = {'status':'denied', 'error':str(e)}
        return JsonResponse(json)

class ShowAllObjects(ListView):
    template_name = "offsite/showallobjects.html"
    model = Object
    context_object_name = 'objects'
    
    def get_queryset(self, *args, **kwargs):
        argument_list = []
        fields = ['name']
        query_string = self.kwargs['filter']
        for query in query_string.split('&'):
            if query.isalnum():
                for field in fields:
                    argument_list.append( Q(**{'filter_link__'+field : query} ))
        if argument_list:
            objects = self.model.objects.filter(reduce(operator.or_, argument_list) or None).distinct()
        else:
            objects = self.model.objects.all()
        return objects
    
    def get_context_data(self, **kwargs):
        context = super(ShowAllObjects, self).get_context_data(**kwargs)
        #context['nodes'] = Filter.objects.all()
        query_string = str(self.kwargs['filter'])
        print(query_string)
        context['nodes'] = Filter.objects.raw('''with recursive rec as (
                                                    select * from offsite_filter where mptt_level = 0
                                                    union all 
                                                    select of.* from rec join offsite_filter of
                                                    on of.parent_id = rec.id)
                                                select name, id, strpos(%s, name) as checked
                                                from rec
                                                order by mptt_level, name''', [query_string])
        return context