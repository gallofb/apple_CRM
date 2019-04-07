# from crm import models
# from django.shortcuts import  render,redirect
# #将app存入字典中
# enable_admins = {}
# #父类
# class BaseAdmin(object):
#     list_display = []
#     list_filter = []
#     list_per_page =10
#     search_fields = []
#     ordering = None
#     filter_horizontal = []
#     readonly_fields = []
#     actions = ["delete_selected_objs",]
#     readonly_table = False
#
#     def delete_selected_objs(self, request, querysets):
#         app_name = self.model._meta.app_label
#         table_name = self.model._meta.model_name
#         print("--->delete_selected_objs", self, request, querysets)
#         if request.POST.get("delete_confirm") == "yes":
#             querysets.delete()
#             return redirect("/king_admin/%s/%s/" % (app_name, table_name))
#         selected_ids = ','.join([str(i.id) for i in querysets])
#         return render(request, "king_admin/table_obj_delete.html", {"objs": querysets,
#                                                                     "admin_class": self,
#                                                                     "app_name": app_name,
#                                                                     "table_name": table_name,
#                                                                     "selected_ids": selected_ids,
#                                                                     "action": request._admin_action
#                                                                     })
#
#     def default_form_validation(self):
#         pass
#
# #子类
# class CustomerAdmin(BaseAdmin):
#     list_display = ['id','qq','name','source','consultant','date','status']
#     list_filters = ['source', 'consultant', 'consult_course', 'status','date']
#     search_fields = ['qq','name']
#     filter_horizontal = ('tags',)
#     readonly_fields = ['qq','consultant''tags']
#     readonly_table = True
#
#     # model = models.Customer  和 admin_class.model = model_class
#     ordering = "id"
#
#     actions = ["delete_selected_objs","test"]
#     def test(self,request,querysets):
#         print("in test",)
#     test.display_name = "测试动作"
#
#     def default_form_validation(self):
#         consult_content = self.cleaned_data.get("content",'')
#         if len(consult_content) < 15:
#             return self.ValidationError(
#                 ('Field %(field)s 咨询内容记录不少15个字符'),
#                 code = 'invalid',
#                 params = {'field':"content",},
#             )
#
#     def clean_name(self):
#         print("name clean validation:", self.cleaned_data["name"])
#         if not self.cleaned_data["name"]:
#             self.add_error('name', "cannot be null")
#
#
# class UserProfileAdmin(BaseAdmin):
#     list_display = ('email','name')
#
#
# class CustomerFollowUpAdmin(BaseAdmin):
#     #数据库表里面的字段
#     list_display = ['customer','consultant','date']
#
# def register(model_class,admin_class=None):
#
#     #通过表名找app名
#     if model_class._meta.app_label not in enable_admins:
#         # app加入到字典中
#         enable_admins[model_class._meta.app_label] = {}
#         #enabled_admins['crm'] = {}   将app放入到字典中
#     admin_class.model = model_class #绑定model对象和admin类
#     #将表名加入到字典中
#     enable_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class
#
#
# register(models.Customer,CustomerAdmin)
# register(models.CustomerFollowUp,CustomerFollowUpAdmin)
# register(models.UserProfile,UserProfileAdmin)



#__author:  Administrator
#date:  2017/1/5
from django.shortcuts import  render,redirect
from crm import models


enabled_admins = {}

class BaseAdmin(object):
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = 20
    ordering = None
    filter_horizontal = []
    readonly_fields = []
    actions = ["delete_selected_objs",]
    readonly_table = False
    modelform_exclude_fields = []

    def delete_selected_objs(self,request,querysets):
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        print("--->delete_selected_objs",self,request,querysets)
        if self.readonly_table:
            errors = {"readonly_table": "This table is readonly ,cannot be deleted or modified!" }
        else:
            errors = {}
        if request.POST.get("delete_confirm") == "yes":
            if not self.readonly_table:
                querysets.delete()
            return redirect("/king_admin/%s/%s/" % (app_name,table_name))
        selected_ids =  ','.join([str(i.id) for i in querysets])
        return render(request,"king_admin/table_obj_delete.html",{"objs":querysets,
                                                              "admin_class":self,
                                                              "app_name": app_name,
                                                              "table_name": table_name,
                                                              "selected_ids":selected_ids,
                                                              "action":request._admin_action,
                                                              "errors":errors
                                                              })

    def default_form_validation(self):
        '''用户可以在此进行自定义的表单验证，相当于django form的clean方法'''
        pass

class CustomerAdmin(BaseAdmin):
    list_display = ["id",'qq','name','source','consultant','consult_course','date','status','enroll']
    list_filters = ['source','consultant','consult_course','status','date']
    search_fields = ['qq','name',"consultant__name"]
    filter_horizontal = ('tags',)
    #model = models.Customer
    list_per_page = 5
    ordering = "qq"
    readonly_fields = ["qq","consultant","tags"]
    #readonly_table = True
    #modelform_exclude_fields = []
    actions = ["delete_selected_objs","test"]
    def test(self,request,querysets):
        print("in test",)
    test.display_name  = "测试动作"

    def enroll(self):
        print("enroll",self.instance)
        if self.instance.status ==0:
            link_name = "报名新课程"
        else:
            link_name = "报名"
        return '''<a href="/crm/customer/%s/enrollment/" > %s</a>''' %(self.instance.id,link_name)
    enroll.display_name = "报名链接"

    def default_form_validation(self):
        #print("-----customer validation ",self)
        #print("----instance:",self.instance)

        consult_content =self.cleaned_data.get("content",'')
        if len(consult_content) <15:
            return self.ValidationError(
                            ('Field %(field)s 咨询内容记录不能少于15个字符'),
                            code='invalid',
                            params={'field': "content",},
                       )


    def clean_name(self):
        print("name clean validation:", self.cleaned_data["name"])
        if not self.cleaned_data["name"]:
            self.add_error('name', "cannot be null")



class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer','consultant','date')


class UserProfileAdmin(BaseAdmin):
    list_display = ('email','name')
    readonly_fields = ('password',)
    modelform_exclude_fields = ["last_login",]
    filter_horizontal = ("user_permissions","groups")

def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {} #enabled_admins['crm'] = {}
    #admin_obj = admin_class()
    admin_class.model = model_class #绑定model 对象和admin 类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class
    #enabled_admins['crm']['customerfollowup'] = CustomerFollowUpAdmin


register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.UserProfile,UserProfileAdmin)


