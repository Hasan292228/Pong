import tkinter as tk
import time
from random import randint


isRunning = False
keys_pressed = set()
x_velocity = 0
y_velocity = 0
bot_paddle_speed = 0
difficulty = 'None' # Easy, Normal, Impossible
mode = 'TP' # SP, TP


def start_game_two():
    global isRunning
    if isRunning:
        return
    isRunning = True
    y = 0
    game_frame.place(x=0, y=-450)
    while y < 450:
        y += 1
        start_frame.place_configure(y=y)
        game_frame.place_configure(y=y-450)
        pong.update()
    initialize()
    loop()

def game_options():
    global isRunning
    if isRunning:
        return
    isRunning = True
    y = 0
    options_frame.place(x=0, y=-450)
    while y < 450:
        y += 1
        start_frame.place_configure(y=y)
        options_frame.place_configure(y=y-450)
        pong.update()

def start_game_single():
    global mode
    mode = 'SP'
    y = 0
    game_frame.place(x=0, y=-450)
    while y < 450:
        y += 1
        options_frame.place_configure(y=y)
        game_frame.place_configure(y=y-450)
        pong.update()
    initialize()
    loop()

def reset_game():
    global isRunning, difficulty, mode, bot_paddle_speed
    if not isRunning:
        return
    isRunning = False
    difficulty = 'None'
    mode = 'TP'
    bot_paddle_speed = 0
    left_score.configure(text='0')
    right_score.configure(text='0')
    initialize()
    winner_frame.place(x=0, y=-450)
    options_frame.place(x=0, y=-450)
    game_frame.place(x=0, y=-450)
    start_frame.place(x=0, y=0)

def initialize():
    global x_velocity, y_velocity
    
    ball.place_configure(x=288, y=225)
    left_paddle.place_configure(x=10, y=175)
    right_paddle.place_configure(x=580, y=175)
    pong.update()

    time.sleep(0.5)

    random_int = randint(0, 1)
    x_velocity = randint(2, 4) if random_int == 0 else -randint(2, 4)
    random_int = randint(0, 1)
    y_velocity = randint(2, 4) if random_int == 0 else -randint(2, 4)

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

def set_diff(diff):
    global difficulty, bot_paddle_speed
    if difficulty != 'None':
        return
    elif diff == 'Easy':
        difficulty = 'Easy'
        bot_paddle_speed = 3
    elif diff == 'Normal':
        difficulty = 'Normal'
        bot_paddle_speed = 4
    elif diff == 'Impossible':
        difficulty = 'Impossible'
        bot_paddle_speed = 8
    start_game_single()

def move_ball():
    global x_velocity, y_velocity

    ball_left = ball.winfo_x()
    ball_right = ball.winfo_x() + 25
    ball_top = ball.winfo_y()
    ball_bottom = ball.winfo_y() + 25

    left_paddle_left = left_paddle.winfo_x()
    left_paddle_right = left_paddle.winfo_x() + 10
    left_paddle_top = left_paddle.winfo_y()
    left_paddle_bottom = left_paddle.winfo_y() + 100

    right_paddle_left = right_paddle.winfo_x()
    right_paddle_right = right_paddle.winfo_x() + 10
    right_paddle_top = right_paddle.winfo_y()
    right_paddle_bottom = right_paddle.winfo_y() + 100
    
    ball.place_configure(x=ball_left + x_velocity, y=ball_top + y_velocity)

    # ball hits top or bottom
    if ball_top <= 0:
        y_velocity = -y_velocity
        ball.place_configure(x=ball_left, y=1)
        return
    elif ball_bottom >= 450:
        y_velocity = -y_velocity
        ball.place_configure(x=ball_left, y=424)
        return

    # ball hits paddles
    if (ball_left <= left_paddle_right and ball_right >= left_paddle_left and ball_top <= left_paddle_bottom and ball_bottom >= left_paddle_top):
        x_velocity = -x_velocity
        inc_speed()
        ball.place_configure(x=21, y=ball_top)
        return
    if (ball_right >= right_paddle_left and ball_left <= right_paddle_left and ball_top <= right_paddle_bottom and ball_bottom >= right_paddle_top):
        x_velocity = -x_velocity
        inc_speed()
        ball.place_configure(x=554, y=ball_top)
        return 

    # ball didnt hit any paddle
    if ball.winfo_x() < 15:
        right_score.config(text=int(right_score.cget("text")) + 1)
        initialize()
        return
    if ball.winfo_x() + 25 > 585:
        left_score.config(text=int(left_score.cget("text")) + 1)
        initialize()
        return

def paddle_movement():
    global mode
    if "w" in keys_pressed:
        if left_paddle.winfo_y() >= 15:
            left_paddle.place_configure(y=left_paddle.winfo_y() - 15)
    if "s" in keys_pressed:
        if left_paddle.winfo_y() <= 335:
            left_paddle.place_configure(y=left_paddle.winfo_y() + 15)
    if mode != 'TP':
        return
    if "Up" in keys_pressed:
        if right_paddle.winfo_y() >= 15:
            right_paddle.place_configure(y=right_paddle.winfo_y() - 15)
    if "Down" in keys_pressed:
        if right_paddle.winfo_y() <= 335:
            right_paddle.place_configure(y=right_paddle.winfo_y() + 15)

def move_right_paddle():
    global difficulty, x_velocity, y_velocity, bot_paddle_speed
    if x_velocity < 0 and difficulty == 'Easy':
        return
    if ball.winfo_y() + 12.5 < right_paddle.winfo_y() + 50:
        if right_paddle.winfo_y() >= 15:
            right_paddle.place_configure(y=right_paddle.winfo_y() - bot_paddle_speed)
    elif ball.winfo_y() + 12.5 > right_paddle.winfo_y() + 50:
        if right_paddle.winfo_y() <= 335:
            right_paddle.place_configure(y=right_paddle.winfo_y() + bot_paddle_speed)  

def check_winner():
    global mode
    if int(left_score.cget('text')) == 5:
            game_frame.place(x=0, y=-450)
            winner_label.configure(text='Player 1 Won!' if mode == 'TP' else 'You Won!')
            pong.update()
            winner_frame.place(x=0, y=0)
            return True
    if int(right_score.cget('text')) == 5:
        game_frame.place(x=0, y=-450)
        winner_label.configure(text='Player 2 Won!' if mode == 'TP' else 'You Lost!')
        pong.update()
        winner_frame.place(x=0, y=0)
        return True

def loop():
    global mode, difficulty
    paddle_movement()
    move_ball()
    if mode == 'SP':
        move_right_paddle()
    if 'Escape' in keys_pressed:
        reset_game()
        return
    if check_winner():
        pong.after(2000, reset_game)
        return
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
pong_label.place(x=222, y=50)

# single player button
single_play_button = tk.Button(start_frame, text="Single Player", width=15, font=("Monaco", 20), bg="#AAAAAA", fg="black", command=game_options)
single_play_button.place(x=182, y=200)

# two player button
two_play_button = tk.Button(start_frame, text="Two Player", width=15, font=("Monaco", 20), bg="#AAAAAA", fg="black", command=start_game_two)
two_play_button.place(x=182, y=250)


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


# options frame
options_frame = tk.Frame(pong, width=600, height=450, bg="black")

# create difficulty label
difficulty_label = tk.Label(options_frame, text="Difficulty:", font=("Monaco", 30), bg="black", fg="white")
difficulty_label.place(x=180, y=50)

# easy mode button
easy_mode = tk.Button(options_frame, text="Easy", width=10, font=("Monaco", 20), bg="#AAAAAA", fg="black", command=lambda: set_diff('Easy'))
easy_mode.place(x=145, y=200)

# normal mode button
normal_mode = tk.Button(options_frame, text="Normal", width=10, font=("Monaco", 20), bg="#AAAAAA", fg="black", command=lambda: set_diff('Normal'))
normal_mode.place(x=305, y=200)

# impossible mode button
impossible_mode = tk.Button(options_frame, text="Impossible", width=20, font=("Monaco", 20), bg="#AAAAAA", fg="red", command=lambda: set_diff('Impossible'))
impossible_mode.place(x=145, y=252)


# winner frame
winner_frame = tk.Frame(pong, width=600, height=450, bg="black")

# winner label
winner_label = tk.Label(winner_frame, text='', font=("Monaco", 30), bg="black", fg="white")
winner_label.pack(anchor='center', padx= 50, pady=50)

# start the game
pong.mainloop()