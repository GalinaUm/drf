from pprint import pprint

# import requests
import stripe
from forex_python.converter import CurrencyRates
# from stripe.issuing import Authorization

from config.settings import EXCHANGE_API_KEY, STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары"""

    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)

    # url = "https://api.exchangeratesapi.io/v1/convert"
    # response = requests.get(url, params={
    #     "amount": amount,
    #     "access_key": EXCHANGE_API_KEY,
    #     "from": "RUB",
    #     "to": "USD",
    # }, headers={"Accept": "application/json", "Authorization": f"Bearer {EXCHANGE_API_KEY}"})
    # return response.json


def create_stripe_price(amount):
    """Создает цену в страйпе"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        recurring={"interval": "month"},
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


if __name__ == "__main__":
    pprint(convert_rub_to_dollars(100))
