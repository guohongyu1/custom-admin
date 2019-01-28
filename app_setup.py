from django import conf
def kingadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            mod = __import__('%s.kingadmin' % app_name)
        except ImportError:
            pass















