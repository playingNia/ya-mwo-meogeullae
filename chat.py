from color import WHITE, BLACK, GRAY, BLUE

import tkinter as tk
from tkinter import scrolledtext
import os

def send_system_msg(msg):
    global chat_frame, canvas
    msg_frame = tk.Frame(chat_frame, bg=WHITE)
    msg_label = tk.Label(msg_frame, text=msg, bg=GRAY, fg=BLACK, padx=10, pady=5, wraplength=250, justify="left")
    msg_label.pack(anchor='w')
    msg_frame.pack(anchor='w', fill='x', pady=5, padx=10)
    chat_frame.update_idletasks()
    canvas.yview_moveto(1.0)

def send_user_msg(msg):
    global chat_frame, canvas, msg_entry
    msg_frame = tk.Frame(chat_frame, bg=WHITE)
    msg_label = tk.Label(msg_frame, text=msg, bg=BLUE, fg=WHITE, padx=10, pady=5, wraplength=250, justify="left")
    msg_label.pack(anchor='e')
    msg_frame.pack(anchor='e', fill='x', pady=5, padx=10)
    chat_frame.update_idletasks()
    canvas.yview_moveto(1.0)
    msg_entry.delete(0, tk.END)

def on_resize(event):
    global window_id
    canvas_width = event.width
    canvas.itemconfig(window_id, width=canvas_width)

chat_frame = None
canvas = None
msg_entry = None
window_id = None

def load(root):
    global chat_frame, canvas, msg_entry, window_id
    chat_box_frame = tk.Frame(root, height=500)
    chat_box_frame.pack(fill='x')

    canvas = tk.Canvas(chat_box_frame, bg=WHITE, height=500)
    scrollbar = tk.Scrollbar(chat_box_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill='y')
    canvas.pack(fill='x')

    chat_frame = tk.Frame(canvas, bg=WHITE)
    window_id = canvas.create_window((0, 0), window=chat_frame, anchor="nw", width=canvas.winfo_width())
    canvas.bind("<Configure>", on_resize)
    chat_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    msg_entry = tk.Entry(root, width=40)
    msg_entry.pack(pady=10)

    send_button = tk.Button(root, text="전송", command=lambda: send_user_msg(msg=msg_entry.get()))
    send_button.pack()

    send_system_msg("야! 뭐 먹을래?")