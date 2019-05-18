from typing import Union

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from services.service_proxy import ServiceProxy
from home.forms import CurrencyExchangeForm


@login_required()
def finance_view(request):
    if request.method == "POST":
        form = CurrencyExchangeForm(request.POST)
        if form.is_valid():
            base_currency = form.cleaned_data["base_currency"]
            target_currency = form.cleaned_data["target_currency"]
            base_amount = form.cleaned_data["base_amount"]
            result_amount = convert_currency(
                base_currency=base_currency,
                target_currency=target_currency,
                base_amount=base_amount,
            )
            context = build_finance_view_context(
                base_currency=base_currency,
                base_amount=base_amount,
                result_amount=result_amount,
                result_currency=target_currency,
            )
            context["form"] = form
            return render(request, "home/finance_page.html", context=context)
    else:
        form = CurrencyExchangeForm()
    return render(request, "home/finance_page.html", {"form": form})


def convert_currency(base_currency: str, target_currency: str, base_amount: int):
    if base_currency == target_currency:
        return base_amount
    payload = {"base": base_currency, "target": target_currency, "amount": base_amount}
    try:
        service_proxy = ServiceProxy()
        response = service_proxy.service_request(
            service_name="fx_service",
            service_version=1,
            function_name="conversion",
            payload=payload,
        )
        return response.get("payload")
    except Exception:
        return None


def build_finance_view_context(
    base_currency: str,
    base_amount: int,
    result_amount: Union[float, None],
    result_currency: str,
) -> dict:
    if result_amount:
        return {
            "fx": True,
            "base_amount": round(base_amount, 2),
            "base_currency": base_currency,
            "result_amount": round(result_amount, 2),
            "result_currency": result_currency,
        }
    else:
        return {"fx_error": True}
