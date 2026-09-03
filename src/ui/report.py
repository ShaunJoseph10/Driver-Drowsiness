import tkinter as tk
from tkinter import messagebox
import csv
import os


def open_report():

    report = tk.Toplevel()

    report.title("Driver Report")
    report.geometry("600x520")
    report.configure(bg="#1e1e1e")
    report.resizable(False, False)

    log_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "logs",
            "drowsiness_log.csv"
        )
    )

    screenshot_folder = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "screenshots"
        )
    )

    title = tk.Label(
        report,
        text="Driver Report",
        font=("Arial", 20, "bold"),
        bg="#1e1e1e",
        fg="white"
    )

    title.pack(pady=20)

    info_label = tk.Label(
        report,
        justify="left",
        font=("Consolas", 14),
        bg="#1e1e1e",
        fg="white"
    )

    info_label.pack(pady=20)


    def load_report():

        yawns = 0
        alerts = 0
        total_events = 0

        if os.path.exists(log_file):

            with open(log_file, "r") as file:

                reader = csv.DictReader(file)

                for row in reader:

                    total_events += 1

                    if row["Event"] == "Yawn Detected":
                        yawns += 1

                    elif row["Event"] == "Drowsiness Detected":
                        alerts += 1

        screenshots = 0

        if os.path.exists(screenshot_folder):

            screenshots = len([
                f for f in os.listdir(screenshot_folder)
                if f.lower().endswith((".jpg", ".png", ".jpeg"))
            ])

        if alerts == 0:
            status = "SAFE"

        elif alerts < 5:
            status = "FATIGUED"

        else:
            status = "DROWSY"

        report_text = (
            f"{'🥱 Total Yawns':<30}: {yawns}\n\n"
            f"{'🚨 Drowsiness Alerts':<30}: {alerts}\n\n"
            f"{'📷 Screenshots Captured':<30}: {screenshots}\n\n"
            f"{'📄 Total Events Logged':<30}: {total_events}\n\n"
            f"{'😊 Driver Status':<30}: {status}"
        )

        info_label.config(text=report_text)


    def reset_report():

        answer = messagebox.askyesno(
            "Reset Report",
            "Delete all logs and screenshots?"
        )

        if not answer:
            return

        if os.path.exists(log_file):

            with open(log_file, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Timestamp",
                    "EAR",
                    "Event"
                ])

        if os.path.exists(screenshot_folder):

            for file in os.listdir(screenshot_folder):

                if file.lower().endswith((".jpg", ".png", ".jpeg")):

                    os.remove(
                        os.path.join(
                            screenshot_folder,
                            file
                        )
                    )

        messagebox.showinfo(
            "Success",
            "Report has been reset."
        )

        load_report()


    load_report()


    tk.Button(
        report,
        text="🔄 Refresh",
        width=20,
        height=2,
        bg="#2196F3",
        fg="white",
        command=load_report
    ).pack(pady=5)


    tk.Button(
        report,
        text="🗑 Reset Report",
        width=20,
        height=2,
        bg="orange",
        fg="black",
        command=reset_report
    ).pack(pady=5)


    tk.Button(
        report,
        text="❌ Close",
        width=20,
        height=2,
        bg="red",
        fg="white",
        command=report.destroy
    ).pack(pady=15)