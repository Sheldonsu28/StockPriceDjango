from stock.models import Subscription
from yfinance import Tickers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def obtain_subscriptions():
    subscriptions = Subscription.objects.all()
    symbol_set = set()
    user_table = {}

    for item in subscriptions:
        symbol_set.add(item.symbol)
        if item.user.email not in user_table:
            user_table[item.user.email] = {item.symbol: 0}
        else:
            user_table[item.user.email][item.symbol] = 0

    query_string = "".join([" " + symbol for symbol in symbol_set])
    response = Tickers(query_string.strip()).tickers

    symbol_table = {ticker: response[ticker].info['regularMarketPrice'] for ticker in response.keys()}

    for email in user_table.keys():
        target_user = user_table.get(email)
        for symbol in target_user.keys():
            target_user[symbol] = symbol_table[symbol]

    return user_table


@shared_task
def send_email():
    logger.info('Start!')
    print('start')
    user_info = obtain_subscriptions()
    title = "Your hourly stock price update from Sheldon's Stock Price Subscription"
    sender_email = "placeholder"

    for email in user_info.keys():
        target_user = user_info[email]
        price_info = {'symbols': [{'ticker': symbol, 'price': target_user[symbol]} for symbol in target_user.keys()]}

        rendered_html = render_to_string("email.html", price_info)
        html_text = strip_tags(rendered_html)
        mail = EmailMultiAlternatives(title, html_text, sender_email, [email])
        mail.attach_alternative(rendered_html, "text/html")
        mail.send()
