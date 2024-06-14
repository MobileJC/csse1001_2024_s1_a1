# DO NOT modify or add any import statements
from typing import Optional
from a1_support import *

# Name: Wilkinson John Chan
# Student Number: 47277610
# ----------------

#Global variable
board = []
help = ['H', 'h']
quit = ['Q', 'q']
quit_confirm = ['Y', 'y']
add = ['A', 'a']
remove = ['R', 'r']

# Write your classes and functions here
def num_hours() -> float:
    """(float) Returns the number of hours I estimated 
        spent on the assignment.
    """
    est_hours = 50.5
    return est_hours

def generate_initial_board() -> list[str]:
    """(list[str]) Returns initial board state represented by a list
        of string. The list is ordered by leftmost column to rightmost
        column.
    """
    if board == []:
        for col in range(BOARD_SIZE):
            board.append(BLANK_PIECE * BOARD_SIZE)
        return board
    else:
        for col in range(BOARD_SIZE):
            board[col] = (board[col].replace(PLAYER_1_PIECE, BLANK_PIECE)
                          .replace(PLAYER_2_PIECE, BLANK_PIECE))
        return board
        

def is_column_full(column: str) -> bool:
    """(bool) Returns True if the given column is full, False otherwise.

    Parameter:
        column (str): A single column in the board.
    """
    for char in column:
        if char != PLAYER_1_PIECE and char != PLAYER_2_PIECE:
            return False
    return True

def is_column_empty(column: str) -> bool:
    """(bool) Returns True if the given column is empty, False otherwise.

    Parameters:
        column (str): A single column in the board.
    """
    for row in column:
        if row != BLANK_PIECE * len(row):
            return False
    return True 
    

def display_board(board: list[str]) -> None:
    """Prints the game board separated by | and the number of the column.

    Parameters:
        board (list[str]): The current game board status.
    """
    num_rows = len(board[0])
    num_cols = len(board)
    
    for row in range(num_rows):
        print(COLUMN_SEPARATOR, end="")
        for col in range(num_cols):
            print(str(board[col][row]) + COLUMN_SEPARATOR, end="")
        print()
        
    # Print column numbers 
    cols = []
    for num in range(1, num_cols+1):
        cols.append(str(num))
    print_str = " " + " ".join(cols) + " "
    print(print_str)
    
        


def check_input(command: str) -> bool:
    """(bool) Returns True if command is a well formatted, valid command.

        Parameters:
            command (str): It should begin with a character, followed by
            an integer, between 1 and 8 inclusively, does not contain any
            superflous character, and is a valid column on the board.
    """

    #Check for help or quit
    if command in help or command in quit:
        return True
    
    # Check length of command
    if len(command) == 2:
        action, column = command[0], command[-1]
        # Check for command 'add' or 'remove'
        if action not in add and action not in remove:
            print(INVALID_FORMAT_MESSAGE)
            return False
        else:
            # Check for second part of command is a digit or not
            if column.isdigit() is False:
                print(INVALID_COLUMN_MESSAGE)
                return False
            else:
                # Check whether the digit is a number from 1 to 8
                if int(column) not in range(1, 9):
                    print(INVALID_COLUMN_MESSAGE)
                    return False
                else:
                    return True
    else:
        print(INVALID_FORMAT_MESSAGE)
        return False
    

def get_action() -> str:
    """(str): Repeatedly prompts the user for a valid command
        checked by check_input, then returns the first valid
        command entered by the user.
    """
    while True:
        user_input = input(ENTER_COMMAND_MESSAGE)
        if check_input(user_input) is False:
            continue
        else:
            return user_input

def add_piece(board: list[str], piece: str, column_index: int) -> bool:
    """(bool) Adds specified piece to the column at the given
        column_index of the given board and returns True if
        the piece was successfully added, else returns False
        and an error message.

    Parameters:
        board (list[str]): Board yet to be updated.
        piece (str): Piece specified by the user.
        column_index (index): 0-indexed which means it starts from 0.
    """
    if is_column_full(board[column_index]):
        print(FULL_COLUMN_MESSAGE)
        return False
    
    row = 0
    # len(board[column_index]) = 8
    while row < len(board[column_index]):
        if board[column_index][row] == BLANK_PIECE:
            row += 1
        else:
            break

    if row < 8:
        # Copy everything before and after the targeted row
        board[column_index] = board[column_index][:row - 1] 
        + piece + board[column_index][row:]
        return True
    else:
        # Copy everything before and after the targeted row
        board[column_index] = board[column_index][:row - 1] + piece
        return True
    

                    

def remove_piece(board: list[str], column_index: int) -> bool:
    """(bool) Removes the bottom-most piece from the specified column
        and moves all other pieces in the specified column down a row.
        Returns true if a piece is successfully removed according to
        the game rule, else returns False and an error message.

    Parameters:
        board (list[str]): Board yet to be updated.
        column_index: 0-indexed which means it starts from 0.
    """
    if is_column_empty(board[column_index]):
        print(EMPTY_COLUMN_MESSAGE)
        return False
    
    # Find the piece from the bottom
    row = 7
    while row >= 0:
        if board[column_index][row] != BLANK_PIECE:
            break
        else:
            row -= 1

    
    # Copy everything before and after the targeted row
    board[column_index] = BLANK_PIECE * (BOARD_SIZE - row) 
    + board[column_index][:row]
    return True


def check_win(board: list[str]) -> Optional[str]:
    """(Optional[str]): Returns the winning player's piece
        if a player has formed an unbroken line horizontally,
        vertically, or diagonally, else returns None.

    Parameters:
        board (list[str]): Current board state.
    """
    winning_piece = [0, 0]
    complement_row_index = None

    # Check in rows
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - 3):
            if (board[col][row] == PLAYER_1_PIECE 
                and board[col][row + 1] == PLAYER_1_PIECE 
                and board[col][row + 2] == PLAYER_1_PIECE 
                and board[col][row + 3] == PLAYER_1_PIECE):
                winning_piece[0] += 1
            if (board[col][row] == PLAYER_2_PIECE 
                and board[col][row + 1] == PLAYER_2_PIECE 
                and board[col][row + 2] == PLAYER_2_PIECE 
                and board[col][row + 3] == PLAYER_2_PIECE):
                winning_piece[1] += 1

    # Check in cols
    for col in range(BOARD_SIZE - 3):
        for row in range(BOARD_SIZE):
            if (board[col][row] == PLAYER_1_PIECE 
                and board[col + 1][row] == PLAYER_1_PIECE 
                and board[col + 2][row] == PLAYER_1_PIECE 
                and board[col + 3][row] == PLAYER_1_PIECE):
                winning_piece[0] += 1
            if (board[col][row] == PLAYER_2_PIECE 
                and board[col + 1][row] == PLAYER_2_PIECE 
                and board[col + 2][row] == PLAYER_2_PIECE 
                and board[col + 3][row] == PLAYER_2_PIECE):
                winning_piece[1] += 1

    # Check forward diagonals \
    for col in range(BOARD_SIZE - 3):
        for row in range(BOARD_SIZE - 3):
            if (board[col][row] == PLAYER_1_PIECE 
                and board[col + 1][row + 1] == PLAYER_1_PIECE 
                and board[col + 2][row + 2] == PLAYER_1_PIECE 
                and board[col + 3][row + 3] == PLAYER_1_PIECE):
                winning_piece[0] += 1
            if (board[col][row] == PLAYER_2_PIECE 
                and board[col + 1][row + 1] == PLAYER_2_PIECE 
                and board[col + 2][row + 2] == PLAYER_2_PIECE 
                and board[col + 3][row + 3] == PLAYER_2_PIECE):
                winning_piece[1] += 1
                
    # Check backward diagonals /
    for col in range(BOARD_SIZE - 3):
        for row in range(BOARD_SIZE):
            if BOARD_SIZE - row - 1 > 3:
                complement_row_index = BOARD_SIZE - row - 1
            else:
                complement_row_index = 3
            if complement_row_index >= 3:
                if (board[col][complement_row_index] == PLAYER_1_PIECE 
                    and board[col + 1][complement_row_index - 1] 
                    == PLAYER_1_PIECE 
                    and board[col + 2][complement_row_index - 2] 
                    == PLAYER_1_PIECE 
                    and board[col + 3][complement_row_index - 3] 
                    == PLAYER_1_PIECE):
                    winning_piece[0] += 1
                if (board[col][complement_row_index] == PLAYER_2_PIECE 
                    and board[col + 1][complement_row_index - 1] 
                    == PLAYER_2_PIECE 
                    and board[col + 2][complement_row_index - 2] 
                    == PLAYER_2_PIECE 
                    and board[col + 3][complement_row_index - 3] 
                    == PLAYER_2_PIECE):
                    winning_piece[1] += 1
        
        

    # Return winning piece
    if winning_piece[0] > 0 and winning_piece[1] > 0:
        return BLANK_PIECE
    elif winning_piece[0] > 0:
        return PLAYER_1_PIECE
    elif winning_piece[1] > 0:
        return PLAYER_2_PIECE
    else:
        return None

def play_game() -> None:
    """Simple composition of game functions.
        This function coordinates gamaplay of a single game
        from start to finish.
    """
    board = generate_initial_board()
    turn_num = 0
    winning_condition = check_win(board)
    is_invalid_add_removal = False
    while winning_condition is None:
        if not is_invalid_add_removal:
            display_board(board)
        winning_condition = check_win(board)
        if turn_num % 2 == 0:
            #Player 1's turn
            if not is_invalid_add_removal:
                print(PLAYER_1_MOVE_MESSAGE)
            user_command = get_action()
            if user_command[0] in add:
                if add_piece(board, PLAYER_1_PIECE, int(user_command[1])-1):
                    # Move to next player's turn
                    turn_num += 1
                    winning_condition = check_win(board)
                    is_invalid_add_removal = False
                else:
                    is_invalid_add_removal = True
            elif user_command[0] in remove:
                if remove_piece(board, int(user_command[1])-1):
                    # Move to next player's turn
                    turn_num += 1
                    winning_condition = check_win(board)
                    is_invalid_add_removal = False
                else:
                    is_invalid_add_removal = True
            elif user_command in help:
                print(HELP_MESSAGE)
            elif user_command in quit:
                break
        else:
            # Player 2's turn
            if not is_invalid_add_removal:
                print(PLAYER_2_MOVE_MESSAGE)
            user_command = get_action()
            if user_command[0] in add:
                if add_piece(board, PLAYER_2_PIECE, int(user_command[1])-1):
                    # Move to next player's turn
                    turn_num += 1
                    winning_condition = check_win(board)
                    is_invalid_add_removal = False
                else:
                    is_invalid_add_removal = True
            elif user_command[0] in remove:
                if remove_piece(board, int(user_command[1])-1):
                    # Move to next player's turn
                    turn_num += 1
                    winning_condition = check_win(board)
                    is_invalid_add_removal = False
                else:
                    is_invalid_add_removal = True
            elif user_command in help:
                print(HELP_MESSAGE)
            elif user_command in quit:
                break
    
    # Display winning board and message if a line of four is formed
    if winning_condition != None:
        display_board(board)
        if winning_condition is BLANK_PIECE:
            print(DRAW_MESSAGE)
        elif winning_condition is PLAYER_1_PIECE:
            print(PLAYER_1_VICTORY_MESSAGE)
        elif winning_condition is PLAYER_2_PIECE:
            print(PLAYER_2_VICTORY_MESSAGE)
        else:
            return


def main() -> None:
    """ Entry-point to gameplay """
    generate_initial_board()
    play_game()
    
    # Flow after first game
    replay_prompt = input(CONTINUE_MESSAGE)
    while replay_prompt in quit_confirm:
        generate_initial_board()
        play_game()
        replay_prompt = input(CONTINUE_MESSAGE)
        
        
if __name__ == "__main__":
    main()