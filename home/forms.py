from django import forms


class CurrencyExchangeForm(forms.Form):
    AUS_DOLLAR = "AUD"
    CANADA_DOLLAR = "CAD"
    CZECH_KORUNA = "CZK"
    EURO = "EUR"
    GB_POUND = "GBP"
    PL_ZLOTY = "PLN"
    USA_DOLLAR = "USD"
    CURRENCY_CHOICES = (
        (AUS_DOLLAR, "Australia Dollar"),
        (CANADA_DOLLAR, "Canada Dollar"),
        (CZECH_KORUNA, "Czech Koruna"),
        (EURO, "Euro"),
        (GB_POUND, "GB Pound"),
        (PL_ZLOTY, "Poland Zloty"),
        (USA_DOLLAR, "USA Dollar"),
    )
    base_currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES, required=True, initial=GB_POUND
    )
    target_currency = forms.ChoiceField(
        widget=forms.Select, choices=CURRENCY_CHOICES, required=True, initial=EURO
    )
    amount = forms.IntegerField(widget=forms.NumberInput, required=True)
