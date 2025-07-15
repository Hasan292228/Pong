import tkinter as tk
import time
from random import randint

isRunning = False
gameStarted = False
keys_pressed = set()
x_velocity = 0
y_velocity = 0

def start_game():
    global isRunning, gameStarted
    if isRunning:
        return
    isRunning = True
    y = 0
    game_frame.place(x=0, y=-450)
    while y < 450:
        y += 1
        start_frame.place_configure(y=y)
        game_frame.place_configure(y=y-450)
        time.sleep(0.001)
        pong.update()
    start_frame.place_forget()
    gameStarted = True
    initialize()
    loop()

def move_ball():
    global x_velocity, y_velocity

    ball.place_configure(x=ball.winfo_x() + x_velocity, y=ball.winfo_y() + y_velocity)

    # ball touches top or bottom
    if ball.winfo_y() <= 0:
        y_velocity = -y_velocity
        ball.place_configure(x=ball.winfo_x() + x_velocity, y=ball.winfo_y() + 10)
        return
    if ball.winfo_y() + 25 >= 450:
        y_velocity = -y_velocity
        ball.place_configure(x=ball.winfo_x(), y=ball.winfo_y() - 10)
        return

    # ball touches paddles
    if ball.winfo_x() <= left_paddle.winfo_x() + 15 and ball.winfo_y() >= left_paddle.winfo_y() - 5 and ball.winfo_y() <= left_paddle.winfo_y() + 105:
        inc_speed()
        x_velocity = -x_velocity
        ball.place_configure(x=ball.winfo_x() + 10, y=ball.winfo_y())
        return
    if ball.winfo_x() + 25 >= right_paddle.winfo_x() - 5 and ball.winfo_y() >= right_paddle.winfo_y() - 5 and ball.winfo_y() <= right_paddle.winfo_y() + 105:
        inc_speed()
        x_velocity = -x_velocity
        ball.place_configure(x=ball.winfo_x() - 10, y=ball.winfo_y())
        return

    # ball doesnt touch any paddle
    if ball.winfo_x() < 15:
        right_score.config(text=int(right_score.cget("text")) + 1)
        initialize()
        return
    if ball.winfo_x() + 25 > 585:
        left_score.config(text=int(left_score.cget("text")) + 1)
        initialize()
        return

def move_paddles():
    global gameStarted
    if not gameStarted:
        return
    if "w" in keys_pressed:
        if left_paddle.winfo_y() >= 15:
            left_paddle.place_configure(y=left_paddle.winfo_y() - 15)
    if "s" in keys_pressed:
        if left_paddle.winfo_y() <= 335:
            left_paddle.place_configure(y=left_paddle.winfo_y() + 15)
    if "Up" in keys_pressed:
        if right_paddle.winfo_y() >= 15:
            right_paddle.place_configure(y=right_paddle.winfo_y() - 15)
    if "Down" in keys_pressed:
        if right_paddle.winfo_y() <= 335:
            right_paddle.place_configure(y=right_paddle.winfo_y() + 15)

def initialize():
    global x_velocity, y_velocity

    ball.place_configure(x=288, y=225)

    randomint = randint(0, 1)
    x_velocity = randint(1, 3) if randomint == 0 else -randint(1, 3)
    randomint = randint(0, 1)
    y_velocity = randint(1, 3) if randomint == 0 else -randint(1, 3)

def inc_speed():
    global x_velocity, y_velocity
    if x_velocity > -10 and x_velocity < 10:
        if x_velocity > 0:
            x_velocity += 1
        else:
            x_velocity -= 1
    if y_velocity > -10 and y_velocity < 10:
        if y_velocity > 0:
            y_velocity += 1
        else:
            y_velocity -= 1

def loop():
    move_paddles()
    move_ball()
    pong.after(16, loop)

# create the main window
pong = tk.Tk()
pong.title("Pong")
pong.geometry("600x450")
pong.resizable(False, False)
pong.configure(bg="black")

# binds for paddle movement
pong.bind("<KeyPress>", lambda event: keys_pressed.add(event.keysym))  
pong.bind("<KeyRelease>", lambda event: keys_pressed.discard(event.keysym))

# start frame
start_frame = tk.Frame(pong, width=600, height=450, bg="black")
start_frame.place(x=0, y=0)

# pong label
pong_label = tk.Label(start_frame, text="Pong", font=("Monaco", 50), bg="black", fg="white")
pong_label.place(x=210, y=50)

# single player button
single_play_button = tk.Button(start_frame, text="Single Player", width=20, font=("Monaco", 20), bg="#AAAAAA", fg="black", command=lambda: start_game())
single_play_button.place(x=150, y=200)

# two player button
two_play_button = tk.Button(start_frame, text="Two Players", width=20, font=("Monaco", 20), bg="#AAAAAA", fg="black", command=lambda: start_game())
two_play_button.place(x=150, y=250)

# game frame
game_frame = tk.Frame(pong, width=600, height=450, bg="black")

# create center bar
center_bar = tk.Frame(game_frame, width=5, height=450, bg="#AAAAAA")
center_bar.place(x=297.5, y=0)

# create left paddle
left_paddle = tk.Frame(game_frame, width=10, height=100, bg="white")
left_paddle.place(x=10, y=175)  

# create right paddle
right_paddle = tk.Frame(game_frame, width=10, height=100, bg="white")
right_paddle.place(x=580, y=175)

# create left score label
left_score = tk.Label(game_frame, text="0", font=("Monaco", 30), bg="black", fg="white")
left_score.place(x=170, y=20)       

# create right score label
right_score = tk.Label(game_frame, text="0", font=("Monaco", 30), bg="black", fg="white")
right_score.place(x=400, y=20)

# create ball
ball = tk.Canvas(game_frame, width=25, height=25, bg="black", highlightthickness=0)
ball.place(x=288, y=225)
drawn_ball = ball.create_oval(0, 0, 25, 25, fill="white")

# start the game
pong.mainloop()