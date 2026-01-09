# ui/settings.py
import customtkinter as ctk
from config import THEME, BASE_CURRENCY, DEFAULT_USD_RATE
from database.db_manager import DatabaseManager

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, refresh_callback=None):
        super().__init__(parent, fg_color=THEME["background"])
        self.pack(fill="both", expand=True)
        self.db = DatabaseManager()
        self.refresh_callback = refresh_callback

        self.build_ui()

    def build_ui(self):
        card = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=16, border_width=1, border_color=THEME["border"])
        card.pack(padx=30, pady=30, fill="x")

        # ---------------- MONTHLY SALARY ----------------
        ctk.CTkLabel(card, text="Monthly Salary", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20, pady=(20,5))
        self.salary_entry = ctk.CTkEntry(card, width=200)
        self.salary_entry.pack(anchor="w", padx=20, pady=(0,10))
        self.salary_entry.insert(0, str(self.db.get_setting("monthly_salary") or 0))

        # ---------------- USD RATE ----------------
        ctk.CTkLabel(card, text="USD Conversion Rate", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20, pady=(10,5))
        self.usd_entry = ctk.CTkEntry(card, width=200)
        self.usd_entry.pack(anchor="w", padx=20, pady=(0,10))
        self.usd_entry.insert(0, str(self.db.get_setting("usd_rate") or DEFAULT_USD_RATE))

        # ---------------- BUTTONS ----------------
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(anchor="w", padx=20, pady=(20,20))

        save_btn = ctk.CTkButton(btn_frame, text="Save Settings", width=120, command=self.save_settings)
        save_btn.pack(side="left", padx=5)

        reset_btn = ctk.CTkButton(btn_frame, text="Reset All Data", width=140, fg_color="#FF5C5C", command=self.reset_data)
        reset_btn.pack(side="left", padx=5)

        # Info label
        self.info_label = ctk.CTkLabel(card, text="", text_color=THEME["primary"])
        self.info_label.pack(anchor="w", padx=20)

    # ---------------- SAVE SETTINGS ----------------
    def save_settings(self):
        try:
            salary = float(self.salary_entry.get())
            usd_rate = float(self.usd_entry.get())
        except ValueError:
            self.info_label.configure(text="Please enter valid numeric values.")
            return

        self.db.update_setting("monthly_salary", salary)
        self.db.update_setting("usd_rate", usd_rate)
        self.info_label.configure(text="Settings saved successfully.")

        # Refresh other pages
        if self.refresh_callback:
            self.refresh_callback()

    # ---------------- RESET ALL DATA ----------------
    def reset_data(self):
        # Delete all expenses
        self.db.cursor.execute("DELETE FROM expenses")
        self.db.conn.commit()

        # Reset monthly salary and USD rate
        self.db.update_setting("monthly_salary", 0)
        self.db.update_setting("usd_rate", DEFAULT_USD_RATE)

        # Refresh other pages
        if self.refresh_callback:
            self.refresh_callback()

        self.salary_entry.delete(0, "end")
        self.salary_entry.insert(0, "0")
        self.usd_entry.delete(0, "end")
        self.usd_entry.insert(0, str(DEFAULT_USD_RATE))

        self.info_label.configure(text="All data reset successfully.")
