# Mini-project #6 - Blackjack
#Simple implementation of BlackJack
#Includes a betting system
#Written for Interactive Programming in Python Course on Coursera
#LC 3/2/2016

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
#tiled image
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")


CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':11, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# initialize some useful global variables
in_play = False
outcome = ""
pool = 500
bet = 0
bet_input = False
is_integer = False


# define card class
class Card:
    def __init__(self, rank, suit):
        if (rank in RANKS) and (suit in SUITS):
            self.rank = rank
            self.suit = suit
            
        else:
            self.rank = None
            self.suit = None
            
            print "Invalid card: ", rank, suit

    def __str__(self):
        return self.rank + "of" + self.suit

    def get_rank(self):
        return self.rank
    
    def get_suit(self):
        return self.suit

    

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0 # create Hand object

    def __str__(self):
        for i in self.cards:
            print i.rank + "of" + i.suit
        return ""
        # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)                              
        self.value += VALUES[card.get_rank()]
            
        
            # add a card object to a hand

    def get_value(self):
        a_num = 0
        if self.value > 21:
            for i in self.cards:
                if i.get_rank() == 'A':
                    a_num +=1
            
        return self.value - a_num * 10 
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust        
        #written like this to not change the value while getting the value
        
   
    def draw(self, canvas, pos):
        for i in self.cards:
            i.draw(canvas, pos)
            pos[0]+= CARD_SIZE[1] - 10
            
            # draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck=[Card(r,s) for r in RANKS for s in SUITS]
        pass	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
            # deal a card object from the deck
    
    def __str__(self):
        for i in self.deck:
            print i.get_rank() + "of" + i.get_suit()
        return ""
            # return a string representing the deck

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, pool,bet, bet_input, is_integer
    
    #implement hand and deck
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    deck.shuffle()

    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    #logic to continue game
    #required because pressing deal starts a new game
    if bet > pool:
        bet_input = False
        in_play = False
        label_bet.set_text("Error: bet is higher than pool")
    
    if not is_integer:
        bet_input = False
        in_play = False
        label_bet.set_text("Error: Please bet a postive integer")    
    
    if bet_input == True:
        pool -= bet
        label_pool.set_text("You have " + str(pool) + ".")
        label_bet.set_text("You bet " + str(bet) + ".")


        in_play = True
        outcome = "Hit or Stand?"
    elif bet > pool:
        label_bet.set_text("Error: bet is higher than pool")
        outcome = ""
    elif not is_integer:
        label_bet.set_text("Error: Please bet a postive integer")    
        outcome = ""
    else:
        label_bet.set_text("Enter a bet to start.")

        
def hit():
    global outcome, in_play, deck, player_hand, dealer_hand,bet,pool
    
    
    if in_play:
        player_hand.add_card(deck.deal_card())
   
        if player_hand.get_value() > 21:
            in_play = False
            outcome ="You have busted! Deal again?"
            
    
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, in_play, deck, player_hand, dealer_hand, pool,bet
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
              
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        if dealer_hand.get_value() > 21 or player_hand.get_value() > dealer_hand.get_value():
            outcome = "Player wins! Deal again?"
            in_play = False
            pool += bet*2
        else:
            outcome = "Dealer wins! Deal again?"
            in_play = False             
    
def input_handler(amount):
    #remember here amount is passed as a string
    global pool,bet, in_play, bet_input, is_integer
    try: #a check to make sure input is an integer
        bet = int(amount)
            
    except ValueError:
        label_bet.set_text("ValError: Please bet a postive integer")    
        is_integer = False
        inp.set_text("")
        
    else:
        is_integer = True
        bet = int(amount)
        if bet < 0:
            label_bet.set_text("Error: Please bet a postive integer")    
        if not in_play and bet > 0: #prevent betting while in play
            if bet > pool:
                label_bet.set_text("Error: bet is higher than pool")
            else:
                label_bet.set_text("You bet " + str(bet) + ".")

                label_pool.set_text("You have " + str(pool) + ".")
                bet_input = True
                is_integer = True
                deal()
 
def reset():
    global pool, bet, in_play, bet_input, outcome
    
    pool = 500
    bet = 0
    in_play = False
    bet_input = False
    is_integer = False
    outcome = ""
    label_pool.set_text("You have " + str(pool) + ".")
    label_bet.set_text("Enter a bet to start.")
    inp.set_text("")
    
# draw handler    
def draw(canvas):
    global player_hand, dealer_hand, outcome, in_play, bet_input
    

    if bet_input == True:
        dealer_hand.draw(canvas,[50,150])
        player_hand.draw(canvas, [50,350])
        canvas.draw_text("Value: "+str(dealer_hand.get_value()),(50,130),20,"White")         
        canvas.draw_text("Value: "+str(player_hand.get_value()),(500,580),20,"White") 
        
    if in_play:
        #coverup dealer value and dealer hole card
        canvas.draw_polygon([(105,110),(105,140),(150,140),(150,110)],1,"Green","Green")
        canvas.draw_image(card_back,CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [CARD_CENTER[0]+50,CARD_CENTER[1]+150], CARD_SIZE)
    
    canvas.draw_text("Blackjack", (50, 75), 60, "Navy", "monospace")
    blackjack_text_len = frame.get_canvas_textwidth("Blackjack", 60, "monospace")
    canvas.draw_line((50, 91), (50 + blackjack_text_len, 91), 5, "Black")     
    canvas.draw_text(outcome,(230,280),20,"White")    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_label("Dealer stands on Soft 17.",200)
frame.add_label("Dealer wins on Push.",200)
frame.add_label("Blackjack is treated as 21.",200)
label_pool = frame.add_label("You have " + str(pool) + ". Enter your bet:",200)
inp = frame.add_input("", input_handler, 40) #can't change label of input field so had to make an extra label

label_bet = frame.add_label("Enter a bet to start.",200)
frame.set_draw_handler(draw)
frame.add_button("Reset", reset,200)


# get things rolling

frame.start()


