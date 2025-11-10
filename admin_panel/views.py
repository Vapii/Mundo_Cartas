from django.shortcuts import render
from .models import RegistroAdmin
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_admin(request):
    registros = RegistroAdmin.objects.order_by('-fecha')[:20]
    return render(request, 'admin_panel/dashboard.html', {'registros': registros})
