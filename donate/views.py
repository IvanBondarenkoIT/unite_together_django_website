from django.shortcuts import render

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse


def donate_paypal(request, lang="uk"):
    product_price = settings.PRODUCT_PRICE
    product_id = settings.PRODUCT_ID

    host = request.get_host()

    paypal_checkout = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": product_price,
        "item_name": product_id,
        "invoice": uuid.uuid4(),
        "currency_code": "USD",
        "notify_url": f"http://{host}{reverse('paypal-ipn')}",
        "return_url": f"http://{host}{reverse('donate-success')}",
        "cancel_url": f"http://{host}{reverse('donate-failed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {"product_price": product_price, "paypal": paypal_payment}

    return render(request, "donate/donate-paypal.html", context=context)


def donate_successful(request, lang="uk"):
    return render(
        request,
        "donate/donate-success.html",
    )


def donate_failed(request, lang="uk"):
    return render(
        request,
        "donate/donate-failed.html",
    )
