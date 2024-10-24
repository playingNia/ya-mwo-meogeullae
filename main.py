import chat
from color import WHITE, BLACK, BLUE
from chat import load

import tkinter as tk
import tkinter.font as tkFont
import os

root = tk.Tk()
root.title("야! 뭐 먹을래?")
root.geometry("450x750+0+0")
root.resizable(False, False)
root.configure(bg=WHITE)

font = tkFont.Font(family="Arial", size=12, weight="bold")
root.option_add("*Font", font)

page = "main"
popup_opened = False

def remove_wigets():
    for widget in root.pack_slaves():
        widget.pack_forget()

def submit_api_key(key):
    global root, popup_opened
    if key == "":
        return

    popup_opened = False
    with open("api-key.txt", 'w') as f:
        f.write(key)

    remove_wigets()
    load()

def open_chat():
    global page, root
    page = "chat"
    remove_wigets()
    chat.load(root)

def load():
    if popup_opened:
        frame = tk.Frame(root, bg=WHITE)
        frame.pack(expand=True, anchor="center")

        label = tk.Label(frame, text="Open AI API key를 입력하세요.", bg=WHITE, fg=BLACK)
        label.pack()

        entry = tk.Entry(frame, width=34, fg=BLACK)
        entry.pack(pady=10)

        btn = tk.Button(frame, text="완료", bg=BLUE, fg=WHITE, width=30, height=2, relief="flat", command=lambda: submit_api_key(entry.get()))
        btn.pack()
    else:
        btn = tk.Button(root, text="메뉴 정하러 가기", bg=BLUE, fg=WHITE, relief="flat", pady=10, padx=10, command=lambda: open_chat())
        btn.pack(expand=True, anchor="center")

if page == "main":
    if not os.path.exists("api-key.txt"):
        popup_opened = True

    load()

root.mainloop()