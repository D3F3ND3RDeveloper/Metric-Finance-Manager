# main.py
import customtkinter as ctk
from ui.splash import SplashScreen
from ui.dashboard import DashboardPage
from ui.analytics import AnalyticsPage
from ui.expenses import ExpensesPage
from ui.reports import ReportsPage
from ui.settings import SettingsPage
from config import THEME, APP_NAME, LOGO_PATH
from customtkinter import CTkImage
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ---------------- ROOT WINDOW ----------------
        self.title(APP_NAME)
        self.geometry("1200x700")
        self.minsize(1000, 600)
        self.configure(fg_color=THEME["background"])

        # Set the window icon (OS title bar)
        try:
            icon_image = Image.open(LOGO_PATH)  # use .ico for Windows
            self.iconphoto(False, ImageTk.PhotoImage(icon_image))
        except Exception as e:
            print("Failed to load window icon:", e)

        # ---------------- TOP BAR ----------------
        self.build_top_bar()

        # ---------------- PAGES CONTAINER ----------------
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Dictionary for page instances
        self.pages = {}
        self.refresh_callbacks = []

        # ---------------- SPLASH SCREEN ----------------
        self.after(100, self.show_splash)

    # ---------------- SHOW SPLASH ----------------
    def show_splash(self):
        self.splash = SplashScreen(self, on_finish=self.init_pages)
        self.splash.grab_set()  # Focus splash window

    # ---------------- TOP BAR ----------------
    def build_top_bar(self):
        top_bar = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=0)
        top_bar.pack(fill="x")

        # Logo + App Name
        logo_img = CTkImage(Image.open(LOGO_PATH), size=(40, 40))
        ctk.CTkLabel(top_bar, image=logo_img, text="").pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(
            top_bar,
            text=APP_NAME,
            font=("Segoe UI", 18, "bold"),
            text_color=THEME["primary"]
        ).pack(side="left")

        # Page buttons
        btn_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)
        pages = [
            ("Dashboard", "dashboard"),
            ("Analytics", "analytics"),
            ("Expenses", "expenses"),
            ("Reports", "reports"),
            ("Settings", "settings")
        ]
        for name, key in pages:
            ctk.CTkButton(
                btn_frame,
                text=name,
                width=100,
                command=lambda k=key: self.show_page(k)
            ).pack(side="left", padx=5)

    # ---------------- INIT PAGES AFTER SPLASH ----------------
    def init_pages(self):
        # Create pages
        self.pages["dashboard"] = DashboardPage(self.container)
        self.pages["analytics"] = AnalyticsPage(self.container)
        self.pages["expenses"] = ExpensesPage(self.container, refresh_callback=self.refresh_all)
        self.pages["reports"] = ReportsPage(self.container)
        self.pages["settings"] = SettingsPage(self.container, refresh_callback=self.refresh_all)

        # Keep pages that support refresh
        self.refresh_callbacks = [
            self.pages["dashboard"],
            self.pages["analytics"],
            self.pages["reports"]
        ]

        # Place all pages in same location
        for page in self.pages.values():
            page.place(x=0, y=0, relwidth=1, relheight=1)

        # Show dashboard by default
        self.show_page("dashboard")

    # ---------------- SHOW PAGE ----------------
    def show_page(self, key):
        for k, page in self.pages.items():
            if k == key:
                page.lift()
            else:
                page.lower()

    # ---------------- REFRESH ALL PAGES ----------------
    def refresh_all(self):
        for page in self.refresh_callbacks:
            if hasattr(page, "refresh"):
                page.refresh()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")  # dark green theme
    app = App()
    app.mainloop()
