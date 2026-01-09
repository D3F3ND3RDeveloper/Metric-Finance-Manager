# config.py

# ---------------- APP DETAILS ----------------
APP_NAME = "Metric"
APP_VERSION = "1.0.0"

# ---------------- CURRENCY ----------------
BASE_CURRENCY = "PKR"
BASE_SYMBOL = "₨"

SECONDARY_CURRENCY = "USD"
USD_SYMBOL = "$"

# Default USD rate
DEFAULT_USD_RATE = 0.0036

# ---------------- DATABASE ----------------
DB_PATH = "database/metric.db"

# ---------------- GEMINI AI (Finance Only) ----------------
GEMINI_API_KEY = "AIzaSyCTDhclJvSGyii5USWbXB2j_rdxa03bDl0"
GEMINI_SYSTEM_PROMPT = """
You are a professional personal finance assistant.
You must ONLY answer questions related to:
- budgeting
- saving money
- expense control
- financial discipline
- personal finance advice

If a question is unrelated, respond with:
"I can only assist with finance-related topics."
"""

# ---------------- UI THEME ----------------
THEME = {
    "background": "#0B0F0C",    # dark greenish-black
    "sidebar": "#0D120D",
    "card": "#121712",           # dark card
    "border": "#1A2218",         # card border
    "hover": "#203124",          # hover highlight
    "primary": "#3CB371",        # neon green accent
    "secondary": "#2E8B57",      # darker green buttons
    "danger": "#FF5C5C",
    "warning": "#FFB020",

    "text": "#E0E0E0",
    "muted_text": "#A3A3A3"
}

# ---------------- FONTS ----------------
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 14, "bold")
FONT_TEXT = ("Segoe UI", 12)
FONT_SMALL = ("Segoe UI", 10)

# ---------------- PATHS ----------------
ASSETS_PATH = "assets/"
LOGO_PATH = ASSETS_PATH + "logo.png"
ICON_PATH = ASSETS_PATH + "icon.ico"
SPLASH_BG_PATH = ASSETS_PATH + "splash_bg.png"

# ---------------- ANIMATIONS ----------------
ANIMATION_SPEED = 5   # subtle, smooth
FADE_STEPS = 10       # low, no janky fade

# ---------------- DATE / TIME ----------------
TIME_FORMAT = "%I:%M %p"
DATE_FORMAT = "%A, %d %B %Y"

# Active USD rate used by app
USD_RATE = DEFAULT_USD_RATE
