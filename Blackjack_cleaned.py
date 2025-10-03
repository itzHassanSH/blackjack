values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

from random import shuffle
from repeat_function import repeat_game

class Card:
    global values
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def __str__(self):
        return "The deck has:\n" + "\n".join(str(card) for card in self.cards)

    def shuffle(self):
        shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == "Ace":
            self.aces += 1
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def hit(self, deck):
        card = deck.deal()
        self.add_card(card)


class Chips:
    def __init__(self):
        self.wallet = 1000
        self.bet = 0

    def win_bet(self):
        self.wallet += self.bet

    def lose_bet(self):
        self.wallet -= self.bet

    def take_bet(self):
        while True:
            try:
                bet = int(input("How many chips would you like to put forward? "))
                if bet > self.wallet:
                    print(f"Sorry your bet can't exceed your wallet: {self.wallet}")
                else:
                    self.bet = bet
                    break
            except ValueError:
                print("Sorry, the value must be an integer!")


class Player:
    def __init__(self):
        self.hand = Hand()
        self.chips = Chips()

class Dealer:
    def __init__(self):
        self.hand = Hand()


def show_some(player, dealer):
    print("\nDealer's Hand: ")
    print(" <hidden card> ")
    print(f"{dealer.hand.cards[1]}")
    print("\nPlayer's Hand: ", *player.hand.cards, sep='\n')
    print(f"Player's Total: {player.hand.value}")

def show_all(player, dealer):
    print("\nDealer's's Hand: ", *dealer.hand.cards, sep='\n')
    print(f"Dealer's Total: {dealer.hand.value}")
    print("\nPlayer's Hand: ", *player.hand.cards, sep='\n')
    print(f"Player's Total: {player.hand.value}")

def win(winner, loser):
    if isinstance(winner, Player):
        print("Player wins!")
        user.chips.win_bet()
    else:
        print("Dealer wins!")
        user.chips.lose_bet()

def bust(user):
    if isinstance(user, Player):
        print("Player busts!")
        user.chips.lose_bet()
    else:
        print("Dealer busts!")
        user.chips.win_bet()

def push():
    print("Dealer and Player tie! It's a push. ")

def check_initial_blackjack(player, dealer):
    if player.hand.value == 21 and dealer.hand.value == 21:
        show_all(player, dealer)
        print("Push! Both have Blackjack")
    elif player.hand.value == 21:
        show_all(player, dealer)
        print("Player wins with a Blackjack!")
        player.chips.win_bet()
    elif dealer.hand.value == 21:
        show_all(player, dealer)
        print("Dealer wins with a Blackjack!")
        player.chips.lose_bet()
    else:
        return False
    return True

def main():
    player = Player()
    dealer = Dealer()
    while True:
        print("Welcome to BlackJack! Get as close to 21 as you can without going over!")
        print("Dealer hits until he reaches 17. Aces count as 1 or 11")

        card_deck = Deck()
        card_deck.shuffle()

        player.hand.add_card(card_deck.deal())
        player.hand.add_card(card_deck.deal())
        dealer.hand.add_card(card_deck.deal())
        dealer.hand.add_card(card_deck.deal())

        player.chips.take_bet()

        show_some(player, dealer)

        # GAME STARTS
        game_on = True
        while game_on:
            # INITIAL BLACKJACK CHECK
            if check_initial_blackjack(player, dealer):
                break

            move = input("\nWould you like to Hit or Stand? ").upper()
            while move[0] not in ["H", "S"]:
                move = input("Please only select Hit or Stand").upper()

            if move[0] == "H":
                player.hand.hit(card_deck)
                show_some(player, dealer)
                if player.hand.value > 21:
                    bust(player)
                    break
                if player.hand.value == 21:
                    move = "S"
            if move[0] == "S":
                show_all(player, dealer)
                while dealer.hand.value < 17:
                    dealer.hand.hit(card_deck)
                    show_all(player, dealer)
                if dealer.hand.value > 21:
                    bust(dealer)
                elif player.hand.value > dealer.hand.value:
                    win(player)
                elif dealer.hand.value > player.hand.value:
                    win(dealer)
                else:
                    push()
                break

        print(f"\nPlayer's winning stand at: {player.chips.wallet}")

        if not repeat_game():
            print("Thank you for playing Blackjack. Hope you had a fun time!")
            break

        player.hand = Hand()
        dealer.hand = Hand()

if __name__ == "__main__":
    main()
