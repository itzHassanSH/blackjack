# BlackJack
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

from random import shuffle
from colorama import Fore
from repeat_function import repeat_game

# Deck and Card classes remain same --> deck has deal, shuffle,
# User comes in, which can be a player or dealer. both have hit attribute, stand happens in logic,

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
        print(Fore.GREEN + f"{len(self.cards)} Cards:" + Fore.RESET)
        for _ in range(len(self.cards)):
            print(self.cards[_])
        return ""

    def shuffle(self):
        shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class User:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_cards(self, card):
        self.cards.append(card)

    def __str__(self):
        print(f"{self.name}: ", end="")
        for i in range(len(self.cards)-1):
            print(f"{self.cards[i].rank}", end=" and ")
        return f"{self.cards[-1].rank} -- {self.calculate_total()}"


    def calculate_total(self):
        total = 0
        ace_count = 0
        for i in range(len(self.cards)):
            total += self.cards[i].value
            if self.cards[i].rank == "Ace":
                ace_count += 1
        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1
        return total


card_deck = Deck()
card_deck.shuffle()

def main():
    global card_deck
    wallet = 0
    while True:
        print("Welcome to Blackjack")
        wallet += int(input("How much would you like to put forward? "))
        while wallet < 25:
            wallet = int(input("Must put forward minimum starting amount of 25: "))
        bet = int(input("Now place your bet -- 25, 50, 100, 500 "))
        while bet > wallet or bet not in [25, 50, 100, 500]:
            if bet > wallet:
                user_input = int(input("Insufficient funds. Place your bet -- 25, 50, 100, 500 \nTo add more funds, enter 0 \nTo withdraw and exit, enter -1\n"))
            else:
                user_input = int(input("Only these values are accepted -- 25, 50, 100, 500 \nTo add more funds, enter 0 \nTo withdraw and exit, enter -1\n"))

            if user_input == -1:
                print(f"You have successfully withdrawn {wallet}")
                exit()
            elif user_input == 0:
                wallet += user_input
                user_input = int(input("Accepted bet values: 25, 50, 100, 500 \nTo add more funds, enter 0 \nTo withdraw and exit, enter -1\n"))
                if user_input == -1:
                    print(f"You have successfully withdrawn {wallet}")
                    exit()
            elif user_input in [25, 50, 100, 500]:
                bet = user_input
        wallet -= bet

        computer = User("Computer")
        player_one = User("You")

        for x in range (2):
            computer.add_cards(card_deck.deal())
            player_one.add_cards(card_deck.deal())

        print(f"\nComputer: {computer.cards[1].rank} and ___ -- {computer.cards[1].value}")
        print(f"You: {player_one.cards[0].rank} and {player_one.cards[1].rank} -- {player_one.calculate_total()}")

        # GAME STARTS
        game_on = True
        while game_on:
            # INITIAL BLACKJACK CHECK
            if player_one.calculate_total() == 21 or computer.calculate_total() == 21:
                if player_one.calculate_total() > computer.calculate_total():
                    print(f"Blackjack! You take away {bet + bet * 3 / 2}")
                    wallet += bet + bet * 3 / 2
                elif player_one.calculate_total() < computer.calculate_total():
                    print(computer)
                    print(f"Blackjack! Dealer takes away {bet + bet * 3 / 2}")
                else:
                    print(computer)
                    print(f"Push! You take away {bet}")
                    wallet += bet
                break

            move = input("\nWould you like to Hit or Stand? ").upper()
            while move not in ["HIT", "STAND"]:
                move = input("Please only select Hit or Stand").upper()

            if move == "HIT":
                player_one.add_cards(card_deck.deal())
                print(f"{player_one}")
                if player_one.calculate_total() > 21:
                    print(f"\nYou Bust! Dealer takes {bet}")
                    break
                if player_one.calculate_total() == 21:
                    move = "STAND"
            if move == "STAND":
                print("")
                print(computer)
                while computer.calculate_total() < 17:
                    computer.add_cards(card_deck.deal())
                    print(computer)
                if computer.calculate_total() > 21:
                    print(f"\nDealer Busts! You take {bet*2}")
                    wallet += bet*2
                elif player_one.calculate_total() > computer.calculate_total():
                    print(f"\nYou win! You take {bet*2}")
                    wallet += bet * 2
                elif computer.calculate_total() > player_one.calculate_total():
                    print(f"\nYou lose! Dealer takes {bet*2}")
                else:
                    print(f"\nPush! You take away {bet}")
                    wallet += bet
                break

        print(f"\nYour wallet stands at {wallet}")
        if not repeat_game():
            print("Thank you for playing Blackjack. Hope you had a fun time!")
            break
        card_deck = Deck()
        card_deck.shuffle()



if __name__ == "__main__":
    main()


