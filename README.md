1、setting.py<br>
------
STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),<br>
                  (os.path.join(BASE_DIR,'kingadmin/static')))

2、kingadmin.py<br>
------
在每个app下创建kingadmin.py,注册model<br>
from kingadmin.sites import site<br>
from kingadmin.admin_base import BaseAdmin<br>
from crm import models<br>
 tab tab   class CustomerAdmin(BaseAdmin):<br>
      list_display = []<br>
      list_filter = []<br>
      search_fields = []<br>
      readonly_fields = []<br>
      filter_horizontal = []<br>
      actions = []<br>
site.register(models.CustomerInfo,CustomerAdmin)

