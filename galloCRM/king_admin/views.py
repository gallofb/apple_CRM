from django.shortcuts import render
from king_admin import king_admin
from king_admin.utils import table_filter
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def index(request):
    print(king_admin.enable_admins)   #返回app models
    return render(request,"king_admin/table_index.html",{'table_lsit':king_admin.enable_admins})

# 显示表的内容
def display_table_objs(request,app_name,table_name):
    print("-->",app_name,table_name)
    admin_class = king_admin.enable_admins[app_name][table_name]
    Object_list = admin_class.model.objects.all()
    # object_list= table_filter(request,admin_class)
    paginator = Paginator(Object_list,2)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)    #<Page 2 of 3>
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)
        print("9999999")
        print(paginator.num_pages)

    return render(request,"king_admin/table_objs.html",{"admin_class":admin_class,
                                                        "query_sets":query_sets })

