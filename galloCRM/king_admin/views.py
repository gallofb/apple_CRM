from django.shortcuts import render
from king_admin import king_admin
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def index(request):
    print(king_admin.enable_admins)   #返回app models
    return render(request,"king_admin/table_index.html",{'table_lsit':king_admin.enable_admins})

#显示表的内容
def display_table_objs(request,app_name,table_name):
    # 动态导入模块
    # model_module =
    admin_class = king_admin.enable_admins[app_name][table_name]
    # print(admin_class)   <class 'king_admin.king_admin.CustomerAdmin'>
    return render(request,'king_admin/table_objs.html',{"admin_class":admin_class})


