from django.shortcuts import render, redirect
from .tasks import send_email
from django.http import HttpRequest
from stock.models import Subscription


def send_email_to_user(request: HttpRequest, symbol: str) -> render:
    if not request.user.is_authenticated:
        return redirect("/users/login/")

    symbol = symbol.upper()
    target = Subscription.objects.filter(user=request.user, symbol=symbol)
    send_email(target)

    return redirect("/stock/user_home_page")
# Create your views here.
