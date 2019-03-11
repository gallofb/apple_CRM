#__author:  Administrator
#date:  2017/1/10

from django.forms import forms,ModelForm

from crm import models

class CustomerModelForm(ModelForm):
    class Meta:
        model =  models.Customer
        fields = "__all__"



def create_model_form(request,admin_class):
    '''动态生成MODEL FORM'''

    def __new__(cls, *args, **kwargs):

        # super(CustomerForm, self).__new__(*args, **kwargs)
        print("base fields",cls.base_fields)   #给所有的表格加上样式
        for field_name,field_obj in cls.base_fields.items():
            print(field_name,dir(field_obj))
            field_obj.widget.attrs['class'] = 'form-control'
            # field_obj.widget.attrs['maxlength'] = getattr(field_obj,'max_length' ) if hasattr(field_obj,'max_length') \
            #     else ""

            if not hasattr(admin_class,"is_add_form"):   #代表这是添加form，不需要disabled
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs['disabled'] = 'disabled'

        return ModelForm.__new__(cls)

    def default_clean(self):
        print("------runing default clean",admin_class)
        for field in admin_class.readonly_fields:
            field_val = getattr(self.instance,field)

            field_val_from_frontend = self.cleaned_date.get(field)
            # rasie __ValueError(
            #     _('Field Readonly value:%(value)s is readonly'),
            #     code = 'invalid'
            #     params = ('value','42')
            #
            # )

    class Meta:
        model = admin_class.model
        fields = "__all__"
    attrs = {'Meta':Meta}
    _model_form_class =  type("DynamicModelForm",(ModelForm,),attrs)
    setattr(_model_form_class,'__new__',__new__)
    setattr(_model_form_class,'clean',default_clean)
    print("model form",_model_form_class.Meta.model )
    return _model_form_class