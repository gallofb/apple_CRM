from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from django import template
register = template.Library()


#自定义标签
@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

# @register.simple_tag
# def get_query_sets(admin_class):
#     return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(request,obj,admin_class):
    #obj <class 'king_admin.king_admin.CustomerAdmin'>
    row_ele = ""
    for index,column in enumerate(admin_class.list_display):    #king_admin
        field_obj = obj._meta.get_field(column)
        # print(column)    list_diaplay的值
        # print(field_obj)    #crm.Customer.qq
        if field_obj.choices:      #chices type
            column_data = getattr(obj, "get_%s_display" % column)()   #取的是choice序列号所对应的值
            # column_data = getattr(obj,column)
            # print(column_data)    所对应的值
        else:
            column_data = getattr(obj,column)
        if type(column_data).__name__ == 'datetime':    #用来验证是否是时间的格式
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")

        if index == 0:  # add a tag, 可以跳转到修改页
            column_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path = request.path,
                                                                                       obj_id = obj.id,
                                                                                       data = column_data)

        row_ele += "<td>%s</td>" % column_data
    return mark_safe(row_ele)

@register.simple_tag
def built_paginators(query_sets,filter_condtions,previous_orderby,search_text):
    page_btns = ''
    filters = ''
    for k, v in filter_condtions.items():
        filters += "&%s=%s" % (k,v)

    added_dot_ele = False
    for page_num in query_sets.paginator.page_range:
        if page_num < 2 or page_num > query_sets.paginator.num_pages - 2 \
                or abs(query_sets.number - page_num) <= 1:
            # print("00000000%s----" %query_sets.number)
            #query.sets.number 当前页数  query_sets.paginator.num_pages总页数
            ele_class = ""
            if query_sets.number == page_num:
                added_dot_ele = False
                ele_class = "active"
            page_btns += '''<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a><li>'''\
                         %(ele_class,page_num,filters,previous_orderby,search_text,page_num)

        # elif abs(query_sets.number - page_num) <= 1: #判断前后1页
        #     ele_class = ""
        #     if query_sets.number == page_num:
        #         added_dot_ele = False
        #         ele_class = "active"
        #     page_btns += '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' % (
        #     ele_class, page_num, filters, page_num)

        else: #显示...
            if added_dot_ele == False:
                page_btns += '<li><a>...</a></li>'
                added_dot_ele = True

    return mark_safe(page_btns)

        # elif #代表最前的1,2页


@register.simple_tag
def render_page_ele(loop_counter,query_sets,filter_condtions):
    filters = ''
    for k, v in filter_condtions.items():
        filters += "&%s=%s" % (k,v)
    # print(query_sets.number)  query_sets.number 总页数
    if loop_counter < 3 or loop_counter > query_sets.number-2:
        # pass
    # if abs(query_sets.number - loop_counter) <= 2:
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a><li>'''%(ele_class,loop_counter,filters,loop_counter)
        return mark_safe(ele)

    return ""

@register.simple_tag
def render_filter_ele(filter_field,admin_class,filter_condtions):
    select_ele = '''<select class="form-control" name='{filter_field}' ><option value=''>----</option>'''
    field_obj = admin_class.model._meta.get_field(filter_field)
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            print("choice", choice_item, filter_condtions.get(filter_field), type(filter_condtions.get(filter_field)))
            if filter_condtions.get(filter_field) == str(choice_item[0]):
                selected = "selected"

            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''
    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
        date_els = []
        today_ele = datetime.now().date()
        date_els.append(['今天', datetime.now().date()])
        date_els.append(["昨天", today_ele - timedelta(days=1)])
        date_els.append(["近7天", today_ele - timedelta(days=7)])
        date_els.append(["本月", today_ele.replace(day=1)])
        date_els.append(["近30天", today_ele - timedelta(days=30)])
        date_els.append(["近90天", today_ele - timedelta(days=90)])
        date_els.append(["近180天", today_ele - timedelta(days=180)])
        date_els.append(["本年", today_ele.replace(month=1, day=1)])
        date_els.append(["近一年", today_ele - timedelta(days=365)])

        selected = ''
        for item in date_els:
            select_ele += '''<option value='%s' %s>%s</option>''' % (item[1], selected, item[0])

        filter_field_name = "%s__gte" % filter_field

    else:
        filter_field_name = filter_field
    select_ele += "</select>"
    select_ele = select_ele.format(filter_field=filter_field_name)

    return mark_safe(select_ele)

@register.simple_tag
def built_table_header_column(column,orderby_key,filter_condtions):
    filters = ''
    for k,v in filter_condtions.items():
        filters += "&%s=%s" %(k,v)

    ele = '''<th><a href="?{filters}&o={orderby_key}">{column}</a>
       {sort_icon}
       </th>'''

    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon = '''<span class="glyphicon glyphicon-chevron-up"></span>'''
        else:
            sort_icon = '''<span class="glyphicon glyphicon-chevron-down"></span>'''

        if orderby_key.strip("-") == column:
            orderby_key = orderby_key
        else:
            orderby_key =column
            sort_icon = ''
    else: #没有排序
        orderby_key = column
        sort_icon = ''
    ele = ele.format(orderby_key=orderby_key,column=column,sort_icon=sort_icon,filters=filters)
    return mark_safe(ele)

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.verbose_name

#get_choices