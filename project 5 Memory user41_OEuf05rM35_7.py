# implementation of card game - Memory - Luke Chu 
#2/29/16

import simplegui
import random

# helper function to initialize globals
def new_game():
    global numbers, exposed, state, card1_ind,card2_ind, turns
    numbers = range(8) + range(8)
    random.shuffle(numbers)
    exposed = [False for i in range(16)]
    state = 0
    card1_ind = 0
    card2_ind = 0
    turns = 0
    label.set_text("Turns = 0")
    return
     
    
# define event handlers
def mouseclick(pos):
    global state, card1_ind, card2_ind, turns
    
    #calculate which card on a grid 
    i = pos[0]/50 + 4*(pos[1]/80)
     #again this works because function assumes exposed is global
    
    #state 0 is start of game. need for initial start
    if state == 0:
        if not exposed[i]:
            exposed[i] = True
            card1_ind = i   
            state = 1
            
    #one card has been flipped over        
    elif state == 1:
        if not exposed[i]:
            exposed[i] = True
            card2_ind = i
            state = 2
            
            
            turns +=1
            label.set_text("Turns = "+ str(turns))
    
    #two cards flipped
    elif state == 2:
        if(numbers[card1_ind] != numbers[card2_ind]):
            exposed[card1_ind] = False
            exposed[card2_ind] = False
            
        if not exposed[i]:
            exposed[i] = True
            card1_ind = i
            state = 1
            
        
        
                
# cards are 50x100 pixels in size, 4x4 grid    
def draw(canvas):
    
    #for spacing purposes
    y_space=0
    for i in range(4):
        x_space = 0
        y_space += 1
        
        for j in range(4):
            canvas.draw_text(str(numbers[4*i+j]),(x_space*50+10,y_space*80-20), 50, "white")
            
            x_space +=1         
    
    #could combine with drawing the numbers, but separated for clrity
    for i in range(4):
        for j in range(4):
                if(not exposed[4*i+j]):
                    canvas.draw_polygon([[50*j,80*i],[50*(j+1),80*i],[50*(j+1),80*(i+1)],[50*j,80*(i+1)]],3,"Black", "Blue")
   
                            
    


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 200, 320)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()