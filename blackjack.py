# _*_ coding: utf8 -*-
"""Blackjack console game - Written by Aaron Olson

   TODO: Soft Totals, add money & bets.  EVENTUALLY splits, double down
"""

from random import shuffle

class Deck:
    """ A deck of cards """

    def __init__(self):
        self.suites = ['\u2660', '\u2663', '\u2665', '\u2666']
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'K', 'Q', 'J', 'A']
        self.cards = []

    def gen_cards(self):
        """ Generate a deck of cards """
        for value in self.values:
            for suite in self.suites:
                self.cards.append(value + " of " + suite)

    def print_cards(self):
        """ Debug Function to print all cards """
        for card in self.cards:
            print(card, " ")


    def shuffle_cards(self):
        """ Shuffles the deck """
        shuffle(self.cards)

class Game:
    """ Game of (single deck) Blackjack and its members """
    def __init__(self):
        self.deck1 = Deck()
        self.deck1.gen_cards()
        self.deck1.shuffle_cards()

        self.p_cards = []
        self.d_cards = []


        self.p_total = [0, 0]
        self.d_total = [0, 0]

        self.p_bj = False
        self.p_money = 10000
        self.p_bet = 0
        self.p_can_double = True



        self.face_down = True
        self.cards_left = True
        self.hand_end = False

    def dealer_shuffle(self):
        """ Instantiate Deck, generate its cards, and shuffles """
        print("Shuffling Deck. . .")
        self.deck1 = Deck()
        self.deck1.gen_cards()
        self.deck1.shuffle_cards()


    def bet(self):
        """Input player's Wager, deduce from players total """
        print("Your cash: $" + str(self.p_money))
        self.p_bet = int(input("| Enter bet for this hand | : $"))
        self.p_money -= self.p_bet


    def deal(self):
        """ Dealing prodecure for each round of cards dealts """
        self.hand_end = False
        if len(self.deck1.cards) < 13: # cut card, 75% deck pen
            self.dealer_shuffle()


        self.p_cards.append(self.deck1.cards.pop())
        self.d_cards.append(self.deck1.cards.pop())
        self.p_cards.append(self.deck1.cards.pop())
        self.d_cards.append(self.deck1.cards.pop())
        self.set_totals(self.p_cards,self.p_total)
        self.set_totals(self.d_cards,self.d_total)
        self.print_visible_cards()

        if (self.p_total[0] == 21 and self.d_total[0] != 21):
            self.player_win()
            self.p_bj = True
        elif (self.d_total[0] == 21 and self.p_total[0] != 21):
            self.dealer_win()
            self.p_bj = False
        elif (self.d_total[0] == 21 and self.p_total[0] == 21):
            self.push()
            self.p_bj = False
        else:
            self.p_bj = False


    def print_visible_cards(self):
        """ Outputs cards for each step of round """
        print()
        print("Your cards:", end=' | ')
        for cards in self.p_cards:
            print(cards, end=' | ')
        print()
        print("Dealers Cards:", end=' | ')
        if self.face_down:
            print(self.d_cards[0] + " | xxxxxx", end = ' | ')
        else:
            for cards in self.d_cards:
                print(cards, end=' | ')
        print()

    def set_totals(self, hand, total):
        """ Setter Method for both dealer and player card totals """
        total[0] = 0
        total[1] = 0
        for card in hand:
            if card[0] in {'J', 'K', 'Q', '1'}:
                total[0] += 10
                total[1] += 10
            elif card[0] in 'A':
                total[0] += 11
                total[1] += 1
            else:
                total[0] += int(card[0])
                total[1] += int(card[0])

            if total[0] > 21 >= total[1]:
                total[0] = total[1]


    def end_hand(self):
        """ Reinitializes members after hand is over """
        self.face_down = True
        self.hand_end = True
        self.p_can_double = True
        self.p_cards = []
        self.d_cards = []
        self.p_total[0] = 0
        self.p_total[1] = 0
        self.d_total[0] = 0
        self.d_total[1] = 0
        self.p_bet = 0

    def player_hit(self):
        """ Player hits for a card """
        self.p_cards.append(self.deck1.cards.pop())
        self.set_totals(self.p_cards, self.p_total)

        if self.check_bust(self.p_total): #player busted, dealer won
            self.dealer_win()
        else:
            self.print_visible_cards()


    def player_stand(self):
        """ Player stands and keeps current total """
        self.face_down = False
        self.print_visible_cards()
        self.print_totals()
        self.set_totals(self.p_cards,self.p_total)

        #this is where the dealer plays out his hand
        while (self.d_total[0] < 17 and self.d_total[1] <= 17):
            self.d_cards.append(self.deck1.cards.pop())
            self.set_totals(self.d_cards,self.d_total)
            self.print_visible_cards()
            self.print_totals()
        if self.check_bust(self.d_total):
            self.player_win()
        else:
            self.check_winner()

    def print_totals(self):
        """Prints the totals of the player and dealer hand """
        print("Player Total: " + str(self.p_total[0]))
        if self.p_total[0] != self.p_total[1]:
            print("Player Soft Total: " + str(self.p_total[1]))
        if not self.face_down:
            print("Dealer Total: " + str(self.d_total[0]))
            if self.d_total[0] != self.d_total[1]:
                print("Dealer Soft Total: " + str(self.d_total[1]))

    def check_bust(self, total):
        """ Function returns True if the player has busted """
        busted = False

        if total[0] > 21 and total[1] > 21:
            busted = True

        return busted


    def check_winner(self):
        """ Determine the winner and call appropriate function for winner
            If the player busted during hitting, dealer_win is already called
            If the dealer busts during hitting, player_win is already called
        """
        if self.p_total[0] > self.d_total[0]: #players total is higher, player wins
            self.player_win()
        elif self.d_total[0] > self.p_total[0]: #dealers total is higher, dealer wins
            self.dealer_win()
        elif self.p_total[0] == self.d_total[0]: #totals equal, push
            self.push()
        else:
            print("This should not run, but just in case. . .")
            self.end_hand()

    def player_win(self):
        """ The player has won, pay player at 1 to 1 or blackjack odds
            Also returns the original wager deduces from player's money
        """
        print("============== YOU WIN ==============")
        if self.p_bj:
            self.p_money += 1.5 * self.p_bet
        else:
            self.p_money += self.p_bet * 2
        self.end_hand()

    #def double_hand(self):
    #    print('nothing happened.... to do')

    def dealer_win(self):
        """ The player has lost the hand, money is already deducted from total"""
        if self.face_down:
            self.face_down = False
            self.print_visible_cards()
            self.print_totals()
        print("============ DEALER WINS ============")
        self.end_hand()

    def push(self):
        """ The player and dealer have tied, return original wager to player """
        print("================ PUSH ===============")
        self.p_money += self.p_bet
        self.end_hand()


#Start Game
g = Game()
PLAYING = True

while PLAYING:
    if g.p_money > 0:

        g.bet()
        g.deal()
        while not g.hand_end:
            try:
                choice = int(input("| 1 to Hit | 2 to Stand | : "))
                if choice == 1:
                    g.player_hit()
                else:
                    g.player_stand()
            except ValueError:
                print("You did not enter a number; try again.")

        i = ""
        while not isinstance(i, int):
            try:
                i = int(input("| 1 to play again | : "))
            except ValueError:
                print("You did not enter a number; try again")

        if i != 1:
            PLAYING = False
    else: #ran out of money
        PLAYING = False



if g.p_money > 0:
    print("============= YOU LEFT WITH $" + str(g.p_money) + "! =============")
else:
    print("============= DOWN TO THE FELT! =============")
