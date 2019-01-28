from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django import conf
from kingadmin import app_setup
from kingadmin.sites import site
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from kingadmin import forms
import json
app_setup.kingadmin_auto_discover()
# Create your views here.
def app_index(request):
    return render(request, 'kingadmin/app_index.html',{'site':site})
def acc_login(request):
    msg_error=""
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','/kingadmin/'))
        else:
            msg_error="wrong username or password"
            return render(request, 'kingadmin/login.html', {'msg_error':msg_error})
    return render(request, 'kingadmin/login.html')
def acc_logout(request):
    logout(request)
    return redirect('/kingadmin/login')
def get_filter(request,obj):
    filter_dict={}
    for k,v in request.GET.items():
        if k in ('_page','_o','_q'): continue
        if v:
            filter_dict[k]=v
    return obj.filter(**filter_dict),filter_dict
def sorted_column(request,admin_class,obj):
    lp_dict={}
    lp_index=request.GET.get('_o')
    if lp_index:
        lp_key=admin_class.list_display[abs(int(lp_index))]
        lp_dict[lp_key]=lp_index
        if lp_index.startswith('-'):
            lp_key=lp_key
        else:
            lp_key = '-' + lp_key
        return obj.order_by(lp_key),lp_dict
    else:
        return obj,lp_dict
def search_group(request,admin_class,obj):
    search_key=request.GET.get('_q')

    if search_key:
        q=Q()
        q.connector='OR'
        for search_field in admin_class.search_fields:
            q.children.append(('%s__contains'%search_field,''.join(search_key.split())))
        return obj.filter(q),search_key
    else:
        return obj,''
# @login_required
def table_obj_list(request,app_name,model_name):
    admin_class=site.enabled_admins[app_name][model_name]
    admin_class_actions=list(set(admin_class.actions))
    if request.method=='POST':
        selected_action=request.POST.get('action')
        selected_ids=json.loads(request.POST.get('selected_ids'))
        # selected_objs=admin_class.model.objects.filter(id__in=selected_ids)
        # admin_action_func = getattr(admin_class, selected_action)
        # admin_action_func(request,selected_objs)
        # if admin_class.default_action:
        #     return  admin_action_func(request,selected_objs)
        if not selected_action:
            # if selected_ids:
                admin_class.model.objects.filter(id__in=selected_ids).delete()
        else:
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_class, selected_action)
            response=admin_action_func(request, selected_objs)
            if response:
                return response
    obj=admin_class.model.objects.all().order_by('-id')
    obj,filter_dict=get_filter(request,obj)
    admin_class.filter_dict = filter_dict
    obj,search_key=search_group(request,admin_class,obj)
    admin_class.search_key=search_key
    obj,lp_dict=sorted_column(request,admin_class, obj)
    paginator=Paginator(obj,10)
    page=request.GET.get('_page')
    try:
        obj=paginator.page(page)
    except PageNotAnInteger:
       obj=paginator.page(1)
    except EmptyPage:
        obj=paginator.page(paginator.num_pages)
    return render(request,'kingadmin/table_obj_list.html',{'admin_class':admin_class,
                                                           'obj':obj,
                                                           'lp_dict':lp_dict,
                                                           'app_name':app_name,
                                                           'model_name':model_name,
                                                           'admin_class_actions':admin_class_actions
                                                           })
# @login_required
def table_obj_change(request,app_name,model_name,obj_id):
    admin_class=site.enabled_admins[app_name][model_name]
    model_form=forms.create_dynamic_models_forms(admin_class)
    # model_form=forms.a()
    obj=admin_class.model.objects.get(id=obj_id)
    if request.method=='GET':
        form_obj=model_form(instance=obj)
    elif request.method=='POST':
        form_obj = model_form(instance=obj,data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/kingadmin/%s/%s'%(app_name,model_name))
    return render(request,'kingadmin/table_obj_change.html',locals())
# @login_required
def table_obj_add(request,app_name,model_name):
    admin_class=site.enabled_admins[app_name][model_name]
    model_form=forms.create_dynamic_models_forms(admin_class,form_add=True)
    if request.method=='GET':
        form_obj=model_form()
        # return render(request, 'kingadmin/table_obj_add.html', locals())
    elif request.method=='POST':
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/kingadmin/%s/%s'%(app_name,model_name))
    return render(request, 'kingadmin/table_obj_add.html', locals())
# @login_required
def table_obj_delete(request,app_name,model_name,obj_id):
    admin_class=site.enabled_admins[app_name][model_name]
    obj=admin_class.model.objects.get(id=obj_id)
    if request.method=='POST':
        admin_class.model.objects.filter(id__in=obj_id).delete()
        return redirect('/kingadmin/{app_name}/{model_name}/'.format(app_name=app_name,model_name=model_name))
    return render(request,'kingadmin/table_obj_delete.html',locals())










