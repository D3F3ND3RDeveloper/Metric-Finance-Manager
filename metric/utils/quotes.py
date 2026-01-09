import random
from datetime import date

_QUOTES = [
    "Do not save what is left after spending; spend what is left after saving.",
    "A budget is telling your money where to go instead of wondering where it went.",
    "Beware of little expenses; a small leak will sink a great ship.",
    "Financial freedom is freedom from fear.",
    "Wealth is not about having a lot of money, but having a lot of options."
]

def get_daily_quote():
    today = date.today().toordinal()
    return _QUOTES[today % len(_QUOTES)]
