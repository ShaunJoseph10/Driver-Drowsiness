import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


current_index = 0
images = []


def load_images():

    global images

    screenshot_folder = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "screenshots"
        )
    )

    if os.path.exists(screenshot_folder):

        images = [

            os.path.join(screenshot_folder, file)

            for file in os.listdir(screenshot_folder)

            if file.lower().endswith((".png", ".jpg", ".jpeg"))

        ]

        images.sort()


def open_gallery():

    global current_index

    load_images()

    if len(images) == 0:

        messagebox.showinfo(
            "Screenshots",
            "No screenshots found."
        )

        return

    window = tk.Toplevel()

    window.title("Screenshot Gallery")

    window.geometry("900x650")

    image_label = tk.Label(window)

    image_label.pack(pady=20)

    filename_label = tk.Label(
        window,
        font=("Arial",12)
    )

    filename_label.pack()


    def show_image():

        img = Image.open(images[current_index])

        img.thumbnail((750,500))

        photo = ImageTk.PhotoImage(img)

        image_label.configure(image=photo)

        image_label.image = photo

        filename_label.config(
            text=os.path.basename(images[current_index])
        )


    def next_image():

        global current_index

        if current_index < len(images)-1:

            current_index += 1

            show_image()


    def previous_image():

        global current_index

        if current_index > 0:

            current_index -= 1

            show_image()


    tk.Button(

        window,

        text="◀ Previous",

        command=previous_image,

        width=15

    ).pack(side="left", padx=50, pady=20)


    tk.Button(

        window,

        text="Next ▶",

        command=next_image,

        width=15

    ).pack(side="right", padx=50, pady=20)


    show_image()