from crm import models
#将app存入字典中
enable_admins = {}
#父类
class BaseAdmin(object):
    list_display = []
    list_filter = []
    list_per_page =10
    search_fields = []
    ordering = None

#子类
class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','source','consultant','date','status']
    list_filters = ['source', 'consultant', 'consult_course', 'status','date']
    search_fields = ['qq','name']
    # model = models.Customer  和 admin_class.model = model_class
    ordering = "id"

class CustomerFollowUpAdmin(BaseAdmin):
    #数据库表里面的字段
    list_display = ['customer','consultant','date']

def register(model_class,admin_class=None):

    #通过表名找app名
    if model_class._meta.app_label not in enable_admins:
        # app加入到字典中
        enable_admins[model_class._meta.app_label] = {}
        #enabled_admins['crm'] = {}   将app放入到字典中
    admin_class.model = model_class #绑定model对象和admin类
    #将表名加入到字典中
    enable_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)