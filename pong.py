import tkinter as tk
import time
from random import randint

isRunning = False
gameStarted = False
keys_pressed = set()
x_velocity = 0
y_velocity = 0

def calc_velocity():
    global x_velocity, y_velocity
    x_velocity = randint(-3,3)
    while x_velocity == 0:
        x_velocity = randint(-3,3)
    y_velocity = randint(-5,5)
    while y_velocity == 0:
        y_velocity = randint(-5,5)

def start_game():
    global isRunning, gameStarted
    if not isRunning:
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
        game_loop()

def move_ball():
    global x_velocity, y_velocity
    x_current = ball.winfo_x()
    y_current = ball.winfo_y()

    # for y axis
    if y_current <= 0 or y_current >= 425:
        y_velocity = -y_velocity

    ball.place_configure(x=ball.winfo_x() + x_velocity, y=ball.winfo_y() + y_velocity)
    
    # for x axis
    left_paddle_x = left_paddle.winfo_x() + left_paddle.winfo_width()
    left_paddle_y = left_paddle.winfo_y() - 5
    right_paddle_x = right_paddle.winfo_x()
    right_paddle_y = right_paddle.winfo_y() - 5

    if x_current <= left_paddle_x and y_current >= left_paddle_y and y_current <= left_paddle_y + 105:
        x_velocity = -x_velocity
        ball.place_configure(x=ball.winfo_x() + x_velocity, y=ball.winfo_y() + y_velocity)
    elif x_current + 25 >= right_paddle_x and y_current >= right_paddle_y and y_current <= right_paddle_y + 105:
        x_velocity = -x_velocity
        ball.place_configure(x=ball.winfo_x() + x_velocity, y=ball.winfo_y() + y_velocity)

    elif x_current < 20:
        right_score.config(text=int(right_score.cget("text")) + 1)
        initialize()
    elif x_current > 555:
        left_score.config(text=int(left_score.cget("text")) + 1)
        initialize()

def move_paddles():
    if "w" in keys_pressed:
        move_left_paddle_up()
    if "s" in keys_pressed:
        move_left_paddle_down()
    if "Up" in keys_pressed:
        move_right_paddle_up()
    if "Down" in keys_pressed:
        move_right_paddle_down()

def initialize():
    ball.place_configure(x=287.5, y=225)
    calc_velocity()

def game_loop():
    move_paddles()
    move_ball()
    pong.after(16, game_loop)

# movement functions
def move_left_paddle_up():
    global gameStarted
    if gameStarted:
        if left_paddle.winfo_y() > 15:
            left_paddle.place_configure(y=left_paddle.winfo_y() - 15)

def move_right_paddle_up():
    global gameStarted
    if gameStarted:
        if right_paddle.winfo_y() > 15:
            right_paddle.place_configure(y=right_paddle.winfo_y() - 15)
    
def move_left_paddle_down():
    global gameStarted
    if gameStarted:
        if left_paddle.winfo_y() < 335:
            left_paddle.place_configure(y=left_paddle.winfo_y() + 15)   
    
def move_right_paddle_down():
    global gameStarted
    if gameStarted:
        if right_paddle.winfo_y() < 335:
            right_paddle.place_configure(y=right_paddle.winfo_y() + 15)

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
ball.place(x=287.5, y=225)
drawn_ball = ball.create_oval(0, 0, 25, 25, fill="white")

# start the game
pong.mainloop()
