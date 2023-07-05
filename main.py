import sys
import argparse

# Imports for serial
import serial
import json
import io
import time

# Imports for dominoes
import dominoes

# Args setup
argParser = argparse.ArgumentParser()
argParser.add_argument(
    "-pn", "--player_number", type=int, help="Player number to play in this instance"
)


def main():
    """
    Main function for the game

    Here the ports are established and selected

    Parameters:
    -----------
    player_number: integer
        For establishing in what port the player is going to read and write, can be 1 or 2
    """

    # Get the player number
    args = argParser.parse_args()
    player_number = args.player_number

    # Ports to be used
    # Port to communicate between tow computers
    port_COM = None  # Port to communicate
    # Initialize the ports and the io wrappers
    if player_number == 1:
        # Player is number 1
        port_COM = serial.Serial(port="COM1", timeout=0)

    elif player_number == 2:
        # Player is number 2
        port_COM = serial.Serial(port="COM2", timeout=0)

    print("----------------------------------Init----------------------------------")
    print("Informacion de instancia:")
    print(f"     - Numero del jugador: {player_number}")
    print(f"     - Puerto a utilizar: {port_COM.port}")

    # Game logic
    # ------------------------------------------------------------------

    # Variables
    game = None  # Game to be played

    # Set the game
    if player_number == 1:
        # Player 1 so the game is created be him
        game = dominoes.Game.new(starting_player=0)
        # Write the game to the output port
        port_COM.write(json.dumps(game.__dict__).encode("utf-8"))
    else:
        # Player 2 so the game comes from player 1
        game = dominoes.game.Game(*json.load(port_COM.readline().decode("utf-8")))

    # Game
    while not game.result:
        # Verify that is the player turn
        if game.turn == player_number - 1:
            # Player can play
            print(" Mesa de juego:")
            print(game.board)

            print(" Mano del jugador:")
            print(game.hands[game.turn])

            print(" Posibles jugadas:")
            print(game.valid_moves)

            # Player select the play to make
            player_play = input(
                "Seleccione la jugada que desea realizar (comienza desde 0)"
            )
            # The play is made
            game.make_move(*game.valid_moves[player_play])

            # Now the AI player make the play
            dominoes.players.random(game)
            if len(game.valid_moves):
                game.make_move(*game.valid_moves[0])
            else:
                game.make_move(*game.valid_moves[0])

            # Write the new game state to the output port
            port_COM.write(json.dumps(game.__dict__).encode("utf-8"))

        # Verify if the port have information to update the state of the game
        if port_COM.in_waiting():
            # Update the game by the state in the port B
            game = dominoes.game.Game(*json.load(port_COM.readline().decode("utf-8")))

    # Game finished print the result
    print(game.result)
    # ------------------------------------------------------------------

    # Close the ports
    try:
        port_COM.close()
        port_COM.close()
        print("Puertos cerrados")
    except:
        print("Los puertos no pudieron ser cerrados")
    print("----------------------------------End----------------------------------")


# Execute main
main()
