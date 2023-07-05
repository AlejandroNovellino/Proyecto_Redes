import sys
import argparse
import time

# Imports for serial
import serial
import json
import pickle

# Imports for dominoes
import dominoes

# possible strategies for each of the players
PLAYER_SETTINGS = [
    ("Human", None),
    ("AI: random", dominoes.players.random),
    ("AI: omniscient", dominoes.players.omniscient()),
]


def validated_input(prompt, validate_and_transform, error_message):
    """
    Convenience wrapper around `input` that prompts the user until valid
    input is provided. Strips leading and trailing spaces from the input
    before applying any further processing.

    :param str prompt: prompt for input displayed to the user
    :param function validate_and_transform: function that takes as input the
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    input provided by the user; returns
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    None if the input is invalid;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    otherwise, returns the input,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    potentially after applying some
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    processing to it
    :param str error_message: error message to display on invalid input
    :return: the user input, after `validate_and_transform` transforms it
    """
    while True:
        user_input = input(prompt).strip()
        validated_user_input = validate_and_transform(user_input)

        if validated_user_input is not None:
            return validated_user_input

        print(error_message)


def validate_and_transform_target_score(target_score):
    """
    To be used as a `validate_and_transform` function with `validated_input`.

    Requires that the input be a positive integer.

    :param str target_score: user input representing the target score
    :return: positive int representing the target score, if it is valid;
                                                                                                                                                                                                                                                                    None otherwise
    """
    try:
        target_score = int(target_score)
    except ValueError:
        return None

    if target_score <= 0:
        return None

    return target_score


def validate_and_transform_nonnegative_index(sequence):
    """
    Returns a function to be used as a `validate_and_transform`
    function with `validated_input`.
    """

    def _validate_and_transform_nonnegative_index(i):
        """
        To be used as a `validate_and_transform` function with `validated_input`.

        Requires that the input be a valid nonnegative index into `sequence`.

        :param str i: user input representing an index into `sequence`
        :return: the index as an integer, if it is valid; None otherwise
        """
        if i not in (str(j) for j in range(len(sequence))):
            return None

        return int(i)

    return _validate_and_transform_nonnegative_index


def validate_and_transform_end(end):
    """
    To be used as a `validate_and_transform` function with `validated_input`.

    Requires that the input be a valid end of the domino board - i.e. 'l' or 'r'.

    :param str end: user input representing an end of the domino board
    :return: True for the left end, False for the right end, None for invalid input
    """
    end = end.lower()
    try:
        return {"l": True, "r": False}[end]
    except KeyError:
        return None


# Args setup
argParser = argparse.ArgumentParser()
argParser.add_argument(
    "-pn", "--player_number", type=int, help="Player number to play in this instance"
)

# Get the player number
args = argParser.parse_args()
player_number = args.player_number

# Ports to be used
# Port to communicate between tow computers
port_COM = None  # Port to communicate
# Initialize the ports and the io wrappers
if player_number == 0:
    # Player is number 1
    port_COM = serial.Serial(port="COM1", timeout=3, write_timeout=3)
elif player_number == 1:
    # Player is number 2
    port_COM = serial.Serial(port="COM2", timeout=3, write_timeout=3)
elif player_number == 2:
    # Player is number 2
    port_COM = serial.Serial(port="COM1", timeout=3, write_timeout=3)
elif player_number == 3:
    # Player is number 2
    port_COM = serial.Serial(port="COM2", timeout=3, write_timeout=3)

print("----------------------------------Init----------------------------------")
print("Informacion de instancia:")
print(f"     - Numero del jugador: {player_number}")
print(f"     - Puerto a utilizar: {port_COM.port} \n")

# Game logic
# -------------------------------------------------------------------------------

# Variables
game = None  # Game to be played

# Set the game
if player_number == 0:
    # Player 1 so the game is created be him
    game = dominoes.Game.new(starting_player=0)
    # Write the game to the port
    port_COM.write(pickle.dumps(game))
elif player_number == 1:
    # Player 2 so the game comes from player 1
    game = pickle.loads(port_COM.readline())
elif player_number == 2:
    # Player 3 so the game comes from player 1
    game = pickle.loads(port_COM.readline())
elif player_number == 3:
    # Player 4 so the game comes from player 1
    game = pickle.loads(port_COM.readline())

"""# start a series up to `target_score`
series = dominoes.Series(target_score=100)
game = series.games[0]"""
"""
# print out the possible player settings
print("Player settings:")
for i, (name, _) in enumerate(PLAYER_SETTINGS):
	print("{}) {}".format(i, name))"""

"""# ask the user(s) to select a setting for each player
player_settings = []
valid_inputs = list(range(len(PLAYER_SETTINGS)))
for player in range(len(game.hands)):
	player_settings.append(
		PLAYER_SETTINGS[
			validated_input(
				"Select a setting for player {}: ".format(player),
				validate_and_transform_nonnegative_index(PLAYER_SETTINGS),
				"Please enter a value in: {}".format(valid_inputs),
			)
		]
	)"""


input("Press enter to begin game.")

# game.result will be filled in once the game ends
while game.result is None:
    # Verify is the player turn to play
    if game.turn != player_number:
        # Verify if it is AI turns
        if player_number == 1 and (game.turn == 2 or game.turn == 3):
            # If game turn is 2 AI 2 plays
            if game.turn == 2:
                # Make the AI 2 play
                print("---------------------------------------------------------------")
                print("- AI player making a move:")
                # Random AI player selecting a move
                dominoes.players.random(game)
                print(
                    "Player {} ({}) chose to play {} on the {} end of the board.".format(
                        game.turn,
                        f"AI-{game.turn}",
                        game.valid_moves[0][0],
                        "left" if game.valid_moves[0][1] else "right",
                    )
                )
                # make the selected move
                game.make_move(*game.valid_moves[0])
            # If game turn is 3 AI 3 plays
            if game.turn == 3:
                # Make the AI 3 play
                print("---------------------------------------------------------------")
                print("- AI player making a move:")
                # Random AI player selecting a move
                dominoes.players.random(game)
                print(
                    "Player {} ({}) chose to play {} on the {} end of the board.".format(
                        game.turn,
                        f"AI-{game.turn}",
                        game.valid_moves[0][0],
                        "left" if game.valid_moves[0][1] else "right",
                    )
                )
                # make the selected move
                game.make_move(*game.valid_moves[0])

            # Write the new state of the game to the port
            print("---------------------------------------------------------------")
            print("Resultados de las AI")
            print(f"	Turno: {game.turn}")
            print(f"	Board: {game.board}")
            port_COM.write(pickle.dumps(game))
            time.sleep(4)
            continue

        # Do nothing
        # Read the serial port if something have being written
        if port_COM.in_waiting:
            # Update the game with the one that comes from the port
            print("---------------------------------------------------------------")
            print("Leyendo del puerto")
            game = pickle.loads(port_COM.readline())
            print("Resultados de las lectura")
            print(f"	Turno: {game.turn}")
            print(f"	Board: {game.board}")
        continue

    # If we get to this point is the player turn
    # print the game state so that all players can see it
    print("---------------------------------------------------------------")
    print("Board:")
    print(game.board)
    for player, hand in enumerate(game.hands):
        print("Player {} has {} dominoes in his/her hand.".format(player, len(hand)))

        # clear the terminal upon starting a new turn
    input("It is now player {}'s turn. Press enter" " to continue.".format(game.turn))

    # print the board so that the player can decide what to play
    print("Board:")
    print(game.board)

    # remember whose turn it currently is.
    # we'll need it after we move on to the next player.
    turn = game.turn

    # player's hand in multiple-choice format.
    print("Player {}'s hand:".format(game.turn))
    hand = game.hands[game.turn]
    for i, d in enumerate(hand):
        print("{}) {}".format(i, d))

        # ask what move they'd like to play,
        # until they select a valid move.
    while True:
        valid_inputs = list(range(len(hand)))
        d = hand[
            validated_input(
                "Choose which domino you would like to play: ",
                validate_and_transform_nonnegative_index(hand),
                "Please enter a value in: {}".format(valid_inputs),
            )
        ]

        if game.board:
            end = validated_input(
                "Choose what end of the board you" " would like to play on (l or r): ",
                validate_and_transform_end,
                "Please enter a value in: [l, r]",
            )
        else:
            # if the board is empty, default to playing on the 'left'
            end = True

        try:
            game.make_move(d, end)
            break
        except dominoes.EndsMismatchException:
            # `game.make_move` is transactional - if it fails, the game
            # state is exactly as it was when the operation started
            print(
                "The selected domino cannot be played on the"
                " selected end of the board. Please try again."
            )
            # clear the terminal upon moving to the next
            # turn - no looking at the previous player's hand!
    input("Press enter to end player {}'s turn.".format(turn))
    port_COM.write(pickle.dumps(game))
    time.sleep(4)

# Game over
print("---------------------------------------------------------------")
print("Game over!")
print(game.result)
print(game)


# Close the ports
try:
    port_COM.close()
    print("Puertos cerrados")
except:
    print("Los puertos no pudieron ser cerrados")
print("----------------------------------End----------------------------------")
