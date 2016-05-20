#Mini Project 2 "Guess the Number"
#Player has to guess a secret number chosen by the computer
#Each time computer will tell the player whether the guess
#should be higher or lower, or correct
#Player has a limited number of guesses depending on the range
#Written by LC For Coursera course 
#Intro to Interactive Programming in Python

import simplegui
import math
import random

#global variables
secret_number = 0
guesses  = 0
game_id = 0

# helper function to start and restart the game
def new_game():
   
   #whoa! python isnt top down! too much C++ :D
    #initializes game in correct state( 0-100 or 0-1000)
    if game_id == 0:
        range100() 
    elif game_id == 1:
        range1000()
    else:
        range100()

# define event handlers for control panel
def range100():
    global secret_number, guesses, game_id
    
    secret_number = random.randrange(0,100)
    guesses = 7
    game_id = 0
    print "The number is now between 0 and 100."
    print "You have 7 guesses remaining.\n"
    
def range1000():
    global secret_number, guesses, game_id
    
    secret_number = random.randrange(0,1000)
    guesses = 10
    game_id = 1
    print "The number is now between 0 and 1000."
    print "You have 10 guesses remaining.\n"
    
def input_guess(guess):
    global guesses
    #convert input from string a number
    # a bit redundant, but for practice
    guess = float(guess)
    print "Your guess is", int(guess)
    #print "ig: secret_number is:", secret_number
    if guess > secret_number:
        print "Lower!"
               
    elif guess < secret_number:
        print "Higher!"
               
    elif guess == secret_number:
        print "Correct! You got it!\n"
        new_game()
        return
        
    else:
        print "Uh oh...I don't think you entered a number\n"
        
    guesses -= 1
    
    if guesses > 0:
        print "You have %d guesses remaining\n" %(guesses)
    
    if guesses == 0:
        print ("Ooooh, too bad! You've run out of guesses. "
        " The number was:"), secret_number , "\n"
        new_game()
    
# create frame
frame = simplegui.create_frame("Home", 300,300)

# register event handlers for control elements and start frame
frame.add_button("Range 0-100", range100)
frame.add_button("Range 0-1000", range1000)
frame.add_input("Enter your guess:", input_guess, 50)

frame.start()
# call new_game 
new_game()


