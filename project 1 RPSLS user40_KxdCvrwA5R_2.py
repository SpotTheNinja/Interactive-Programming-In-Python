#Code by Luke Chu. 5/30/2015 
#Mini-Project 1
#Runs Rock-Paper-Scissors-Lizard-Spock against a computer.
#Written for Courera Intro to Programming in Python 



import random

def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        print (" Error, you chose a wrong hand signal! "
        "Please start over.")
        return 5 
        
        

def number_to_name(number):
    if number == 0 :
        return 'rock'
    elif number == 1 :
        return 'Spock'
    elif number == 2 :
        return 'paper'
    elif number == 3 :
        return 'lizard'
    elif number == 4 :
        return 'scissors'
    else:
        print "number not found!"
        return 'ERROR'
    
    
def rpsls(player_choice):
    player_number = name_to_number(player_choice)
    if player_number == 5:
        return
    
    print "You chose %s!" % player_choice
    
    comp_number = random.randrange(0,5,1)
    #interesting function, inclusive then exclusive
    
    comp_choice = number_to_name(comp_number)
    
    print "The computer chooses %s!" % comp_choice
    num_result = (player_number - comp_number) % 5
    #RPSLS follows easy cases of modular arithmetic
    #see below

    if num_result == 0:
        print ("%s and %s are the same. " 
        "\nTie!\n") %(player_choice, comp_choice)
    elif num_result == 1 or num_result == 2:
        print ("%s beats %s. \nPlayer " 
        "wins!\n") %(player_choice, comp_choice)
    elif num_result == 3 or num_result == 4:
        print ("%s beats %s. \nComputer "
        "wins!\n") %(comp_choice, player_choice)
    else:
        print """Hmmm, something seems have to gone awry.
        Please try again.\n"""
    return

rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
        
    
 
    