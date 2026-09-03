import os
import sys
import subprocess
import customtkinter as ctk
from PIL import Image

from ui.logs import open_logs
from ui.gallery import open_gallery
from ui.report import open_report
from ui.about import open_about


# -----------------------------
# Resource Path (Works in EXE)
# -----------------------------
def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        # Running from PyInstaller EXE
        base_path = os.path.join(os.path.dirname(sys.executable), "_internal")
    else:
        # Running from Python
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base_path, relative_path)


background_path = resource_path("assets/background.png")
icon_path = resource_path("assets/icon.ico")

# -----------------------------
# Window
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Driver Drowsiness Detection System")
root.geometry("1200x760")
root.resizable(False, False)

if os.path.exists(icon_path):
    root.iconbitmap(icon_path)


# -----------------------------
# Background Image
# -----------------------------
background = ctk.CTkImage(
    light_image=Image.open(background_path),
    dark_image=Image.open(background_path),
    size=(1200, 760)
)

bg = ctk.CTkLabel(
    root,
    image=background,
    text=""
)

bg.place(
    relwidth=1,
    relheight=1
)


# -----------------------------
# Title
# -----------------------------
title = ctk.CTkLabel(
    root,
    text="Driver Drowsiness Detection System",
    font=("Segoe UI", 28, "bold"),
    text_color="white"
)

title.pack(pady=(35, 20))


# -----------------------------
# Main Frame
# -----------------------------
frame = ctk.CTkFrame(
    root,
    width=450,
    height=470,
    corner_radius=20,
    fg_color="#1F2A44"
)

frame.pack(pady=10)
frame.pack_propagate(False)

# -----------------------------
# Button Functions
# -----------------------------
def start_detection():
    if getattr(sys, "frozen", False):
        # Running as menu.exe
        exe_path = os.path.join(
            os.path.dirname(sys.executable),
            "..",
            "main",
            "main.exe"
        )
        exe_path = os.path.abspath(exe_path)

        subprocess.Popen([exe_path])

    else:
        # Running from VS Code
        subprocess.Popen(
            [sys.executable, os.path.join(os.path.dirname(__file__), "main.py")]
        )


def exit_app():
    root.destroy()


# -----------------------------
# Buttons
# -----------------------------
btn_width = 260
btn_height = 48

start_btn = ctk.CTkButton(
    frame,
    text="▶ Start Detection",
    width=btn_width,
    height=btn_height,
    corner_radius=12,
    font=("Segoe UI", 18, "bold"),
    fg_color="#0078D7",
    hover_color="#005A9E",
    command=start_detection
)

logs_btn = ctk.CTkButton(
    frame,
    text="📄 View Logs",
    width=btn_width,
    height=btn_height,
    corner_radius=12,
    font=("Segoe UI", 18),
    command=open_logs
)

gallery_btn = ctk.CTkButton(
    frame,
    text="🖼 Screenshots",
    width=btn_width,
    height=btn_height,
    corner_radius=12,
    font=("Segoe UI", 18),
    command=open_gallery
)

report_btn = ctk.CTkButton(
    frame,
    text="📊 Generate Report",
    width=btn_width,
    height=btn_height,
    corner_radius=12,
    font=("Segoe UI", 18),
    command=open_report
)

about_btn = ctk.CTkButton(
    frame,
    text="ℹ About Project",
    width=btn_width,
    height=btn_height,
    corner_radius=12,
    font=("Segoe UI", 18),
    command=open_about
)

exit_btn = ctk.CTkButton(
    frame,
    text="❌ Exit",
    width=btn_width,
    height=btn_height,
    corner_radius=12,
    font=("Segoe UI", 18),
    fg_color="#C62828",
    hover_color="#8E0000",
    command=exit_app
)

start_btn.pack(pady=(30, 15))
logs_btn.pack(pady=10)
gallery_btn.pack(pady=10)
report_btn.pack(pady=10)
about_btn.pack(pady=10)
exit_btn.pack(pady=(20, 10))


# -----------------------------
# Footer
# -----------------------------
footer = ctk.CTkLabel(
    root,
    text="© 2026 Driver Drowsiness Detection System",
    font=("Segoe UI", 12),
    text_color="lightgray"
)

footer.pack(side="bottom", pady=15)


root.mainloop()