from email import message_from_string

from flask import Flask, request, render_template, session, jsonify, redirect, url_for
from markupsafe import escape
import Blackjackgame as Game

app = Flask(__name__)
app.secret_key = "some_random_key"

@app.route('/')
def home():
    phase = session.get("phase", "deal")
    return render_template("home.html", phase=phase)

# Query Parameters:
# Purpose: carry extra information about how you want to interact with the resource, usually optional or temporary.
# Examples:
#   Search terms (query=blackjack)
#   Filters (category=books, sort=price_asc)
#   Pagination (page=2)
#   Temporary flags (dark_mode=true)
# Rule of thumb: Use query parameters for transient, user-supplied, or optional info that modifies how the page is displayed.

@app.route('/game')
def game():
    phase = session.get("phase", "deal")
    wallet = session.get("wallet", 1000)
    bet = session.get("bet", 0)
    # if 'phase' not in session:
    #     session['wallet'] = 1000
    #     session['bet'] = 0
    #     session['phase'] = "deal"
    #     session["player"] = []
    #     session["dealer"] = []
    # wallet = session['wallet']
    # bet = session["bet"]
    # phase = session["phase"]
    # player = session["player"]
    # dealer = session["dealer"]
    return render_template("game.html", wallet=wallet, bet=bet, phase=phase)

# @app.route('/welcome')
# def welcome():
#     name = request.args.get("name", "Player")  # request.form.get("name") for POST aka sensitive information
#     session["name"] = name
#     return render_template("welcome.html", name=escape(name))


@app.route('/hit', methods=["POST"])
def hit():
    player = Game.Player.from_dict(session["player"])
    print(player)
    player.hand.recalc_value()
    deck = Game.Deck.from_dict(session["deck"])
    player.hand.hit(deck)
    session["player"] = player.to_dict()
    session["deck"] = deck.to_dict()
    return jsonify({
        "phase": "in_game",
        "player_cards": [str(player.hand.cards[-1])]
    })



@app.route('/place_bet', methods=["POST"])
def place_bet():
    data = request.get_json()
    bet = int(data["bet"])

    wallet = session.get('wallet', 1000)
    if bet > wallet:
        message = "Not enough chips!"
    else:
        wallet -= bet
        session['wallet'] = wallet
        session['bet'] += bet
        message = f"You bet {bet} chips."

    return jsonify({
        "message":  message,
        "wallet": wallet,
        "bet": session['bet'],
    })


@app.route('/reset_wallet', methods=["POST"])
def reset_wallet():
    session.clear()
    session["wallet"] = 1000
    session['bet'] = 0
    session["phase"] = "deal"
    session["player"] = []
    session["dealer"] = []
    return jsonify({
        "message": "Session cleared",
        "wallet": 1000,
        "bet": 0,
        "phase": 'deal'
    })

@app.route('/clear_bet', methods=["POST"])
def clear_bet():
    if session["bet"] == 0:
        return jsonify({
            "message": "You haven't placed a bet yet!",
        })
    session["wallet"] += session["bet"]
    session["bet"] = 0
    return jsonify({
        "message": "Bet cleared",
        "wallet": session["wallet"],
        "bet": 0
    })


@app.route('/deal', methods=["POST"])
def deal():
    player, dealer, card_deck = Game.initialize()
    session["phase"] = "in_game"
    session["deck"] = card_deck.to_dict()
    session["player"] = player.to_dict()
    session["dealer"] = dealer.to_dict()
    session["player_cards"] = [str(c) for c in player.hand.cards]
    session["dealer_cards"] = [str(c) for c in dealer.hand.cards]
    return jsonify({
        "phase": "in_game",
        "player_cards": [str(player.hand.cards[0]), str(player.hand.cards[1])],
        "dealer_cards": [str(dealer.hand.cards[0]), str(dealer.hand.cards[1])]
    })

@app.route('/resume', methods=["POST"])
def resume():
    return jsonify({
        "phase": "in_game",
        "player_cards": session["player_cards"],
        "dealer_cards": session["dealer_cards"]
    })

if __name__ == '__main__':
    app.run(debug=True)