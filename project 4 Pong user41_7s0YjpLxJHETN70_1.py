# Pong, Mini-Project #4
# Implementation of the Classic Arcade Game Pong
# For 2 Players
# Written by LC for Coursera: Intro to Interactive
# Programming in Python, 3/25/2016

import simplegui
import random


# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    x = random.randrange(120,240)/60.0 # remember randrange 240 means 239 (and randrange has step extra param)
    y = random.randrange(60,180)/60.0 # div 60 because implicit timer is 1/60 second refreshrate
    
    if direction == "RIGHT":
        ball_vel = [x,-y]   # -1 because y axis goes from top to bottom
    elif direction == "LEFT":
        ball_vel=[-x,-y]
    else:
        ball_vel =[0,-1] # test case
        
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos = [0, HEIGHT/2]
    paddle2_pos = [WIDTH-PAD_WIDTH -1, HEIGHT/2]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    start_choice = random.choice(("LEFT", "RIGHT")) 
    # double parantheses because choice one argument, in this case a tuple

    spawn_ball(start_choice)

def restart():

    new_game()
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos = [x+y for x,y in zip(ball_pos, ball_vel)]  
    # zip pairs things into tuples. then they are in the form of (x,y).
    
    
    if ball_pos[1] <= BALL_RADIUS:    #REFLECTIONS from top and bottom of wall
        ball_vel[1] = -ball_vel[1]
    
    if ball_pos[1] >= (HEIGHT - 1 - BALL_RADIUS):
        ball_vel[1]= -ball_vel[1]
        
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red","White")
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    
    if paddle1_pos[1] <= 0 or paddle1_pos[1] >= (HEIGHT-1-PAD_HEIGHT):
        paddle1_pos[1] -=paddle1_vel
    
    if paddle2_pos[1] <= 0 or paddle2_pos[1] >= (HEIGHT-1-PAD_HEIGHT):
        paddle2_pos[1] -=paddle2_vel  #note cannot be elif else both happening might send paddle 2 off
        #need to check both
        
   
    
    # draw paddles
    paddle1 = [(paddle1_pos[0],paddle1_pos[1]), (paddle1_pos[0]+PAD_WIDTH, paddle1_pos[1]),
               (paddle1_pos[0]+PAD_WIDTH, paddle1_pos[1] +PAD_HEIGHT),
               (paddle1_pos[0], paddle1_pos[1]+PAD_HEIGHT)]
    
    paddle2 = [(paddle2_pos[0],paddle2_pos[1]), (paddle2_pos[0]+PAD_WIDTH, paddle2_pos[1]),
               (paddle2_pos[0]+PAD_WIDTH, paddle2_pos[1] +PAD_HEIGHT),
               (paddle2_pos[0], paddle2_pos[1]+PAD_HEIGHT)]
    
    canvas.draw_polygon(paddle1,1,"white", "white")
    canvas.draw_polygon(paddle2,1,"white", "white")
    # determine whether paddle and ball collide 
    
    
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos[1] and ball_pos[1] <= (paddle1_pos[1] +PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0]*1.10
        else:
            spawn_ball("RIGHT")
            score2 +=1
    elif ball_pos[0] >= (WIDTH - 1 - BALL_RADIUS - PAD_WIDTH):
        if ball_pos[1] >= paddle2_pos[1] and ball_pos[1] <= (paddle2_pos[1] +PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0]*1.10
        else:
            spawn_ball("LEFT")
            score1 +=1
    
    # draw scores
    canvas.draw_text(str(score1),(WIDTH/3.0, 40),40,"white")
    canvas.draw_text(str(score2),(2*WIDTH/3.0-15, 40),40,"white")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 4
    if key ==  simplegui.KEY_MAP["w"]:
        paddle1_vel = -acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = +acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = +acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key ==  simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart",restart)
frame.add_label("Player 1 use W and S")
frame.add_label("Player 2 use Up and Down")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)



# start frame
new_game()
frame.start()

