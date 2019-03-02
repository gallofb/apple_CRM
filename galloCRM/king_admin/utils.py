#过滤


def table_filter(request,admin_class):
    '''进行条件过滤返回过滤后的数据'''
    filter_conditions = {}
    for k,v in request.GET.items():
        if k == 'page': #保留的分页关键字
            continue
        if v:
            filter_conditions[k] = v
    #返回filter_conditions是为了让搜索的关键字显示在搜索栏中
    return admin_class.model.objects.filter(**filter_conditions), filter_conditions

def table_sort(request,admin_class,objs):
    orderby_key = request.GET.get("o")
    print(">>>>>>>>%s" %orderby_key)
    if orderby_key:
        res = objs.order_by(orderby_key)
        if orderby_key.startswith("-"):
            orderby_key = orderby_key.strip("-")
        else:
            orderby_key = "-%s"%orderby_key
    else:
        res = objs
    return res,orderby_key