# ui/analytics.py
import customtkinter as ctk
from config import THEME, BASE_CURRENCY
from database.db_manager import DatabaseManager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
import calendar


class AnalyticsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=THEME["background"])
        self.pack(fill="both", expand=True)

        self.db = DatabaseManager()
        self.canvas = None  # keep reference to matplotlib canvas

        # ---------------- HEADER ----------------
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="Analytics",
            font=("Segoe UI", 20, "bold"),
            text_color=THEME["text"]
        ).pack(anchor="w")

        # ---------------- CHART CARD ----------------
        self.chart_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card"],
            corner_radius=16,
            border_width=1,
            border_color=THEME["border"]
        )
        self.chart_card.pack(fill="both", expand=True, padx=30, pady=20)

        self.draw_chart()

    # ---------------- GET DAILY DATA ----------------
    def get_daily_month_data(self):
        """
        Returns labels (days) and values (total spent per day)
        for current month.
        """
        now = datetime.now()
        year = now.year
        month = now.month

        days_in_month = calendar.monthrange(year, month)[1]
        daily_totals = {day: 0 for day in range(1, days_in_month + 1)}

        # Query expenses for this month
        month_prefix = now.strftime("%Y-%m")
        self.db.cursor.execute(
            """
            SELECT amount, created_at
            FROM expenses
            WHERE created_at LIKE ?
            """,
            (f"{month_prefix}%",)
        )

        rows = self.db.cursor.fetchall()
        for row in rows:
            day = int(row["created_at"].split("-")[2].split(" ")[0])
            daily_totals[day] += row["amount"]

        labels = list(daily_totals.keys())
        values = list(daily_totals.values())

        return labels, values

    # ---------------- DRAW CHART ----------------
    def draw_chart(self):
        # Clear old chart
        for w in self.chart_card.winfo_children():
            w.destroy()

        labels, values = self.get_daily_month_data()

        if not any(values):
            ctk.CTkLabel(
                self.chart_card,
                text="No expense data for this month",
                text_color=THEME["muted_text"],
                font=("Segoe UI", 14)
            ).pack(pady=40)
            return

        # ---------------- MATPLOTLIB ----------------
        fig, ax = plt.subplots(figsize=(9, 4))
        fig.patch.set_facecolor(THEME["card"])
        ax.set_facecolor(THEME["card"])

        ax.plot(labels, values, color=THEME["primary"], linewidth=2)
        ax.fill_between(labels, values, color=THEME["primary"], alpha=0.15)

        # Styling
        ax.tick_params(colors="white", labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(THEME["border"])
        ax.spines["bottom"].set_color(THEME["border"])

        ax.set_xlabel("Day of Month", color="white")
        ax.set_ylabel(BASE_CURRENCY, color="white")

        # Canvas
        self.canvas = FigureCanvasTkAgg(fig, self.chart_card)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # ---------------- REFRESH (CALLED FROM MAIN) ----------------
    def refresh(self):
        self.draw_chart()
