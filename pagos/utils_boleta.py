import io
from django.conf import settings
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generar_boleta_pdf(pago_obj):
    """
    Retorna bytes (PDF) de una boleta simple:
    - nombre + email
    - buy_order + autorización + fecha
    - lista de productos con cantidad y subtotal
    - total (pago_obj.monto)
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "BOLETA DE COMPRA - Mundo Cartas")

    y -= 30
    c.setFont("Helvetica", 10)

    user = pago_obj.usuario
    nombre = getattr(user, "get_full_name", lambda: "")() or getattr(user, "nombre", "") or getattr(user, "username", "")
    email = getattr(user, "email", "")

    c.drawString(50, y, f"Cliente: {nombre}")
    y -= 15
    c.drawString(50, y, f"Email: {email}")
    y -= 15
    c.drawString(50, y, f"Orden: {pago_obj.buy_order}")
    y -= 15
    c.drawString(50, y, f"Autorización: {pago_obj.codigo_autorizacion}")
    y -= 15
    c.drawString(50, y, f"Fecha: {pago_obj.fecha.strftime('%d/%m/%Y %H:%M')}")
    y -= 25

    # Encabezado tabla
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Producto")
    c.drawString(310, y, "Cant.")
    c.drawString(360, y, "Precio")
    c.drawString(450, y, "Subtotal")
    y -= 10
    c.line(50, y, 545, y)
    y -= 15

    c.setFont("Helvetica", 10)

    total_calculado = 0
    items = pago_obj.items.select_related("producto").all()  # related_name="items"

    for it in items:
        nombre_prod = it.producto.nombre
        cant = int(it.cantidad)
        precio = int(it.producto.precio)
        subtotal = cant * precio
        total_calculado += subtotal

        # salto de página si se acaba el espacio
        if y < 80:
            c.showPage()
            y = height - 60
            c.setFont("Helvetica", 10)

        c.drawString(50, y, nombre_prod[:40])
        c.drawRightString(345, y, str(cant))
        c.drawRightString(430, y, f"${precio}")
        c.drawRightString(545, y, f"${subtotal}")
        y -= 18

    y -= 10
    c.line(50, y, 545, y)
    y -= 20
    c.setFont("Helvetica-Bold", 12)

    # Usamos el monto guardado en Pago como total “oficial”
    c.drawRightString(545, y, f"TOTAL: ${int(pago_obj.monto)}")

    # Nota (opcional)
    y -= 30
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Gracias por tu compra.")

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def enviar_boleta_por_email(pago_obj):
    user = pago_obj.usuario
    email_to = getattr(user, "email", "")
    if not email_to:
        return  # no hay email, no se envía

    pdf_bytes = generar_boleta_pdf(pago_obj)

    subject = f"Boleta Mundo Cartas - {pago_obj.buy_order}"
    body = (
        "Hola, adjuntamos tu boleta en PDF.\n\n"
        f"Orden: {pago_obj.buy_order}\n"
        f"Monto: ${int(pago_obj.monto)}\n"
        "Gracias por tu compra."
    )

    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_to],
    )

    filename = f"boleta_{pago_obj.buy_order}.pdf"
    msg.attach(filename, pdf_bytes, "application/pdf")
    msg.send(fail_silently=False)
