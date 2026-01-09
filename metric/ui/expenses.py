# ui/expenses.py
import customtkinter as ctk
from datetime import datetime
from database.db_manager import DatabaseManager
from config import THEME, BASE_CURRENCY, USD_SYMBOL, DEFAULT_USD_RATE

CATEGORIES = {
    "Groceries": ["Vegetables", "Fruits", "Snacks", "Dairy"],
    "Transport": ["Fuel", "Taxi", "Bus"],
    "Bills": ["Electricity", "Internet", "Mobile"],
    "Lifestyle": ["Shopping", "Entertainment", "Gym"],
    "Other": ["Misc"]
}

class ExpensesPage(ctk.CTkFrame):
    def __init__(self, parent, refresh_callback=None):
        super().__init__(parent, fg_color=THEME["background"])
        self.pack(fill="both", expand=True)
        self.db = DatabaseManager()
        self.refresh_callback = refresh_callback

        self.build_header()
        self.build_form()
        self.build_table()
        self.refresh_table()

    # ---------------- HEADER ----------------
    def build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="Today's Expenses",
            font=("Segoe UI", 20, "bold")
        ).pack(side="left")

        self.total_label = ctk.CTkLabel(
            header,
            text=f"{BASE_CURRENCY} 0 | USD 0",
            font=("Segoe UI", 14),
            text_color=THEME["primary"]
        )
        self.total_label.pack(side="right")

    # ---------------- FORM ----------------
    def build_form(self):
        form = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=16)
        form.pack(fill="x", padx=30, pady=10)

        self.category = ctk.CTkComboBox(form, values=list(CATEGORIES.keys()), width=160)
        self.category.pack(side="left", padx=10, pady=15)
        self.category.set("Groceries")

        self.item = ctk.CTkComboBox(form, values=CATEGORIES["Groceries"], width=160)
        self.item.pack(side="left", padx=10)
        self.item.set("Vegetables")

        self.description = ctk.CTkEntry(form, placeholder_text="Description", width=240)
        self.description.pack(side="left", padx=10)

        self.amount = ctk.CTkEntry(form, placeholder_text="Amount (PKR)", width=120)
        self.amount.pack(side="left", padx=10)

        add_btn = ctk.CTkButton(
            form,
            text="Add",
            fg_color=THEME["primary"],
            text_color="black",
            width=80,
            command=self.add_expense
        )
        add_btn.pack(side="left", padx=10)

        self.category.configure(command=self.update_items)

    def update_items(self, category):
        self.item.configure(values=CATEGORIES[category])
        self.item.set(CATEGORIES[category][0])

    # ---------------- TABLE ----------------
    def build_table(self):
        table_card = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=16)
        table_card.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        header = ctk.CTkFrame(table_card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 5))

        cols = ["Time", "Category", "Item", "Description", "PKR", "USD"]
        widths = [80, 110, 110, 260, 90, 90]

        for col, w in zip(cols, widths):
            ctk.CTkLabel(header, text=col, width=w, anchor="w", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)

        self.rows = ctk.CTkScrollableFrame(table_card, fg_color="transparent")
        self.rows.pack(fill="both", expand=True, padx=10, pady=5)

    # ---------------- LOGIC ----------------
    def add_expense(self):
        try:
            amount_value = float(self.amount.get())
        except ValueError:
            return  # invalid input

        self.db.add_expense(
            category=self.category.get(),
            item=self.item.get(),
            description=self.description.get(),
            amount=amount_value,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.amount.delete(0, "end")
        self.description.delete(0, "end")
        self.refresh_table()

        # Refresh other pages
        if self.refresh_callback:
            self.refresh_callback()

    def refresh_table(self):
        for w in self.rows.winfo_children():
            w.destroy()

        expenses = self.db.get_today_expenses()
        rate = self.db.get_usd_rate() or DEFAULT_USD_RATE
        total_pkr = 0

        for e in expenses:
            time = e["created_at"].split(" ")[1][:5]
            usd = round(e["amount"] * rate, 2)
            total_pkr += e["amount"]

            self.add_row(time, e["category"], e["item"], e["description"], e["amount"], usd)

        total_usd = round(total_pkr * rate, 2)
        self.total_label.configure(text=f"{BASE_CURRENCY} {total_pkr:,.0f} | USD {total_usd:,.2f}")

    def add_row(self, time, category, item, desc, pkr, usd):
        row = ctk.CTkFrame(self.rows, fg_color="transparent")
        row.pack(fill="x", pady=3)

        values = [time, category, item, desc, f"{pkr:,.0f}", f"{usd:,.2f}"]
        widths = [80, 110, 110, 260, 90, 90]

        for v, w in zip(values, widths):
            ctk.CTkLabel(row, text=v, width=w, anchor="w").pack(side="left", padx=5)
