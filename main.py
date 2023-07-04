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

    print("----------------------------------Init----------------------------------")
    # Ports to be used
    # Port to communicate between tow computers
    port_COM_A = None  # Port to write
    port_COM_B = None  # Port to read
    # Initialize the ports and the io wrappers
    if player_number == 1:
        # Player is number 1
        # Port A to write
        port_COM_A = serial.Serial(port="COM1", timeout=0)
        # Port B to read
        port_COM_B = serial.Serial(port="COM2", timeout=0)

    elif player_number == 2:
        # Player is number 2
        # Port A to write
        port_COM_A = serial.Serial(port="COM2", timeout=0)
        # Port B to read
        port_COM_B = serial.Serial(port="COM1", timeout=0)

    # Test the ports

    # Write to the port
    test_dict = {"info": "Test information", "player": "Hello"}
    print(f"Valor del diccionario: {json.dumps(test_dict)}")

    # THIS IS HOW WE ARE WORKING
    # port_COM_A.write(json.dumps(test_dict).encode("ascii"))
    port_COM_A.write("Hola desde el puerto A".encode("utf-8"))
    message = port_COM_B.readline()
    print(f"Mensaje leido en el puerto B: {message.decode('utf-8')}")

    port_COM_B.write("Hola desde el puerto B".encode("utf-8"))
    message = port_COM_A.readline()
    print(f"Mensaje leido en el puerto A: {message.decode('utf-8')}")

    # Game logic
    # ------------------------------------------------------------------

    # Variables
    domino = None
    game = None

    # Set the game
    if player_number == 1:
        # Player 1 so the game is created be him
        domino = dominoes.Domino(6, 6)
        game = dominoes.Game.new(starting_domino=domino)
        # Write the game to the output port
        port_COM_A.write(json.dumps(game).encode("utf-8"))
    else:
        # Player 2 so the game comes from player 1
        game = json.load(port_COM_B.readline().decode("utf-8"))

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
            port_COM_A.write(json.dumps(game).encode("utf-8"))

        # Verify if the port have information to update the state of the game
        if port_COM_B.in_waiting():
            # Update the game by the state in the port B
            game = json.load(port_COM_B.readline().decode("utf-8"))

    # Game finished print the result
    print(game.result)
    # ------------------------------------------------------------------

    # Close the ports
    try:
        port_COM_A.close()
        port_COM_B.close()
        print("Puertos cerrados")
    except:
        print("Los puertos no pudieron ser cerrados")
    print("----------------------------------End----------------------------------")


# Execute main
main()
