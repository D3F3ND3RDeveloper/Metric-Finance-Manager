import customtkinter as ctk
from datetime import datetime
from config import THEME, BASE_CURRENCY, APP_NAME, LOGO_PATH
from database.db_manager import DatabaseManager
from utils.quotes import get_daily_quote
from customtkinter import CTkImage
from PIL import Image


class StatCard(ctk.CTkFrame):
    def __init__(self, parent, title, value="—"):
        super().__init__(
            parent,
            fg_color=THEME["card"],
            corner_radius=20,
            border_width=1,
            border_color=THEME["border"]
        )
        self.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color=THEME["muted_text"]
        )
        self.title_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color=THEME["primary"]
        )
        self.value_label.pack(anchor="w", padx=20, pady=(0, 20))

    def update_value(self, value):
        self.value_label.configure(text=value)


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=THEME["background"])
        self.pack(fill="both", expand=True)

        self.db = DatabaseManager()
        self.cards = {}

        self.build_header()
        self.build_cards()
        self.build_quote()
        self.refresh()  # IMPORTANT

    # ---------------- HEADER ----------------
    def build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(15, 10))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", anchor="w")

        logo_img = CTkImage(Image.open(LOGO_PATH), size=(40, 40))
        ctk.CTkLabel(left, image=logo_img, text="").pack(side="left")
        ctk.CTkLabel(
            left,
            text=APP_NAME,
            font=("Segoe UI", 20, "bold"),
            text_color=THEME["primary"]
        ).pack(side="left", padx=10)

        self.datetime_label = ctk.CTkLabel(
            header,
            font=("Segoe UI", 12),
            text_color=THEME["muted_text"]
        )
        self.datetime_label.pack(side="right")
        self.update_datetime()

    # ---------------- STAT CARDS (CREATE ONCE) ----------------
    def build_cards(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=30, pady=10)
        frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.cards["today"] = StatCard(frame, "Today's Spending")
        self.cards["today"].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.cards["salary"] = StatCard(frame, "Monthly Salary")
        self.cards["salary"].grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.cards["balance"] = StatCard(frame, "Available Balance")
        self.cards["balance"].grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    # ---------------- REFRESH VALUES (FIXES RESET) ----------------
    def refresh(self):
        today_spent = self.db.get_today_total() or 0
        monthly_salary = self.db.get_setting("monthly_salary") or 0
        spent_month = self.db.get_monthly_total() or 0
        available = max(monthly_salary - spent_month, 0)

        self.cards["today"].update_value(f"{BASE_CURRENCY} {today_spent:,.0f}")
        self.cards["salary"].update_value(f"{BASE_CURRENCY} {monthly_salary:,.0f}")
        self.cards["balance"].update_value(f"{BASE_CURRENCY} {available:,.0f}")

    # ---------------- QUOTE ----------------
    def build_quote(self):
        quote_text = get_daily_quote() or "Start saving today!"

        card = ctk.CTkFrame(
            self,
            fg_color=THEME["card"],
            corner_radius=20,
            border_width=1,
            border_color=THEME["border"]
        )
        card.pack(fill="x", padx=30, pady=(10, 30))

        ctk.CTkLabel(
            card,
            text="Financial Quote of the Day",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            card,
            text=quote_text,
            font=("Segoe UI", 12),
            wraplength=900,
            justify="left",
            text_color=THEME["muted_text"]
        ).pack(anchor="w", padx=20, pady=(0, 15))

    # ---------------- CLOCK ----------------
    def update_datetime(self):
        now = datetime.now()
        self.datetime_label.configure(
            text=now.strftime("%A, %d %B %Y | %I:%M %p")
        )
        self.after(60000, self.update_datetime)
