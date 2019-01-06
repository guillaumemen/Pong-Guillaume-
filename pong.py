import random
from tkinter import *


def move(direction):
    global player
    global canvas
    global PADDLE_MOVEMENT
    global HEIGHT

    coords = canvas.coords(player)

    if (direction == 'up' and coords[1] <= 10) or \
       (direction == 'down' and coords[3] >= HEIGHT):
       return False

    if direction == 'up':
        movement = -PADDLE_MOVEMENT
    else:
        movement = PADDLE_MOVEMENT

    canvas.move(player, 0, movement)

def move2(direction):
    global player2
    global canvas
    global PADDLE_MOVEMENT
    global HEIGHT

    coords = canvas.coords(player)

    if (direction == 'up' and coords[1] <= 10) or \
       (direction == 'down' and coords[3] >= HEIGHT):
       return False

    if direction == 'up':
        movement = -PADDLE_MOVEMENT
    else:
        movement = PADDLE_MOVEMENT

    canvas.move(player2, 0, movement)

def move_up(event):
    move('up')

def move_up2(event):
    move2('up')

def move_down(event):
    move('down')
    
def move_down2(event):
    move2('down')


def move_ball():
    global ball
    global canvas
    global dx
    global dy

    canvas.move(ball, dx, dy)

'''def move_computer():
    global computer
    global ball
    global canvas
    global HEIGHT
    global PADDLE_MOVEMENT

    ball_pos = canvas.coords(ball)
    comp_pos = canvas.coords(computer)

    if ball_pos[1] > comp_pos[1] and comp_pos[3] < HEIGHT:
        canvas.move(computer, 0, PADDLE_MOVEMENT)
    elif ball_pos[1] < comp_pos[1] and comp_pos[1] > 10:
        canvas.move(computer, 0, -PADDLE_MOVEMENT)
        '''

def show_scores():
    global canvas
    global player_score
    global player2_score
    global player_score_label
    global player2_score_label

    canvas.delete(player_score_label)
    canvas.delete(player2_score_label)

    player_score_label = canvas.create_text(190, 15, text=player2_score, fill='white', font=('Arial', 15))
    player2_score_label = canvas.create_text(210, 15, text=player_score, fill='white', font=('Arial', 15))


def bounce_ball():
    global dx
    global dy

    dx = -dx
    dy = random.randint(1, 3)
    flip_y = random.randint(0, 1) * 1

    if flip_y:
        dy = -dy


def reset_ball():
    global canvas
    global ball
    global dx
    global dy

    flip_x = random.randint(0, 1) * 1
    dx = random.randint(2, 3)
    dy = random.randint(1, 3)

    if flip_x == 1:
        dx = -dx

    canvas.delete(ball)
    ball = canvas.create_rectangle((190, 190, 210, 210), fill="white")


def refresh():
    """
    This is the method which updates all elements in the game.
    """
    global canvas
    global ball
    global player
    global player2
    global player_score
    global player2_score
    global WIDTH
    global HEIGHT
    global dx
    global dy
    global master
    global REFRESH_TIME

    show_scores()
    move_ball()
    ball_coords = canvas.coords(ball)

    if ball_coords[0] < 0:
        player_score = player_score + 1
        reset_ball()
    elif ball_coords[0] > WIDTH:
        player2_score = player2_score + 1
        reset_ball()

    if ball_coords[1] < 0 or ball_coords[3] > HEIGHT:
        dy = -dy

    overlapping = canvas.find_overlapping(*ball_coords)

    if len(overlapping) > 1:
        collided_item = overlapping[0]

        if collided_item == player or collided_item == player2:
            bounce_ball()

    master.after(REFRESH_TIME, refresh)




# Window dimensions and other constants
WIDTH = 400
HEIGHT = 400
PADDLE_MOVEMENT = 10
REFRESH_TIME = 20  # milliseconds

# Game variables
player_score = 0
player2_score = 0

# The Tk labels to show the score
player_score_label = None
player2_score_label = None

# Set up the GUI window via Tk
master = Tk()
master.title("Pong")

canvas = Canvas(master, background="black", width=WIDTH, height=HEIGHT)
canvas.create_line((200, 0, 200, 400), fill="red")

# Keep a reference for the GUI elements
player = canvas.create_rectangle((10, 150, 30, 250), fill="white")
player2 = canvas.create_rectangle((370, 150, 390, 250), fill="white")
ball = None  # Set this variable up for reset_ball()

# Ball acceleration (set in reset_ball())
dx = 0
dy = 0

canvas.pack()

# Bind the keyboard events to our functions
master.bind("w", move_up)
master.bind("s", move_down)
master.bind("<KeyPress-Up>", move_up2)
master.bind("<KeyPress-Down>", move_down2)


# Let's play!
reset_ball()
master.after(REFRESH_TIME, refresh)
master.mainloop()
