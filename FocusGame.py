# Author: Jesse Narkmanee
# Date: 11/25/2020
# Description: Final portfolio game called Domination or Focus that implements 2-d lists to represent the
# board, strings to represent the colored pieces, and individual lists to represent the stacks of pieces.

class FocusGame:
    """ This is the main and only class in this program. It takes the names and colors of both
    players as its parameters and also declares a reserve and capture list as member objects so that when the players
    reserve or capture a piece, they can store it in there. Then this class has a member variable to store and indicate whose previous
    turn it was so that we can keep track if someone plays out of turn. The class lastly creates the whole starting board
    represented as a 2d-array where its implemenation will be further explained down below."""
    def __init__(self, player_1, player_2):
        self._player_1 = player_1[0]
        self._player_2 = player_2[0]
        self._player_1_color = player_1[1]
        self._player_2_color = player_2[1]

        self._reserve_1 = []
        self._captured_1 = []
        self._reserve_2 = []
        self._captured_2 = []

        self._turn = None

        # Our coordinate tuple input gets stored as our rows and columns.
        rows, cols = (6, 6)
        # We use list comprehension and a nested for loop to create the bounds of our rows and columns.
        self._board = [[['G'] for i in range(cols)] for j in range(rows)]
        # A counter is created so that after every two pieces a red piece must be put in. The counter then
        # resets so that green pieces can stay on the board. We traverse this 2-d array using a nested for loop.
        count = 1
        for i in range(rows):
            for j in range(cols):
                if count <= 2:
                    self._board[i][j] = ['R']
                count += 1
                if count > 4:
                    count = 1
        # To sometimes check, we print the starting board where multiple pieces are represented as another list.
        # print(self._board)

    def pop(self, lst, pieces):
        """ We use Python's list splicing method to get the back of the list, indicated by pieces.
        We pop off then delete the last elements of the list of top of the stack first and append it onto a list we
        will later return to indicate the pieces we popped off in order. A counter is used because a person
        can move more than one piece so if more than one piece is popped off it bus be iterated. What is returned are
        the pieces we popped off which will be later added to the new location."""
        popped_lst = []

        while pieces > 0:
            popped_lst.append(lst[-pieces])
            del lst[-pieces]
            pieces -= 1

        return popped_lst

    def move_piece(self, player_name, move_from, move_to, pieces):
        """ Coordinates of the tuples parameters are stored in variables, the player_name is to later indicate
        which player wants to take this turn, and the number of pieces is to indicate how many pieces in the player's
        chosen stack does he or she want to move. First, we store the coordinates of the tuples in variables that will
        later be used when calling the 2d-board array. Then we check if our move is valid or in-bounds. After that, we check
        to see if the player's last turn is the same which meant he or she took two turns in a row which would be illegal, using
        the _turn member variables to see previous turn. The stacks of pieces on the board that is represented as a 2-d list,
        is represented as a list, where the bottom of the stack is 0th index and top is the highest index. Also because of this
        if the number of pieces that the player wants to move, is bigger than the size of the actual stack which is represented
        as a list, an error message will be shown. If all goes well, we call the pop function pops the top pieces of the
        stack depending by how many pieces in the parameter and then we call the extend() method to add these popped pieces
        onto the position we would like to move to. If the moved_to position has more than 5 pieces, then we create a counter
        of the difference of how many pieces and the max 5 so that we know how many times we need to iteratively remove
        the bottom of the stack to either put into the private captured or reserved member lists that were declared
        earlier in the constructor. After this is all done, the program will indicate success or if a player after this move has
        6 or more pieces in its captured members lists, then that player is declared the winner! This code is done two times for
        players 1 and 2 but I think in the future I can condense it to make it more concise. What is returned are
        either the error messages I mentioned before or a succussful move or win indication after one has made a legal move."""
        i, j = move_from
        x, y = move_to

        # If the move is out of bounds of the board or if there are not enough pieces to make a multiple move,
        # then we will return invalid location.
        for variable in [i, j, x, y]:
            if variable < 0 or variable > 6 or x > i + 1 or y > j + 1:
                return "invalid location"

        if player_name == self._player_1:
            if self._turn == player_name:
                return "not your turn"
            self._turn = player_name
            if pieces > len(self._board[i][j]):
                return "invalid number of pieces"

            # Our pop function takes in pieces so that it can make a multiple move if need be.
            # Multiple moves entail creating a counter to iteratively pop off one element at a time
            # to the next legal position indicated by move_to.
            self._board[x][y].extend(self.pop(self._board[i][j], pieces))

            # This checks to see if there are more than 5 pieces in a location after we moved pieces.
            # A counter is made by the difference of 5 to see how many elements we need to dequeue since
            # the specs say we need to remove the bottom or the elements closest to the 0th index. We iteratively
            # keep doing this until our counter reaches 0.
            if len(self._board[x][y]) > 5:
                count = len(self._board[x][y]) - 5

                while count > 0:
                    if self._turn == self._player_1:
                        if self._player_1_color == self._board[x][y][0]:
                            self._reserve_1.append(self._board[x][y][0])
                        else:
                            self._captured_1.append(self._board[x][y][0])
                    elif self._turn == self._player_2:
                        if self._player_2_color == self._board[x][y][0]:
                            self._reserve_2.append(self._board[x][y][0])
                        else:
                            self._captured_2.append(self._board[x][y][0])

                    del self._board[x][y][0]
                    count -= 1

            # Our member function which will return the amount of captured pieces is what will be
            # used to determine if a move is a winning move before returning successful.
            if self.show_captured(player_name) >= 6:
                return "Wins"
            self.print_stuff()
            return "successfully moved"

        elif player_name == self._player_2:
            if self._turn == player_name:
                return "not your turn"
            self._turn = player_name
            if pieces > len(self._board[i][j]):
                return "invalid number of pieces"

            self._board[x][y].extend(self.pop(self._board[i][j], pieces))

            if len(self._board[x][y]) > 5:
                count = len(self._board[x][y]) - 5

                # If it is the player's piece then we store it into reserved list whereas if
                # it is captured, then it is stored in captured list. We also know if the piece is
                # their or not since earlier we saved the player_1 and player_2's color piece, so
                # if the piece string name is the same as their color then it is their piece to then
                # be stored in the appropriate member's list.
                while count > 0:
                    if self._turn == self._player_1:
                        # self._player_1_color
                        if self._player_1_color == self._board[x][y][0]:
                            self._reserve_1.append(self._board[x][y][0])
                        else:
                            self._captured_1.append(self._board[x][y][0])
                    elif self._turn == self._player_2:
                        # self._player_2_color
                        if self._player_2_color == self._board[x][y][0]:
                            self._reserve_2.append(self._board[x][y][0])
                        else:
                            self._captured_2.append(self._board[x][y][0])

                    del self._board[x][y][0]
                    count -= 1

            if self.show_captured(player_name) >= 6:
                return "Wins"
            self.print_stuff()
            return "successfully moved"
        else:
            return "player not found"

    def show_pieces(self, position):
        """ Captures the positions of the tuple parameter so that it can return that same location
        on the 2-d array board. What is returned is the actual stack represented as a list at that location."""
        i, j = position
        return self._board[i][j]

    def show_reserve(self, player_name):
        """ Depending on which player is passed into the function, we will either show the size of
        player 1 or player 2's reserved list. What is returned is the length of the reserved list or 0 if it is empty."""
        if player_name == self._player_1:
            return len(self._reserve_1)
        elif player_name == self._player_2:
            return len(self._reserve_2)
        else:
            return 0

    def show_captured(self, player_name):
        """ Depending on which player is passed into the function, we will either show the size of
        player 1 or player 2's captured list. What is returned is the length of the captured list or 0 if it is empty."""
        if player_name == self._player_1:
            return len(self._captured_1)
        elif player_name == self._player_2:
            return len(self._captured_2)
        else:
            return 0

    def reserved_move(self, player_name, move_to):
        """ We capture the coordinates of the tuple of the variable, make sure that it is our turn
        by looking at our member variable that indicates who had the previous turn, and if there is no error
        the method looks to see if we need to move player_1 or player_2's reservation piece. If there is
        no piece for either player then a string indicated with that error will be returned"""
        x, y = move_to

        if self._turn == player_name:
            return "not your turn"
        self._turn = player_name

        if player_name == self._player_1:
            if self._reserve_1:
                self._board[x][y].extend(self.pop(self._reserve_1, 1))
            else:
                return "no pieces in reserve"
        elif player_name == self._player_2:
            if self._reserve_2:
                self._board[x][y].extend(self.pop(self._reserve_2, 1))
            else:
                return "no pieces in reserve"

    def print_stuff(self):
        """ Trivial function that prints the private member variable, for testing purposes."""
        print(self._board)


# Used for testing only
def main():
    game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
    # print(game.move_piece('PlayerA', (0, 0), (0, 1), 1))  # Returns message "successfully moved"
    # print(game.move_piece('PlayerB', (0, 2), (0, 1), 1))
    # print(game.move_piece('PlayerA', (0, 3), (0, 1), 1))
    # print(game.move_piece('PlayerB', (0, 4), (0, 1), 1))
    # print(game.move_piece('PlayerA', (0, 5), (0, 1), 1))
    # print(game.move_piece('PlayerB', (1, 0), (0, 1), 1))
    # print(game.move_piece('PlayerA', (0, 1), (0, 0), 1))

    print(game.move_piece('PlayerA', (0, 0), (0, 1), 1))  # Returns message "wins"
    print(game.move_piece('PlayerB', (1, 0), (1, 1), 1))
    print(game.move_piece('PlayerA', (0, 1), (0, 2), 2))
    print(game.move_piece('PlayerB', (1, 1), (1, 2), 2))
    print(game.move_piece('PlayerA', (0, 2), (0, 3), 3))
    print(game.move_piece('PlayerB', (1, 2), (1, 3), 3))
    print(game.move_piece('PlayerA', (0, 3), (0, 4), 4))
    print(game.move_piece('PlayerB', (1, 3), (1, 4), 4))
    print(game.move_piece('PlayerA', (0, 4), (0, 5), 5))
    print(game.move_piece('PlayerB', (1, 4), (1, 5), 5))
    print(game.move_piece('PlayerA', (0, 5), (1, 5), 5))
    print(game.move_piece('PlayerB', (2, 2), (2, 3), 1))
    print(game.move_piece('PlayerA', (1, 5), (2, 5), 5))
    print(game.move_piece('PlayerB', (2, 3), (2, 4), 2))
    print(game.move_piece('PlayerA', (2, 5), (2, 4), 5))
    print(game.move_piece('PlayerB', (3, 5), (3, 4), 1))
    print(game.move_piece('PlayerA', (2, 4), (3, 4), 5))

    game.print_stuff()
    # print(game.show_pieces((0, 1)))  # Returns ['R','R']
    print(game.show_captured('PlayerA'))  # Returns 0
    # game.reserved_move('PlayerA', (0, 0))  # Returns message "No pieces in reserve"
    print(game.show_reserve('PlayerA'))  # Returns 0

    print(game.show_captured('PlayerB'))  # Returns 0
    # game.reserved_move('PlayerA', (0, 0))  # Returns message "No pieces in reserve"
    print(game.show_reserve('PlayerB'))  # Returns 0
    game.print_stuff()


if __name__ == "__main__":
    main()
