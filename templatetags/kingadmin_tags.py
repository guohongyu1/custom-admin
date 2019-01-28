from django.template import Library
from django.utils.safestring import mark_safe
import datetime
register=Library()
@register.simple_tag
def  build_filter_ele(filter_column,admin_class ):
    column_obj=admin_class.model._meta.get_field(filter_column)
    try:
        filter_ele = "<select name='%s'>"%filter_column
        for choice in column_obj.get_choices():
            selected=''
            if filter_column in admin_class.filter_dict:
                if str(choice[0]) == admin_class.filter_dict.get(filter_column):
                    selected='selected'
            option="<option value='%s' %s>%s</option>" %(choice[0],selected,choice[1])
            filter_ele+=option
    except AttributeError as e:
        filter_ele = "<select name='%s__gte'>"%filter_column
        if column_obj.get_internal_type() in('DateField','DateTimeField'):
            time_obj=datetime.datetime.now()
            time_list=[
                ['','---------'],
                [time_obj,'今天'],
                [time_obj-datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj-datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1,day=1), '一年内'],
                ['','全部']
            ]
            for i in time_list:
                selected=""
                time_to_str='' if not i[0] else "%s-%s-%s" %(i[0].year,i[0].month,i[0].day)
                if "%s__gte" %filter_column in admin_class.filter_dict:
                    if time_to_str == admin_class.filter_dict.get("%s__gte" %filter_column):
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" %(time_to_str,selected,i[1])
                # option = "<option value='%s'>%s</option>" % (i[0], i[1])
                filter_ele+=option
    filter_ele += "</select>"
    return mark_safe(filter_ele)
@register.simple_tag
def build_table_row(item,admin_class):
    ele=""
    if admin_class.list_display:
        for index,column_name in enumerate(admin_class.list_display):
            column_obj=admin_class.model._meta.get_field(column_name)
            if column_obj.choices:
                column_data=getattr(item,"get_%s_display"%column_name)()
            else:
                column_data = getattr(item,column_name)
            td_ele = "<td>%s</td>" % column_data
            if index == 0:
                td_ele = "<td><a href='%s/change/'>%s</a></td>" %(item.id,column_data)
            ele += td_ele
    else:
        td_ele = "<td><a href='%s/change/'>%s</a></td>" % (item.id, item)
        ele+=td_ele
    return  mark_safe(ele)
@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()
@register.simple_tag
def render_paginator(obj,admin_class,lp_dict):
    get_filter_ele = render_filter_args(admin_class)
    o = ''
    if lp_dict:
        o = '&_o=%s' % list(lp_dict.values())[0]
    ele='''
     <ul class="pagination">
    '''
    pf_ele = '<li class=""><a href="?_page=1&%s%s">first</a></li>'%(get_filter_ele,o)
    ele += pf_ele
    g=eval('obj.number-1')
    if obj.number==1:
        g=1
    pp_ele='<li class=""><a href="?_page=%s&%s%s">previous</a></li>'%(g,get_filter_ele,o)
    ele+=pp_ele
    for i in obj.paginator.page_range:
        if abs(obj.number-i)<2:  #display_page
            active = ''
            if obj.number==i:  #current_page
                active='active'
            p_ele='<li class="%s"><a href="?_page=%s&%s%s">%s</a></li>'%(active,i,get_filter_ele,o,i)
            ele+=p_ele
    j=eval('obj.number+1')
    if obj.number==len(obj.paginator.page_range):
        j=len(obj.paginator.page_range)
    pn_ele = '<li class=""><a href="?_page=%s&%s%s">next</a></li>' %(j,get_filter_ele,o)
    ele+=pn_ele
    p=len(obj.paginator.page_range)
    pl_ele = '<li class=""><a href="?_page=%s&%s%s">last</a></li>'%(p,get_filter_ele,o)
    ele += pl_ele
    ele+='</ul>'
    return mark_safe(ele)
@register.simple_tag
def sorted_column(title,lp_dict,forloop):
    if title in lp_dict:
        sorted_index=lp_dict[title]
        if sorted_index.startswith('-'):
            this_index=sorted_index.strip('-')
        else:
            this_index='-%s'%sorted_index
        return this_index
    else:
        return forloop
@register.simple_tag
def render_sorted_arrow(title,lp_dict):
    if title in lp_dict:
        sorted_index=lp_dict[title]
        if sorted_index.startswith('-'):
            type="top"
        else:
            type="bottom"
        ele='''
        <span class ="glyphicon glyphicon-triangle-%s" aria-hidden="true" > </span>
        ''' %type
        return mark_safe(ele)
    return ''
@register.simple_tag
def render_filter_args(admin_class):
    if admin_class.filter_dict:
        ele=''
        for k,v in admin_class.filter_dict.items():
            ele +='&%s=%s'%(k,v)
        return mark_safe(ele)
    else:
        return ''
@register.simple_tag
def get_sorted(lp_dict):
    return list(lp_dict.values())[0] if lp_dict else ''
@register.simple_tag
def get_readonly_data(form_obj,field):
    return  getattr(form_obj.instance,field)
@register.simple_tag
def get_available_m2m_data(field_name,admin_class,form_obj):
        field_obj=admin_class.model._meta.get_field(field_name)
        obj_list=set(field_obj.related_model.objects.all())
        if not admin_class.form_add:

            obj_list = set(field_obj.related_model.objects.all())
            seleted_data = set(getattr(form_obj.instance, field_name).all())
            return obj_list-seleted_data
        else:

            return obj_list
    # else:
    #     return admin_class.model._meta.get_field(field_name).related_model.objects.all()
@register.simple_tag
def available_m2m_data(field_name,admin_class,form_obj):
        return getattr(form_obj.instance,field_name).all()

@register.simple_tag
def get_kf_obj(obj):
    ele="<ul>"
    # ele+="<li>%s</li>" %obj
    for related_objs in  obj._meta.related_objects:
        related_name=related_objs.name
        related_key="%s_set" %related_name
        related_obj=getattr(obj,related_key).all()
        ele+="<li >%s<ul>"%related_name
        if related_objs.get_internal_type()  =="ManyToManyField":
            for i in related_obj:
                ele += "<li >%s</li>" % i
        else:
            for i in related_obj:
                ele+="<li>%s</li>"%i
                ele+=get_kf_obj(i)
        ele+="</ul></li>"
    ele+="</ul>"
    return ele
@register.simple_tag
def get_model_name_verbose_name(admin_class):
    return admin_class.model._meta.verbose_name


