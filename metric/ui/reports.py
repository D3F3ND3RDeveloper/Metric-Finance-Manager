# ui/reports.py
import customtkinter as ctk
from config import THEME, BASE_CURRENCY, USD_SYMBOL
from database.db_manager import DatabaseManager
from datetime import datetime
import os
import csv

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=THEME["background"])
        self.pack(fill="both", expand=True)
        self.db = DatabaseManager()
        self.build_header()
        self.build_table()
        self.refresh_table()

    # ---------------- HEADER ----------------
    def build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20,10))

        ctk.CTkLabel(header, text="All Expenses Report", font=("Segoe UI",20,"bold")).pack(side="left")

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right")

        self.total_label = ctk.CTkLabel(right, text=f"{BASE_CURRENCY} 0 | USD 0", font=("Segoe UI",14), text_color=THEME["primary"])
        self.total_label.pack(anchor="e")

        btns = ctk.CTkFrame(right, fg_color="transparent")
        btns.pack(anchor="e", pady=5)

        ctk.CTkButton(btns, text="Export Excel", width=120, command=self.export_excel).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Export PDF", width=120, fg_color=THEME["secondary"], command=self.export_pdf).pack(side="left", padx=5)

    # ---------------- TABLE ----------------
    def build_table(self):
        self.table_card = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=16)
        self.table_card.pack(fill="both", expand=True, padx=30, pady=(10,20))

        header = ctk.CTkFrame(self.table_card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10,5))

        cols = ["Time","Category","Item","Description","PKR","USD"]
        widths = [80,110,110,260,90,90]

        for col, w in zip(cols, widths):
            ctk.CTkLabel(header, text=col, width=w, anchor="w", font=("Segoe UI",11,"bold")).pack(side="left", padx=5)

        self.rows = ctk.CTkScrollableFrame(self.table_card, fg_color="transparent")
        self.rows.pack(fill="both", expand=True, padx=10, pady=5)

    # ---------------- LOGIC ----------------
    def refresh_table(self):
        for w in self.rows.winfo_children():
            w.destroy()

        self.expenses = self.db.get_all_expenses()
        rate = self.db.get_setting("usd_rate") or 1
        total_pkr = 0

        for e in self.expenses:
            time = e["created_at"].split(" ")[1][:5]
            usd = round(e["amount"]*rate,2)
            total_pkr += e["amount"]

            row = ctk.CTkFrame(self.rows, fg_color="transparent")
            row.pack(fill="x", pady=3)
            values = [time, e["category"], e["item"], e["description"], f"{e['amount']:.0f}", f"{usd:.2f}"]
            widths = [80,110,110,260,90,90]

            for v,w in zip(values,widths):
                ctk.CTkLabel(row, text=v, width=w, anchor="w").pack(side="left", padx=5)

        total_usd = round(total_pkr*rate,2)
        self.total_label.configure(text=f"{BASE_CURRENCY} {total_pkr:.0f} | {USD_SYMBOL} {total_usd:.2f}")

    # ---------------- EXPORT ----------------
    def export_excel(self):
        os.makedirs("exports/reports_excel", exist_ok=True)
        filename = f"exports/reports_excel/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        rate = self.db.get_setting("usd_rate") or 1

        with open(filename,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Time","Category","Item","Description","PKR","USD"])
            for e in self.expenses:
                time = e["created_at"]
                usd = round(e["amount"]*rate,2)
                writer.writerow([time, e["category"], e["item"], e["description"], e["amount"], usd])
        print("Excel exported:", filename)

    def export_pdf(self):
        os.makedirs("exports/reports_pdf", exist_ok=True)
        filename = f"exports/reports_pdf/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        rate = self.db.get_setting("usd_rate") or 1

        with open(filename,"w",encoding="utf-8") as f:
            f.write("ALL EXPENSES REPORT\n\n")
            for e in self.expenses:
                usd = round(e["amount"]*rate,2)
                f.write(f"{e['created_at']} | {e['category']} | {e['item']} | {e['description']} | {e['amount']} PKR | {usd} USD\n")
        print("PDF exported:", filename)
