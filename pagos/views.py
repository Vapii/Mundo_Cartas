from django.shortcuts import render
from .models import Pago
from django.contrib.auth.decorators import login_required

@login_required
def confirmar_pago(request):
    pagos = Pago.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'pagos/confirm.html', {'pagos': pagos})

