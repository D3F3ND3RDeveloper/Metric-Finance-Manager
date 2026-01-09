import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from database.db_manager import DatabaseManager
from config import THEME

class ChartManager(ctk.CTkFrame):
    """Reusable chart frame for Analytics and Reports"""
    def __init__(self, parent):
        super().__init__(parent, fg_color=THEME["card"], corner_radius=16)
        self.pack(fill="both", expand=True, padx=20, pady=10)

        self.db = DatabaseManager()
        self.mode = "monthly"  # daily / weekly / monthly
        self.chart_type = "line"  # line / bar

        self.build_controls()
        self.build_chart()

    # ---------------- CONTROLS ----------------
    def build_controls(self):
        ctrl = ctk.CTkFrame(self, fg_color="transparent")
        ctrl.pack(fill="x", padx=15, pady=10)

        # Mode buttons
        for m in ["daily", "weekly", "monthly"]:
            ctk.CTkButton(ctrl, text=m.capitalize(), width=80, command=lambda x=m: self.switch_mode(x)).pack(side="left", padx=5)
        
        # Chart type buttons
        for t in ["line", "bar"]:
            ctk.CTkButton(ctrl, text=t.capitalize(), width=80, command=lambda x=t: self.switch_chart(x)).pack(side="right", padx=5)

    # ---------------- CHART ----------------
    def build_chart(self):
        if hasattr(self, "canvas"):
            self.canvas.get_tk_widget().destroy()

        data = self.db.get_chart_data(self.mode)  # dict: {"labels":[], "values":[]}
        labels = data.get("labels", [])
        values = data.get("values", [])

        self.fig = Figure(figsize=(7,4), dpi=100)
        self.fig.patch.set_facecolor(THEME["card"])
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(THEME["card"])
        ax.tick_params(colors=THEME["muted_text"])
        ax.spines['bottom'].set_color(THEME["muted_text"])
        ax.spines['left'].set_color(THEME["muted_text"])

        if self.chart_type == "line":
            ax.plot(labels, values, color=THEME["primary"], marker='o')
        else:
            ax.bar(labels, values, color=THEME["primary"])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def switch_mode(self, mode):
        self.mode = mode
        self.build_chart()

    def switch_chart(self, chart_type):
        self.chart_type = chart_type
        self.build_chart()
