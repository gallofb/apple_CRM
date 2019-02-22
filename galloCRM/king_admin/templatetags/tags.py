from django import template
from django.utils.safestring import mark_safe

from django import template
register = template.Library()


#自定义标签
@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()

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
def render_page_ele(loop_counter,query_sets):
    if abs(query_sets.number - loop_counter) <= 1:
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s">%s</a><li>'''%(ele_class,loop_counter,loop_counter)
        return mark_safe(ele)


@register.simple_tag
def render_filter_ele(condtion,admin_class):
    select_ele = "<select name='%s'>" %condtion



#get_choices