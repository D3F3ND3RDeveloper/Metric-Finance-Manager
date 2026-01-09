from datetime import datetime
from config import BASE_SYMBOL


def format_currency(amount):
    return f"{BASE_SYMBOL} {amount:,.0f}"


def current_date():
    return datetime.now().strftime("%A, %d %B %Y")


def current_time():
    return datetime.now().strftime("%I:%M %p")
