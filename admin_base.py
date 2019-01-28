from django.shortcuts import render
import json
class BaseAdmin(object):
    def __init__(self):
        self.actions.extend(self.default_action)
    list_display =[]
    list_filter =[]
    search_fields = []
    readonly_fields=[]
    actions=[]
    default_action=['delete_select_objs']
    # def add(self):
    #     self.actions.extend(self.default_action)
    def delete_select_objs(self,request,querysets):
        querysets_ids=json.dumps([i.id for i in querysets])
        return render(request,'kingadmin/table_obj_delete.html',{'admin_class':self,'objs':querysets,'querysets_ids':querysets_ids})
# BaseAdmin().add()







