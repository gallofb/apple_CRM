from django.forms import forms,ModelForm
from crm import models

class CustomerMoodelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"



def creat_model_form(request,admin_class):
    """动态生成model form"""
    class Meta:
        model = admin_class.model
        fields = "__all__"
    attrs = {'Meta':Meta}
    _model_form_class = type("DynamicModelForm",(ModelForm,),{})
    setattr(_model_form_class)   #设置属性值
    return _model_form_class