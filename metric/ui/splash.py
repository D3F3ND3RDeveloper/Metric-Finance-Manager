import customtkinter as ctk
from config import THEME, APP_NAME, LOGO_PATH
from PIL import Image
from customtkinter import CTkImage

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent, on_finish):
        super().__init__(parent)
        self.on_finish = on_finish

        self.overrideredirect(True)  # No window border
        self.configure(fg_color=THEME["background"])
        self.attributes("-alpha", 0.0)

        # Set size
        self.width, self.height = 420, 260
        self.geometry(f"{self.width}x{self.height}")

        # Center splash on screen
        self.center_window()

        # Container frame to truly center content
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")  # <- perfectly center

        # Logo
        logo_img = CTkImage(Image.open(LOGO_PATH), size=(90, 90))
        ctk.CTkLabel(content_frame, image=logo_img, text="").pack(pady=(0, 10))

        # App Name
        ctk.CTkLabel(
            content_frame,
            text=APP_NAME,
            font=("Segoe UI", 22, "bold"),
            text_color=THEME["primary"]
        ).pack()

        # Fade-in animation
        self.fade_in(0)

    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def fade_in(self, alpha):
        if alpha < 1:
            self.attributes("-alpha", alpha)
            self.after(25, lambda: self.fade_in(alpha + 0.05))
        else:
            self.after(1200, self.finish)

    def finish(self):
        self.destroy()
        self.on_finish()
