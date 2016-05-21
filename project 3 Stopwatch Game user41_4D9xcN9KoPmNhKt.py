# Stopwatch:The Game, Mini-Project #3
# Displays a stopwatch in the format of MM:SS.T 
# where T is the tenths-of-a-second place
# Goal of the game is to stop the watch at a whole second
# i.e. when T = 0 ; score is kept track in the top right corner
# Written by LC for Coursera: Intro to Interactive
# Programming in Python, 6/20/2015


import simplegui

# define global variables
increment = 0
successes = 0
stops = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    # ive convoluted this actually because of how I handled the math below
    # (used increment *0.1 and int(t*10) )
    # running out of time to edit prior submit but it works the same
    t = int(t*10) 
   
    A =  t / 600 
    B =  t % 600 / 100
    C = (t % 600 - B*100 )/ 10
    D = t % 600 - B* 100 - C*10     
    # print str(A)+ ':' + str(B) + str(C) + '.' + str(D)
    return str(A)+ ':' + str(B) + str(C) + '.' + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    

def stop():
    
    global successes, stops
        
    if timer.is_running(): 
        # to prevent scores from incrementing if timer is already stopped
        timer.stop()
        stops +=1
        if increment % 10 == 0:
            successes += 1
        
def reset():
    
    global increment, successes, stops
    
    timer.stop()
    increment = 0
    successes = 0
    stops = 0
    
    

# define event handler for timer with 0.1 sec interval
def tick():
    global increment
    increment += 1
    

# define draw handler
def draw_handler(canvas):
    
    score = str(successes) + '/' + str(stops)
    # draws the stopwatch
    canvas.draw_text(format(increment*0.1), [105,110], 36, 'White')
    # draws the score
    canvas.draw_text(score, [250, 20], 20, 'Yellow')
    
    # for fun
    canvas.draw_text("Stopwatch: The Game!", [10, 20], 20, 'White')
    canvas.draw_text('See if you can stop the watch at a whole second', [12,195], 14, 'White')
    
# create frame
frame = simplegui.create_frame("Test", 300, 200)
timer = simplegui.create_timer(100, tick)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)

# register event handlers
frame.set_draw_handler(draw_handler)

# start frame
frame.start()

