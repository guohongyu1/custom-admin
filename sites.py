from kingadmin.admin_base import BaseAdmin
class Adminsite:
    def __init__(self):
        self.enabled_admins={}
    def register(self, model_class, admin_class=BaseAdmin):
        app_name=model_class._meta.app_label
        model_name=model_class._meta.model_name
        if not admin_class: #避免多了model共享一个内存对象
            admin_class=BaseAdmin()
        else:
            admin_class=admin_class()
        admin_class.model = model_class
        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name]={}
        self.enabled_admins[app_name][model_name]=admin_class
site=Adminsite()









