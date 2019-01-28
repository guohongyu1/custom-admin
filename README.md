配置
######
1、settings.py
------
```
STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),
                  (os.path.join(BASE_DIR,'kingadmin/static')))
```

2、kingadmin.py
------
在每个app下创建kingadmin.py
```
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
```
3、注册
------
```
site.register(models.CustomerInfo,CustomerAdmin)
```
