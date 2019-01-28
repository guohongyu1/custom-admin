1、setting.py
STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),
                  (os.path.join(BASE_DIR,'kingadmin/static')))

2、kingadmin.py
在每个app下创建kingadmin.py,注册model
from kingadmin.sites import site
from kingadmin.admin_base import BaseAdmin
from crm import models
class CustomerAdmin(BaseAdmin):
    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []
    filter_horizontal = []
    actions = []
site.register(models.CustomerInfo,CustomerAdmin)

