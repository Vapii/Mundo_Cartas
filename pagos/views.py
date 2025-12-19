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
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .utils_boleta import enviar_boleta_por_email
from django.db import transaction



def enviar_recibo_email(user, pago_obj, items_compra):
    if not user.email:
        return  # si el usuario no tiene email, no enviamos

    subject = f"Recibo de compra - {pago_obj.buy_order}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    html_content = render_to_string("emails/recibo.html", {
        "user": user,
        "pago": pago_obj,
        "items": items_compra
    })

    msg = EmailMultiAlternatives(subject, "Tu recibo está en formato HTML.", from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


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

    if not token:
        return render(request, "pagos/resultado.html", {
            "mensaje": "Token inválido."
        })

    tx = Transaction(get_webpay_options())
    result = tx.commit(token)

    if result.get("status") != "AUTHORIZED":
        return render(request, "pagos/resultado.html", {
            "mensaje": "Hubo un problema con tu pago."
        })

    buy_order = result.get("buy_order")

    items = ItemCarrito.objects.select_related("producto").filter(usuario=request.user)
    if not items.exists():
        return render(request, "pagos/resultado.html", {
            "mensaje": "El carrito está vacío."
        })

    total = sum(i.producto.precio * i.cantidad for i in items)
    if int(result.get("amount")) != int(total):
        return render(request, "pagos/resultado.html", {
            "mensaje": "Monto inconsistente."
        })

    with transaction.atomic():
        pago_obj, created = Pago.objects.get_or_create(
            buy_order=buy_order,
            defaults={
                "usuario": request.user,
                "monto": result.get("amount"),
                "metodo": "Webpay",
                "estado": "APROBADO",
                "codigo_autorizacion": result.get("authorization_code", "SIN-CODIGO"),
                "boleta_enviada": False
            }
        )

        if not created:
            return render(request, "pagos/resultado.html", {
                "pago": pago_obj,
                "mensaje": "Este pago ya fue procesado."
            })

        for item in items:
            producto = item.producto
            producto.stock = max(producto.stock - item.cantidad, 0)
            producto.save(update_fields=["stock"])

            ItemCompra.objects.create(
                pago=pago_obj,
                producto=producto,
                cantidad=item.cantidad
            )

        pago_obj = Pago.objects.select_for_update().get(id=pago_obj.id)
        if not pago_obj.boleta_enviada:
            try:
                enviar_boleta_por_email(pago_obj)
                pago_obj.boleta_enviada = True
                pago_obj.save(update_fields=["boleta_enviada"])
            except Exception as e:
                print("Error enviando boleta:", e)

        items.delete()

    return render(request, "pagos/resultado.html", {
        "pago": pago_obj,
        "mensaje": "Pago aprobado correctamente."
    })


@login_required
def confirmar_pago(request):
    pagos = Pago.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, "pagos/confirm.html", {"pagos": pagos})
