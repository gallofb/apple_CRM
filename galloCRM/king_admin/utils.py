#过滤
from django.db.models import Q
def table_filter(request,admin_class):
    '''进行条件过滤返回过滤后的数据'''
    filter_conditions = {}
    keywords = {'page','o','_q'}
    for k,v in request.GET.items():
        if k in keywords: #保留的分页关键字
            continue
        if v:
            filter_conditions[k] = v
    #返回filter_conditions是为了让搜索的关键字显示在搜索栏中
    return admin_class.model.objects.filter(**filter_conditions).\
               order_by("-%s" % admin_class.ordering if admin_class.ordering else "-id"),\
            filter_conditions

#排序
def table_sort(request,admin_class,objs):
    orderby_key = request.GET.get("o")
    # print(">>>>>>>>6666%s" %orderby_key)   orderby_key 是子类中的元素
    if orderby_key:
        res = objs.order_by(orderby_key)
        if orderby_key.startswith("-"):
            orderby_key = orderby_key.strip("-")
        else:
            orderby_key = "-%s"%orderby_key
    else:
        res = objs
    return res,orderby_key

def table_search(request,admin_class,object_list):
    search_key = request.GET.get("_q","")     #拿到_q没有就是空
    q_obj = Q()
    q_obj.connector = "OR"   #连接条件
    for column in admin_class.search_fields:
        q_obj.children.append(("%s__contains" % column, search_key))   #字符串中包含指定的字符串

    res = object_list.filter(q_obj)   #保留符合要求的
    # print("tttttttttt%s" %res)
    return res