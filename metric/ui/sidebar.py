import customtkinter as ctk
from PIL import Image
from config import THEME, LOGO_PATH, FONT_SUBTITLE


class SidebarButton(ctk.CTkButton):
    """Custom sidebar button with hover glow"""

    def __init__(self, parent, text, command):
        super().__init__(
            parent,
            text=text,
            command=command,
            fg_color=THEME["sidebar"],
            hover_color=THEME["card"],
            text_color=THEME["text"],
            corner_radius=10,
            anchor="w",
            height=44,
            font=FONT_SUBTITLE
        )

        self.default_border = THEME["sidebar"]
        self.glow_border = THEME["primary"]

        self.configure(border_width=1, border_color=self.default_border)

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.configure(border_color=self.glow_border)

    def on_leave(self, event):
        self.configure(border_color=self.default_border)


class Sidebar(ctk.CTkFrame):
    """Left sidebar navigation"""

    def __init__(self, parent, switch_page_callback):
        super().__init__(
            parent,
            fg_color=THEME["sidebar"],
            width=240,
            corner_radius=0
        )

        self.pack_propagate(False)
        self.pack(side="left", fill="y")

        self.switch_page = switch_page_callback

        # -------------------------
        # Logo
        # -------------------------
        logo_img = Image.open(LOGO_PATH).resize((80, 80))
        self.logo = ctk.CTkImage(logo_img, size=(80, 80))

        self.logo_label = ctk.CTkLabel(
            self,
            image=self.logo,
            text=""
        )
        self.logo_label.pack(pady=(30, 10))

        # App name
        self.app_name = ctk.CTkLabel(
            self,
            text="Metric",
            font=("Segoe UI", 18, "bold"),
            text_color=THEME["text"]
        )
        self.app_name.pack(pady=(0, 30))

        # -------------------------
        # Navigation Buttons
        # -------------------------
        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ("Dashboard", lambda: self.switch_page("dashboard")),
            ("Expenses", lambda: self.switch_page("expenses")),
            ("Analytics", lambda: self.switch_page("analytics")),
            ("Reports", lambda: self.switch_page("reports")),
            ("Settings", lambda: self.switch_page("settings")),
        ]

        for text, cmd in buttons:
            btn = SidebarButton(self, text, cmd)
            btn.pack(fill="x", padx=16, pady=6)
