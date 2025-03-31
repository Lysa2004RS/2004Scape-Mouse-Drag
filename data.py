import tkinter as tk
from tkinter import ttk
from pynput import mouse
import keyboard
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MouseArrows")
        self.root.geometry("360x160")
        self.root.configure(bg="#FFF0F5")
        self.root.resizable(False, False)
        self.root.attributes("-fullscreen", False)

        self.enabled = True
        self.dragging = False
        self.start_x = self.start_y = 0
        self.current_keys = set()
        self.invert_h = tk.BooleanVar(value=True)
        self.invert_v = tk.BooleanVar(value=True)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background="#FFF0F5", borderwidth=0)
        self.style.configure("TFrame", background="#FFF0F5")
        self.style.configure("TCheckbutton", background="#FFF0F5", foreground="#C71585", font=("Arial", 10, "bold"))
        self.style.configure("TNotebook.Tab", background="#FFB6C1", foreground="#C71585", font=("Arial", 10, "bold"), padding=(12, 6), borderwidth=0)
        self.style.map("TNotebook.Tab", background=[("selected", "#FF69B4"), ("active", "#FFD1DC")], foreground=[("selected", "#FFFFFF"), ("active", "#C71585")], padding=[("selected", (20, 8))])
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        self.main_frame = ttk.Frame(self.notebook)
        self.credits_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Main")
        self.notebook.add(self.credits_frame, text="Credits")
        self.build_ui()
        self.listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)
        self.listener.start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        ttk.Checkbutton(self.main_frame, text="Invert Horizontal", variable=self.invert_h).pack(pady=6)
        ttk.Checkbutton(self.main_frame, text="Invert Vertical", variable=self.invert_v).pack(pady=6)
        self.button = tk.Button(self.main_frame, text="Disable", command=self.toggle, bg="#FF69B4", fg="#FFFFFF", font=("Arial", 10, "bold"), relief="flat", borderwidth=0, padx=12, pady=6)
        self.button.pack(pady=10)
        tk.Label(self.credits_frame, text="Made by Lysa\n\nDisclaimer: For accessibility only, not a cheat.", bg="#FFF0F5", fg="#C71585", font=("Arial", 12), justify="center").pack(expand=True)

    def toggle(self):
        self.enabled = not self.enabled
        self.button.config(text="Disable" if self.enabled else "Enable", bg="#FF69B4" if self.enabled else "#FFB6C1")
        if not self.enabled:
            self.release_all_keys()
            self.dragging = False

    def on_click(self, x, y, button, pressed):
        if not self.enabled or button != mouse.Button.middle:
            return
        self.dragging = pressed
        if pressed:
            self.start_x, self.start_y = x, y
        self.release_all_keys()

    def on_move(self, x, y):
        if not self.enabled or not self.dragging:
            return
        dx, dy = x - self.start_x, y - self.start_y
        keys = set()
        if dx:
            keys.add('left' if (dx < 0) ^ self.invert_h.get() else 'right')
        if dy:
            keys.add('up' if (dy < 0) ^ self.invert_v.get() else 'down')
        for k in keys - self.current_keys:
            keyboard.press(k)
            self.current_keys.add(k)
        for k in self.current_keys - keys:
            keyboard.release(k)
            self.current_keys.remove(k)

    def release_all_keys(self):
        for k in list(self.current_keys):
            keyboard.release(k)
            self.current_keys.remove(k)

    def on_close(self):
        self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    threading.Thread(target=lambda: App(tk.Tk()).root.mainloop()).start()
