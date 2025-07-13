import tkinter as tk
import time

isRunning = False
gameStarted = False

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

# movement functions
def move_left_paddle_up(event):
    global gameStarted
    if gameStarted:
        if left_paddle.winfo_y() > 15:
            left_paddle.place_configure(y=left_paddle.winfo_y() - 15)

def move_right_paddle_up(event):
    global gameStarted
    if gameStarted:
        if right_paddle.winfo_y() > 15:
            right_paddle.place_configure(y=right_paddle.winfo_y() - 15)
    
def move_left_paddle_down(event):
    global gameStarted
    if gameStarted:
        if left_paddle.winfo_y() < 335:
            left_paddle.place_configure(y=left_paddle.winfo_y() + 15)   
    
def move_right_paddle_down(event):
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

# start frame
start_frame = tk.Frame(pong, width=600, height=450, bg="black")
start_frame.place(x=0, y=0)

# pong label
pong_label = tk.Label(start_frame, text="Pong", font=("Monaco", 50), bg="black", fg="white")
pong_label.place(x=210, y=50)

# play button
play_button = tk.Button(start_frame, text="Play", font=("Monaco", 20), bg="#AAAAAA", fg="black", command=lambda: start_game())
play_button.place(x=250, y=200)

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

# bind keys for paddle movement
pong.bind("<w>", move_left_paddle_up)  
pong.bind("<s>", move_left_paddle_down)
pong.bind("<Up>", move_right_paddle_up)
pong.bind("<Down>", move_right_paddle_down)

# start the game
pong.mainloop()