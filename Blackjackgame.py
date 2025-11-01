values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'jack':10,
         'queen':10, 'king':10, 'ace':11}
suits = ('hearts', 'diamonds', 'spades', 'clubs')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace')
wallet = 1000

from random import shuffle

class Card:
    global values
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank}_of_{self.suit}"

    def to_dict(self):
        return {"suit": self.suit, "rank": self.rank}
    @classmethod
    def from_dict(cls, data):
        return cls(data["suit"], data["rank"])


class Deck:
    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def __str__(self):
        return "The deck has:\n" + "\n".join(str(card) for card in self.cards)


    def to_dict(self):
        return {"cards": [card.to_dict() for card in self.cards]}
    @classmethod
    def from_dict(cls, data):
        deck = cls.__new__(cls)  # create deck without calling __init__
        deck.cards = [Card.from_dict(c) for c in data["cards"]]
        return deck


    def shuffle(self):
        shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0


    def to_dict(self):
        return {"cards": [card.to_dict() for card in self.cards]}
    @classmethod
    def from_dict(cls, data):
        hand = cls()
        hand.cards = [Card.from_dict(c) for c in data["cards"]]
        return hand
    def recalc_value(self):
        self.value = sum(card.value for card in self.cards)
        self.aces = sum(1 for card in self.cards if card.rank == "ace")
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == "ace":
            self.aces += 1
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def hit(self, deck):
        card = deck.deal()
        self.add_card(card)


# class Chips:
#     def __init__(self):
#         self.wallet = 1000
#         self.bet = 0
#
#     def win_bet(self, blackjack=False):
#         if blackjack:
#             self.wallet += self.bet*1.5
#         else:
#             self.wallet += self.bet
#
#     def lose_bet(self):
#         self.wallet -= self.bet




class Player:
    def __init__(self):
        self.hand = Hand()
        # self.chips = Chips()

    def to_dict(self):
        return {"hand": self.hand.to_dict()}

    @classmethod
    def from_dict(cls, data):  # Python passes the class Player as cls
        player = cls()  # Same as player = Player()
        player.hand = Hand.from_dict(data["hand"])
        return player




class Dealer:
    def __init__(self):
        self.hand = Hand()

    def to_dict(self):
        return {"hand": self.hand.to_dict()}

    @classmethod
    def from_dict(cls, data):  # Python passes the class Player as cls
        player = cls()  # Same as player = Player()
        player.hand = Hand.from_dict(data["hand"])
        return player



# def show_some(player, dealer):
#     print("\nDealer's Hand: ")
#     print(" <hidden card> ")
#     print(f"{dealer.hand.cards[1]}")
#     print("\nPlayer's Hand: ", *player.hand.cards, sep='\n')
#     print(f"Player's Total: {player.hand.value}")
#
# def show_all(player, dealer):
#     print("\nDealer's's Hand: ", *dealer.hand.cards, sep='\n')
#     print(f"Dealer's Total: {dealer.hand.value}")
#     print("\nPlayer's Hand: ", *player.hand.cards, sep='\n')
#     print(f"Player's Total: {player.hand.value}")

# def win(winner, loser, blackjack=False):
#     if isinstance(winner, Player):
#         print("Player wins!")
#         winner.chips.win_bet(blackjack)
#     else:
#         print("Dealer wins!")
#         loser.chips.lose_bet()
#
# def bust(winner, loser, blackjack=False):
#     if isinstance(loser, Player):
#         print("Player busts!")
#         loser.chips.lose_bet()
#     else:
#         print("Dealer busts!")
#         winner.chips.win_bet(blackjack)
#
# def push():
#     print("Dealer and Player tie! It's a push. ")

# def check_initial_blackjack(player, dealer):
#     if player.hand.value == 21 and dealer.hand.value == 21:
#         # show_all(player, dealer)
#         print("Push! Both have Blackjack")
#     elif player.hand.value == 21:
#         # show_all(player, dealer)
#         print("Player wins with a Blackjack!")
#         player.chips.win_bet(True)
#     elif dealer.hand.value == 21:
#         # show_all(player, dealer)
#         print("Dealer wins with a Blackjack!")
#         player.chips.lose_bet()
#     else:
#         return False
#     return True

def initialize():
    player = Player()
    dealer = Dealer()

    card_deck = Deck()
    card_deck.shuffle()

    player.hand.add_card(card_deck.deal())
    player.hand.add_card(card_deck.deal())
    dealer.hand.add_card(card_deck.deal())
    dealer.hand.add_card(card_deck.deal())

    return player, dealer, card_deck