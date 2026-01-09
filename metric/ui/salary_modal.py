import customtkinter as ctk
from config import THEME
from database.db_manager import DatabaseManager

class SalaryModal(ctk.CTkToplevel):
    def __init__(self, parent, on_save):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.on_save = on_save

        self.title("Set Monthly Salary")
        self.geometry("300x200")
        self.configure(fg_color=THEME["bg"])
        self.grab_set()

        ctk.CTkLabel(
            self,
            text="Monthly Salary (PKR)",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=20)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        ).pack(pady=20)

    def save(self):
        try:
            amount = float(self.entry.get())
            self.db.set_salary(amount)
            self.on_save()
            self.destroy()
        except:
            pass
