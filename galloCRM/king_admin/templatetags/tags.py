from django import template
from django.utils.safestring import mark_safe

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
def build_table_row(obj,admin_class):
    #obj <class 'king_admin.king_admin.CustomerAdmin'>
    row_ele = ""
    for column in admin_class.list_display:    #king_admin
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

        row_ele += "<td>%s</td>" % column_data
    return mark_safe(row_ele)

@register.simple_tag
def built_paginators(query_sets,filter_condtions):
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
            page_btns += '''<li class="%s"><a href="?page=%s%s">%s</a><li>'''\
                         %(ele_class,page_num,filters,page_num)

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
def render_filter_ele(condtion,admin_class,filter_condtions):

    select_ele = '''<select class="form-control" name='%s'><option value=''>----</option>''' %condtion
    field_obj = admin_class.model._meta.get_field(condtion)

    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            #condtion king_admin列表中的元素
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"

            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected = ''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = 'selected'
            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
    select_ele += "</select>"
    return mark_safe(select_ele)

@register.simple_tag
def render_table_header_column(column,orderby_key,filter_condtions):
    filters = ''
    for k,v in filter_condtions:
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
    return mark_safe(ele )

#get_choices