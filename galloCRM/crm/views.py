from django.shortcuts import render
from king_admin import king_admin


# Create your views here.
def index(request):
    return render(request, 'index.html',{'table_list':king_admin.enable_admins})

def customer_list(request):
    return render(request, "sales/customer.html",)