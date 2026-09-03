import customtkinter as ctk


def open_about():

    about = ctk.CTkToplevel()

    about.title("About Project")

    about.geometry("700x600")

    about.resizable(False, False)

    about.grab_set()

    title = ctk.CTkLabel(
        about,
        text="Driver Drowsiness Detection System",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=(25, 10))

    subtitle = ctk.CTkLabel(
        about,
        text="AI Powered Driver Safety Monitoring",
        font=("Arial", 18)
    )

    subtitle.pack(pady=5)

    description = """
This application monitors the driver's alertness in real-time
using Artificial Intelligence and Computer Vision.

FEATURES

• Eye Aspect Ratio (EAR) based eye closure detection

• Blink Detection

• Yawn Detection (MAR)

• Head Pose Estimation

• Real-Time Drowsiness Detection

• Alarm System

• Automatic Screenshot Capture

• Event Logging (CSV)

• Screenshot Gallery

• Driver Report Dashboard

TECHNOLOGIES USED

• Python

• OpenCV

• MediaPipe Face Mesh

• NumPy

• CustomTkinter

• CSV

• Pillow

Developed as an AI & Machine Learning Mini Project.
"""

    info = ctk.CTkTextbox(
        about,
        width=620,
        height=360,
        font=("Arial", 15)
    )

    info.pack(pady=20)

    info.insert("1.0", description)

    info.configure(state="disabled")

    close_btn = ctk.CTkButton(
        about,
        text="Close",
        width=180,
        height=40,
        fg_color="red",
        hover_color="#990000",
        command=about.destroy
    )

    close_btn.pack(pady=20)