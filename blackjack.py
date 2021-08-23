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


        self.p_total = 0
        self.d_total = 0
        self.p_soft_total = 0
        self.d_soft_total = 0

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
        if len(self.deck1.cards) < 4:
            self.dealer_shuffle()


        self.p_cards.append(self.deck1.cards.pop())
        self.d_cards.append(self.deck1.cards.pop())
        self.p_cards.append(self.deck1.cards.pop())
        self.d_cards.append(self.deck1.cards.pop())
        self.set_totals()
        self.print_visible_cards()
        #self.print_totals()

        if (self.p_total == 21 and self.d_total != 21):
            self.player_win()
            self.p_bj = True
        elif (self.d_total == 21 and self.p_total != 21):
            self.dealer_win()
            self.p_bj = False
        elif (self.d_total == 21 and self.p_total == 21):
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

    def set_totals(self):
        """ Setter Method for both dealer and player card totals """
        self.p_total = 0
        self.d_total = 0
        self.p_soft_total = 0
        self.d_soft_total = 0

        for cards in self.p_cards:
            temp = 0
            temp2 = 0
            if cards[0] == 'K' or cards[0] == 'Q' or cards[0] == 'J' or len(cards) == 7:
                temp = 10
                temp2 = 10

            elif cards[0] == 'A':
                temp = 11
                temp2 = 1
            else:
                temp = int(cards[0])
                temp2 = int(cards[0])
            self.p_total += temp
            self.p_soft_total += temp2

            if self.p_total > 21 and self.p_soft_total <= 21:
                self.p_total = self.p_soft_total #is it needed?

        for cards in self.d_cards:
            temp = 0
            temp2 = 0
            if cards[0] == 'K' or cards[0] == 'Q' or cards[0] == 'J' or len(cards) == 7:
                temp = 10
                temp2 = 10

            elif cards[0] == 'A':
                temp = 11
                temp2 = 1
            else:
                temp = int(cards[0])
                temp2 = int(cards[0])
            self.d_total += temp
            self.d_soft_total += temp2


    def end_hand(self):
        """ Reinitializes members after hand is over """
        self.face_down = True
        self.hand_end = True
        self.p_can_double = True
        self.p_cards = []
        self.d_cards = []
        self.p_total = 0
        self.d_total = 0
        self.p_soft_total = 0
        self.d_soft_total = 0
        self.p_bet = 0

    def player_hit(self):
        """ Player hits for a card """
        if len(self.deck1.cards) == 0:
            self.dealer_shuffle()

        self.p_cards.append(self.deck1.cards.pop())
        self.set_totals()
        if self.check_bust() is True:
            self.dealer_win()
        else:
            self.print_visible_cards()
            #self.print_totals()


    def player_stand(self):
        """ Player stands and keeps current total """
        self.face_down = False
        self.check_bust_d()      # two or twelve for double Aces?
        self.print_visible_cards()
        self.print_totals()
        while (self.d_total < 17 and self.d_soft_total <= 17):
            if len(self.deck1.cards) == 0:
                self.dealer_shuffle()
            self.d_cards.append(self.deck1.cards.pop())
            self.set_totals()
            self.check_bust_d()
            self.print_visible_cards()
            self.print_totals()

        self.check_winner()

    def print_totals(self):
        """Prints the totals of the player and dealer hand """
        print("Player Total: " + str(self.p_total))
        if self.p_total != self.p_soft_total:
            print("Player Soft Total: " + str(self.p_soft_total))
        if self.face_down == False:
            print("Dealer Total: " + str(self.d_total))
            if self.d_total != self.d_soft_total:
                print("Dealer Soft Total: " + str(self.d_soft_total))

    def check_bust(self):
        """ Function returns True if the player has busted """
        player_busted = False

        if self.p_total > 21 and self.p_soft_total > 21:
            player_busted = True

        return player_busted

    def check_bust_d(self):
        """ Function returns True if the dealer has busted """
        dealer_busted = False

        if self.d_total > 21 and self.d_soft_total > 21:
            dealer_busted = True

        return dealer_busted



    def check_winner(self):
        """ Determine the winner and call appropriate function for winner """
        if (self.check_bust() is False and self.p_total > self.d_total):
            self.player_win()
        elif (self.check_bust_d() is False and self.d_total > self.p_total):
            self.dealer_win()
        elif (self.check_bust() is False and self.check_bust_d() == False and self.p_total == self.d_total):
            self.push()
        elif (self.check_bust() is False and self.check_bust_d() == True):
            self.player_win()
        elif (self.check_bust() is True and self.check_bust_d() == False):
            self.dealer_win()
        else:
            print("Winner undeterminable. . . .")
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
playing = True

while playing:
    if g.p_money > 0:

        g.bet()
        g.deal()
        while g.hand_end == False:
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
            playing = False
    else:
        playing = False



if g.p_money > 0:
    print("============= YOU LEFT WITH $" + str(g.p_money) + "! =============")
else:
    print("============= DOWN TO THE FELT! =============")
