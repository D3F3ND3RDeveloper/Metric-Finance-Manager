# utils/animations.py

"""
Animations for Metric App UI
- fade_in_window: Smoothly fades in a Tkinter window
- slide_in: Slides a widget in from the left
- hover_lift: Lifts a widget on hover with optional border color change
"""

def fade_in_window(window, steps=20, delay=15):
    """
    Fade in the window smoothly.
    
    Args:
        window: Tkinter window or Toplevel
        steps: number of steps for fade
        delay: delay in ms between steps
    """
    def step(i=0):
        if i <= steps:
            window.attributes("-alpha", i / steps)
            window.after(delay, lambda: step(i + 1))
    step()


def slide_in(widget, steps=20, delay=10):
    """
    Slide a widget in from the left side.

    Args:
        widget: Tkinter or CTkFrame widget
        steps: number of steps for animation
        delay: delay in ms between steps
    """
    widget.update_idletasks()
    width = widget.winfo_width()
    widget.place(x=-width, y=widget.winfo_y(), relheight=1)
    
    def animate(pos=-width):
        if pos < 0:
            widget.place(x=pos, y=widget.winfo_y())
            widget.after(delay, lambda: animate(pos + max(1, width // steps)))
        else:
            widget.place(x=0, y=widget.winfo_y())
    
    animate()


def hover_lift(widget, lift_amount=4, color=None):
    """
    Makes a CTkFrame or widget lift slightly on hover.
    
    Args:
        widget: Tkinter or CTkFrame
        lift_amount: pixels to lift up
        color: optional border color on hover
    """
    default_border = widget.cget("border_color") if "border_color" in widget.keys() else None

    def on_enter(_):
        widget.place_configure(y=widget.winfo_y() - lift_amount)
        if color and "border_color" in widget.keys():
            widget.configure(border_color=color)

    def on_leave(_):
        widget.place_configure(y=widget.winfo_y() + lift_amount)
        if color and "border_color" in widget.keys():
            widget.configure(border_color=default_border)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)
