import turtle
import time
import random
from collections import deque

delay = 0.1

# Score
score = 0
high_score = 0
tail_length = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("light blue")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Register the apple image
apple_image = "apple.gif"  # Make sure this file is in the same directory as your script
wn.register_shape(apple_image)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("indigo")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape(apple_image)
food.penup()
food.goto(0, 100)

segments = []

# Pen for score
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("dark blue")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Pen for menu
menu_pen = turtle.Turtle()
menu_pen.speed(0)
menu_pen.shape("square")
menu_pen.color("dark blue")
menu_pen.penup()
menu_pen.hideturtle()
menu_pen.goto(0, 0)

# Functions to control the snake
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def show_menu():
    menu_pen.clear()
    menu_pen.write("Welcome to Snake Game\nPress 'Space' to Start\nPress 'I' for AI Mode", align="center", font=("Courier", 24, "normal"))
    global running
    global ai_mode
    running = False
    ai_mode = False

def start_game():
    global running
    global ai_mode
    running = True
    ai_mode = False
    menu_pen.clear()
    reset_game()

def start_ai_mode():
    global running
    global ai_mode
    running = True
    ai_mode = True
    menu_pen.clear()
    reset_game()

def reset_game():
    global score, tail_length, delay
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    score = 0
    tail_length = 0
    delay = 0.1
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

# Simple AI movement with lookahead
def ai_move():
    directions = ['up', 'down', 'left', 'right']
    moves = {
        'up': (0, 20),
        'down': (0, -20),
        'left': (-20, 0),
        'right': (20, 0)
    }
    
    best_direction = None
    min_distance = float('inf')
    
    for direction in directions:
        dx, dy = moves[direction]
        new_x = head.xcor() + dx
        new_y = head.ycor() + dy
        
        # Check if new position is a collision with the border
        if new_x > 290 or new_x < -290 or new_y > 290 or new_y < -290:
            continue
        
        # Check if new position is a collision with itself
        collision = False
        for segment in segments:
            if segment.distance(new_x, new_y) < 20:
                collision = True
                break
        if collision:
            continue
        
        # Calculate the distance to the food
        distance = abs(new_x - food.xcor()) + abs(new_y - food.ycor())
        if distance < min_distance:
            min_distance = distance
            best_direction = direction
    
    if best_direction:
        head.direction = best_direction

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(start_game, "space")
wn.onkeypress(start_ai_mode, "i")

# Main game loop
running = False
ai_mode = False
show_menu()

try:
    while True:
        if running:
            wn.update()

            # AI mode logic
            if ai_mode:
                ai_move()

            # Check for a collision with the border
            if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
                time.sleep(1)
                show_menu()

            # Check for a collision with the food
            if head.distance(food) < 20:
                # Move the food to a random spot
                x = random.randint(-290, 290)
                y = random.randint(-290, 290)
                food.goto(x, y)

                # Add a segment
                new_segment = turtle.Turtle()
                new_segment.speed(0)
                new_segment.shape("square")
                if tail_length == 0:
                    new_segment.color("#663399")
                else:
                    new_segment.color("#9370DB")
                new_segment.penup()
                segments.append(new_segment)
                tail_length += 1

                # Shorten the delay
                delay = max(0.01, delay - 0.001)

                # Increase the score
                score += 10

                if score > high_score:
                    high_score = score

                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

            # Move the end segments first in reverse order
            for index in range(len(segments) - 1, 0, -1):
                x = segments[index - 1].xcor()
                y = segments[index - 1].ycor()
                segments[index].goto(x, y)

            # Move segment 0 to where the head is
            if len(segments) > 0:
                x = head.xcor()
                y = head.ycor()
                segments[0].goto(x, y)

            move()

            # Check for head collision with the body segments
            for segment in segments:
                if segment.distance(head) < 20:
                    time.sleep(1)
                    show_menu()

            time.sleep(delay)
        else:
            wn.update()
except turtle.Terminator:
    print("Game closed.")
