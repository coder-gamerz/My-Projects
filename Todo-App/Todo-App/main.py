import customtkinter as ctk
import getpass
from packages import *

USER_NAME = getpass.getuser()

AT_THE_BEGINNING = True

STORAGE = rf"C:\Users\shrey\OneDrive\Documents\My-Projects\Todo-App\Todo-App\tasks.txt"


def save_todo():
    file = open(STORAGE, "w")

    for frame in scrollable_frame.winfo_children():
        for widget in frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                file = open(STORAGE, "a")
                file.write(f"{widget.cget('text')}\n")

    file.close()


def delete_todo(item, content):
    item.destroy()

    save_todo()


def add_todo(_text=""):
    def add(t):
        frame = ctk.CTkFrame(scrollable_frame)

        label = ctk.CTkLabel(frame, text=t, font=ctk.CTkFont(size=18), width=670)

        delete_check = ctk.CTkCheckBox(
            frame, text="", command=lambda: delete_todo(frame, label)
        )

        frame.pack()
        label.grid(row=0, column=1)
        delete_check.grid(row=0, column=0)

        entry.delete(0, ctk.END)

        save_todo()

    todo = entry.get()

    if todo != "":
        add(todo)
    else:
        if _text != "":
            add(_text)


def check_keypress(event):
    if event.keysym == "Return":
        add_todo()


window = ctk.CTk()
window.geometry("750x450")
window.title("ToDo App")


title_label = ctk.CTkLabel(
    window, text="Daily Tasks", font=ctk.CTkFont(size=20, weight="bold")
)
title_label.grid(row=0, column=0, padx=10, pady=10)


scrollable_frame = ctk.CTkScrollableFrame(window, width=700, height=370)
scrollable_frame.grid(row=1, column=0, padx=10, pady=(0, 20))


entry_container = ctk.CTkFrame(scrollable_frame, width=700)
entry_container.pack()


entry = ctk.CTkEntry(entry_container, placeholder_text="Add item", width=670)
entry.grid(row=0, column=0, padx=(0, 5))


add_button = ctk.CTkButton(
    entry_container,
    text="+ ",
    font=ctk.CTkFont(size=18, weight="bold"),
    width=30,
    command=add_todo,
)
add_button.grid(row=0, column=1)


window.bind("<KeyPress>", check_keypress)


if AT_THE_BEGINNING:
    try:
        file = open(STORAGE, "r")
        lines = file.read().splitlines()
        file.close()

        for line in lines:
            add_todo(line)

    except FileNotFoundError:
        print(f"Failed to open {STORAGE}")

    AT_THE_BEGINNING = False


window.mainloop()
