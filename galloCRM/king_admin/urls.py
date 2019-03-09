from django.conf.urls import url
from king_admin import views

urlpatterns = [
    url(r'^$',views.index,name="king_admin"),
    url(r'^(\w+)/(\w+)/$',views.display_table_objs,name='table_objs'),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change,name="table_obj_change"),
    url(r'^(\w+)/(\w+)/add/$',views.table_obj_add,name="table_obj_add"),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete,name="obj_delete"),
]