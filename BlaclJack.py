# http://www.codeskulptor.org/#user47_kwnrsjfLXw_0.py

# Mini-project #6 - Blackjack

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
prompt = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8',
         '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
          '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] \
                    * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] \
                    * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, \
                          [pos[0] + CARD_CENTER[0], pos[1] + \
                           CARD_CENTER[1]], CARD_SIZE)

    def draw_back(self, canvas, pos):
        card_loc = (CARD_CENTER[0],
                    CARD_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_SIZE, \
                          [pos[0] + CARD_CENTER[0], pos[1] + \
                           CARD_CENTER[1]], CARD_SIZE)

    # define hand class


class Hand:
    def __init__(self):
        self.hand_list = []

    def add_card(self, card):
        self.hand_list.append(card)

    def __str__(self):
        string = "Hand contains: "
        for i in range(len(self.hand_list)):
            string += str(self.hand_list[i]) + " "
        return string

    def get_value(self):
        self.hand_value = 0
        if self.hand_list == []:
            self.hand_value = 0
            return self.hand_value
        for v in self.hand_list:
            self.hand_value += VALUES[Card.get_rank(v)]
        for x in self.hand_list:
            if Card.get_rank(x) != "A":
                return self.hand_value
            else:
                if (self.hand_value + 10) <= 21:
                    return self.hand_value + 10
                else:
                    return self.hand_value

    def draw(self, canvas, pos):
        for c in self.hand_list:
            c.draw(canvas, pos)
            pos[0] += 50

    def draw_b(self, canvas, pos):
        self.hand_list[0].draw_back(canvas, pos)
        pos[0] += 50
        for c in self.hand_list:
            c.draw(canvas, pos)
            pos[0] += 0


# define deck class 
class Deck:

    def __init__(self):
        self.full_deck = []
        for s in SUITS:
            for r in RANKS:
                self.full_deck.append(Card(s, r))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.full_deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.full_deck.pop()

    def __str__(self):
        # return a string representing the deck
        deck_string = "Deck contains: "
        for i in range(len(self.full_deck)):
            deck_string += str(self.full_deck[i]) + " "
        return deck_string


# define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, \
        unbiased_deck, prompt, score
    if in_play == True:
        outcome = "Deal in play. Lose round."
        prompt = "Hit or Stand?"
        score -= 1
        return
    player_hand = Hand()
    dealer_hand = Hand()
    unbiased_deck = Deck()
    unbiased_deck.shuffle()
    player_hand.add_card(unbiased_deck.deal_card())
    dealer_hand.add_card(unbiased_deck.deal_card())
    player_hand.add_card(unbiased_deck.deal_card())
    dealer_hand.add_card(unbiased_deck.deal_card())
    in_play = True
    outcome = "Hit or Stand?"
    prompt = ""


def hit():
    global outcome, in_play, player_hand, dealer_hand, unbiased_deck, score, prompt
    if player_hand.get_value() <= 21:
        player_hand.add_card(unbiased_deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = ":( You have busted"
            prompt = "New Deal? Let's keep playing!"
            in_play = False
            score -= 1


def stand():
    global in_play, player_hand, dealer_hand, unbiased_deck, score, outcome, prompt
    if in_play == False:
        outcome = "You can't stand. You have busted. Sorry!"
        prompt = "Let's keep playing! New Deal?"
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(unbiased_deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer has busted! You win!"
            prompt = "New Deal?"
            score += 1
            in_play = False
        else:
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "Dealer wins!"
                prompt = "Let's have another go. New Deal?"
                score -= 1
                in_play = False
            else:
                outcome = "You have won. Congratulations!"
                prompt = "New Deal? "
                score += 1
                in_play = False


# draw handler    
def draw(canvas):
    global player_hand, outcome, score, prompt, in_play, dealer_hand
    player = player_hand
    dealer = dealer_hand
    player.draw(canvas, [300, 420])
    if in_play == True:
        dealer.draw_b(canvas, [300, 300])
    else:
        dealer.draw(canvas, [300, 300])
    canvas.draw_text('BlackJack', (200, 80), 42, 'White')
    canvas.draw_text("score (so far): " + str(score), (300, 260), 30, 'White')
    canvas.draw_text(outcome, (40, 160), 30, 'White')
    canvas.draw_text(prompt, (40, 200), 30, 'White')
    canvas.draw_text("your hand: ", (150, 500), 30, 'White')
    canvas.draw_text("dealers': ", (150, 390), 30, 'White')
    canvas.draw_text("Note. Cards left a bit overlapping intentionally. Not to overlap, \
tune pos to 72 in lines 97 and 101. Enjoy!", (10, 580), 13, 'White')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Grey")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric
