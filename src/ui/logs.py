import tkinter as tk
from tkinter import ttk
import csv
import os


def open_logs():

    window = tk.Toplevel()

    window.title("Driver Event Logs")

    window.geometry("900x500")

    tree = ttk.Treeview(
        window,
        columns=("Timestamp", "EAR", "Event"),
        show="headings"
    )

    tree.heading("Timestamp", text="Timestamp")
    tree.heading("EAR", text="EAR")
    tree.heading("Event", text="Event")

    tree.column("Timestamp", width=250)
    tree.column("EAR", width=100, anchor="center")
    tree.column("Event", width=400)

    tree.pack(fill="both", expand=True)

    # CSV Path
    csv_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "logs",
        "drowsiness_log.csv"
    )

    csv_path = os.path.abspath(csv_path)

    if os.path.exists(csv_path):

        with open(csv_path, "r") as file:

            reader = csv.reader(file)

            next(reader, None)

            for row in reader:

                tree.insert("", "end", values=row)

    else:

        tree.insert(
            "",
            "end",
            values=("No Log File Found", "", "")
        )