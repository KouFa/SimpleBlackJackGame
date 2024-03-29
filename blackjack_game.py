import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven",
         "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of "+self.suit


class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n"+card.__str__()
        return "The deck has: "+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


# TESTING THE DECK
#test_deck = Deck()
# test_deck.shuffle()
# print(test_deck)


class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# TESTING AGAIN
#test_deck = Deck()
# test_deck.shuffle()

# Player
#test_player = Hand()

# Deal one card from the deck
#pulled_card = test_deck.deal()
# print(pulled_card)
# test_player.add_card(pulled_card)
# print(test_player.value)


class Chips():
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:

        try:
            chips.bet = int(input('\nHow many chips would you like to bet? '))
        except:
            print('\nSorry please provide an integer.')
        else:
            if chips.bet > chips.total:
                print('\nSorry, you dont have enough chips! You have only: {}'.format(chips.total))
            else:
                break


def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input('\nHit or Stand? Enter "h" or "s" ')

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print('\nPlayer Stands. Dealers Turn')
            playing = False
        else:
            '\nPlease enter "h" or "s"'
            continue
        break


def show_some(player, dealer):
    print('\nDEALERS HAND:')
    print('<One card hidden!>')
    print(dealer.cards[1])
    print('\n')
    print('PLAYERS HAND:')
    for card in player.cards:
        print(card)


def show_all(player, dealer):
    print('\nDEALERS HAND:')
    for card in dealer.cards:
        print(card)
    print('\n')
    print('PLAYERS HAND:')
    for card in player.cards:
        print(card)


def player_busts(player, dealer, chips):
    print('BUST PLAYER!')
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print('PLAYER WINS!')
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print('DEALER BUSTED! PLAYER WINS!')
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print('BUST WINS!')
    chips.lose_bet()


def push(player, dealer):
    print('Dealer and Player tie! PUSH')


while True:
    # print an opening statement
    print('\nWELCOME TO BLACKJACK\n')

    # create and shuffle the deck, give two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # set up the players chips
    player_chips = Chips()

    # prompt the Player for their bet
    take_bet(player_chips)

    # show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:

        # prompt the Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # if player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)

            break

        # if Player hasn't busted, play Dealers hand until he exceeds Players hand
        if player_hand.value <= 21:
            while dealer_hand.value < player_hand.value:
                hit(deck, dealer_hand)

        # show all cards
        show_all(player_hand, dealer_hand)

        # run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

        # inform player for their total chips
        print('\n Player total chips are at: {}'.format(player_chips.total))

        # ask to play again
        new_game = input('\nWould u like to play again? Anwer "y" or "n" ')
        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            break
