from transbank.common.options import WebpayOptions

def get_webpay_options():
    return WebpayOptions(
        commerce_code="597055555532",
        api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        integration_type="TEST"
    )
