from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from transbank.webpay.webpay_plus.transaction import Transaction
from .models import Pago, ItemCompra
from carrito.models import ItemCarrito
from transbank.common.options import WebpayOptions
from transbank.webpay.webpay_plus.transaction import Transaction
from .utils import get_webpay_options
from django.urls import reverse


tx = Transaction(get_webpay_options())

@login_required
def iniciar_pago(request):
    items = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)

    if request.method == "POST":
        tx = Transaction(get_webpay_options())
        response = tx.create(
            buy_order=f"orden-{request.user.id}-{int(timezone.now().timestamp())}",
            session_id=request.session.session_key,
            amount=total,
            return_url = request.build_absolute_uri(reverse("commit_pago"))
        )
        url = response["url"] + "?token_ws=" + response["token"]
        return redirect(url)

    return render(request, "pagos/iniciar.html", {"total": total})




@login_required
def commit_pago(request):
    token = request.GET.get("token_ws")
    tx = Transaction(get_webpay_options())
    result = tx.commit(token)

    status = result.get("status")

    if result.get("status") == "AUTHORIZED":
        pago_obj = Pago.objects.create(
            usuario=request.user,
            monto=result.get("amount"),
            metodo="Webpay",
            estado="APROBADO",
            codigo_autorizacion=result.get("authorization_code", "SIN-CODIGO"),
            buy_order=result.get("buy_order")
        )

        items = ItemCarrito.objects.select_related("producto").filter(usuario=request.user)
        for item in items:
            producto = item.producto
            producto.stock = max(producto.stock - item.cantidad, 0)
            producto.save(update_fields=["stock"])

            ItemCompra.objects.create(
                pago=pago_obj,
                producto=producto,
                cantidad=item.cantidad
            )

        items.delete()


        return render(request, "pagos/resultado.html", {
            "status": status,
            "buy_order": result.get("buy_order"),
            "amount": result.get("amount"),
            "mensaje": "Pago aprobado correctamente."
        })

    else:
        return render(request, "pagos/resultado.html", {
            "status": status,
            "buy_order": result.get("buy_order"),
            "amount": result.get("amount"),
            "mensaje": "Hubo un problema con tu pago."
        })


@login_required
def confirmar_pago(request):
    pagos = Pago.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, "pagos/confirm.html", {"pagos": pagos})
