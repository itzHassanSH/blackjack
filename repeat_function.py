def repeat_game():
    while True:
        repeat = input("Do you want to play again? Y/N\n").upper()
        if repeat in ["Y", "N"]:
            return repeat == "Y"
        print("Only reply with Y or N")