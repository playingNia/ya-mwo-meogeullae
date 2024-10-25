from color import WHITE, BLACK, GRAY, BLUE

import tkinter as tk
import tkinter.font as tkFont
import os
import openai
import time
from datetime import datetime

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
    load_main()

def open_chat():
    global page, root
    page = "chat"
    remove_wigets()
    load_chat()

def load_main():
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

if not os.path.exists("api-key.txt"):
    popup_opened = True

load_main()





















































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

def on_resize(event):
    global window_id
    canvas_width = event.width
    canvas.itemconfig(window_id, width=canvas_width)

chat_frame = None
canvas = None
msg_entry = None
window_id = None

select_frame = None
option_btns = []

def load_chat():
    global root, chat_frame, canvas, msg_entry, window_id, select_frame
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

    select_frame = tk.Frame(root, height=250, bg=WHITE)
    select_frame.pack(pady=10, expand=True)

    send_system_msg("야! 뭐 먹을래?")

    time.sleep(1.5)
    send_user_msg("그러게...")

    time.sleep(1.5)
    send_system_msg("무슨 음식 먹고 싶어?")
    ask_food_type()

def remove_option_btn():
    for btn in option_btns:
        btn.destroy()
    option_btns.clear()

food_type = None
food_spicy = None
food_hot = None

def select_food_type(type):
    global food_type
    food_type = type

    remove_option_btn()
    send_user_msg(type + '!')

    time.sleep(1.5)
    send_system_msg("매운 음식은 어때?")
    ask_spicy_type()

def ask_food_type():
    button1 = tk.Button(select_frame, text="한식", width=15, height=2, bg=BLUE, fg=WHITE, relief="flat", command=lambda: select_food_type("한식"))
    button1.grid(row=0, column=0, padx=5, pady=5)
    option_btns.append(button1)

    button2 = tk.Button(select_frame, text="양식", width=15, height=2, bg=BLUE, fg=WHITE, relief="flat", command=lambda: select_food_type("양식"))
    button2.grid(row=0, column=1, padx=5, pady=5)
    option_btns.append(button2)

    button3 = tk.Button(select_frame, text="중식", width=15, height=2, bg=BLUE, fg=WHITE, relief="flat", command=lambda: select_food_type("중식"))
    button3.grid(row=1, column=0, padx=5, pady=5)
    option_btns.append(button3)

    button4 = tk.Button(select_frame, text="일식", width=15, height=2, bg=BLUE, fg=WHITE, relief="flat", command=lambda: select_food_type("일식"))
    button4.grid(row=1, column=1, padx=5, pady=5)
    option_btns.append(button4)

def select_spicy_type(type):
    global food_spicy
    food_spicy = type

    remove_option_btn()
    user_msg = "오늘은 매운 게 조금 당기긴 하네~" if type else "매운 건 조금 그렇네..."
    send_user_msg(user_msg)

    time.sleep(1.5)
    send_system_msg("그럼 뜨거운 거 아니면 차가운 거?")
    ask_hot_type()

def ask_spicy_type():
    button1 = tk.Button(select_frame, text="매워도 괜찮아", width=40, height=2, bg=BLUE, fg=WHITE, relief="flat", command=lambda: select_spicy_type(True))
    button1.grid(row=0, column=0, pady=5)
    option_btns.append(button1)

    button2 = tk.Button(select_frame, text="매운 건 조금...", width=40, height=2, bg=GRAY, fg=BLACK, relief="flat", command=lambda: select_spicy_type(False))
    button2.grid(row=1, column=0, pady=5)
    option_btns.append(button2)

def select_hot_type(type):
    global food_hot
    food_hot = True

    remove_option_btn()
    user_msg = "따뜻한 거로 가자~" if type else "시원한 거로 가자~"
    send_user_msg(user_msg)

    time.sleep(1.5)
    send_system_msg("잠시만...")

    food = get_food()
    send_system_msg(f"{food} 어때?")
    ask_satisfied(food)

def ask_hot_type():
    button1 = tk.Button(select_frame, text="따뜻한 거 먹을래!", width=40, height=2, bg=BLUE, fg=WHITE, relief="flat", command=lambda: select_hot_type(True))
    button1.grid(row=0, column=0, pady=5)
    option_btns.append(button1)

    button2 = tk.Button(select_frame, text="시원한 거 먹을래!", width=40, height=2, bg=GRAY, fg=BLACK, relief="flat", command=lambda: select_hot_type(False))
    button2.grid(row=1, column=0, pady=5)
    option_btns.append(button2)

def get_food():
    with open("api-key.txt", "r") as file:
        api_key = file.read()
    openai.api_key = api_key

    current_time = datetime.now().strftime("%H:%M")
    question = f"""
                지금 {current_time}인데 음식 메뉴 추천해줘.
                - {food_type}
                - {"매운 거" if food_spicy else "안 매운 거"}
                - {"따뜻한 거" if food_hot else "시원한 거"}
                다른 텍스트 붙이지 말고, 음식 이름만 출력해 줘.
                """

    response = openai.completions.create(
        model="gpt-3.5-turbo",
        prompt=question,
        max_tokens=25
    )
    print(f"GPT : {response.choices[0]['text']}")
    return response.choices[0]["text"]

# def get_other_food():
#     response = openai.Completion.create(
#         model="gpt-3.5-turbo",
#         prompt="다른 거",
#         max_tokens=50,
#         temperature=0.8
#     )
#
#     return response.choices[0].text.strip()

def satisfied():
    global page
    page = "main"
    remove_wigets()
    load_main()

def ask_satisfied(food):
    button1 = tk.Button(select_frame, text=f"{food} 좋아!", width=40, height=2, bg=BLUE, fg=WHITE, relief="flat", command=lambda: satisfied())
    button1.grid(row=0, column=0, pady=5)
    option_btns.append(button1)

    # TODO: 마음에 안들 때
    button2 = tk.Button(select_frame, text=f"{food}은(는) 별로... 다른 거 없을까?", width=40, height=2, bg=GRAY, fg=BLACK, relief="flat", command=lambda: select_hot_type(False))
    button2.grid(row=1, column=0, pady=5)
    option_btns.append(button2)

root.mainloop()