from django.http import HttpResponse, HttpRequest
from .models import Subscription
from .Utils import batch_get_symbol_price
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserForm, SubscriptionForm


# Create your views here.
def user_home_page(request: HttpRequest) -> render:
    if not request.user.is_authenticated:
        return redirect("/users/login/")
    subscribed_stock = request.user.symbols.all()
    query = [stock.symbol for stock in subscribed_stock]
    prices = batch_get_symbol_price(query)

    context = {'symbols': prices}

    return render(request, 'home.html', context)


def register_user(request: HttpRequest) -> render:
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Registration successful.")
            return redirect('/users/login/')
        else:
            messages.success(request, "Registration not successful.")
    else:
        user_form = CustomUserForm()
    return render(request, './registration/register.html', {'form': user_form})


def delete_subscription(request: HttpRequest, symbol: str) -> render:
    if not request.user.is_authenticated:
        return redirect("/users/login/")

    symbol = symbol.upper()
    target = Subscription.objects.filter(user=request.user, symbol=symbol)
    if len(target) > 0:
        target[0].delete()

    return redirect("/stock/user_home_page")


def subscribe_stocks(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("/users/login/")

    if request.POST:
        target_stock = SubscriptionForm(request.POST)

        if target_stock.is_valid():
            symbol = target_stock.cleaned_data["symbol"].upper()
            if not Subscription.objects.filter(user=request.user, symbol=symbol).exists():
                entry = Subscription(symbol=symbol, user=request.user)
                entry.save()
        return redirect("/stock/user_home_page")

    context = {"form": SubscriptionForm()}
    return render(request, "subscribe.html", context)


def index(request):
    return HttpResponse("Hello, world. You're at the stock index.")
