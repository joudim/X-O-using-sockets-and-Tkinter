class BoardClass:
    """Class that manipulates the board of a tic-tac-toe game.

    Attributes:
        player1name (str): The username of player 1.
        player2name (str): The username of player 2.
        lastUsername (str): The username of the last player who made a move.
        wins (int): The number of wins by the player.
        ties (int): The number of tied games.
        losses (int): The number of losses by the player.
        gamesPlayed (int): The number of games played.
        symbol (str): The symbol used by the player in the game ('X' or 'O').
    """
    def __init__(self, symbol)-> None:
        """Initialize the BoardClass.

        Args:
            symbol (str): The symbol(X/O) representing the player in the game.
        """
        self.player1name = ""
        self.player2name= ""
        self.lastUsername= "" 
        self.wins= 0
        self.ties= 0 
        self.losses= 0
        self.gamesPlayed=0
        self.symbol=symbol


    def updateGamesPlayed(self)-> None: 
        """Counter that increments the number of games played."""
        self.gamesPlayed += 1

    def resetGameBoard(self, board, buttons)-> tuple: 
        """Resets the game board to its initial empty state.
         Args:
            board (list): The game board.
            buttons (list): The buttons representing the board in the UI.

        Returns:
            tuple: cleared game board and buttons.
        """
        for row in range(3):
            for col in range(3):
                buttons[row][col].config(text=" ", state="normal") 
                board[row][col] = ""
        return board, buttons     

    def updateGameBoard(self, board, buttons,row, col, symbol)-> list:
        """Updates the game board with the player's move.

        Args:
            board (list): The game board.
            buttons (list): The buttons representing the board in the UI.
            row (int): The row position of the move.
            col (int): The column position of the move.
            symbol (str): The symbol(X/O) representing the player in the game.
        Returns:
            tuple: Updated game board and buttons with the latest move.
        """
        buttons[row][col].config(text=symbol)
        board[row][col]= buttons[row][col].cget("text")
        return board ,buttons

            
            
    def boardIsFull(self, board)-> bool: 
        """Checks if the board is full then updates the ties count accordingly.
        Args:
            board (list): The game board.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        for row in board:
            for position in row:
                if position == '':
                    return False
        self.ties+=1
        return True
    
    def isWinner(self, board, symbol)-> bool:
        """Checks if the last move led to a win and updates the wins and losses count.

        Args:
            board (list): The game board.
            symbol (str): The symbol (X/O) of the player making the move.

        Returns:
            bool: True if the move led to a win, False if not.
        """   
        if symbol == self.symbol:
            # Check horizontal
            for row in board:
                if row[0] == row[1] == row[2] == symbol:
                    self.wins += 1 
                    return True

            # Check vertical
            for col in range(3):
                if board[0][col] == board[1][col] == board[2][col] == symbol:
                    self.wins += 1 
                    return True

            # Check diagonal (top-left to bottom-right)
            if board[0][0] == board[1][1] == board[2][2] == symbol:
                self.wins += 1 
                return True

            # Check diagonal (top-right to bottom-left)
            if board[0][2] == board[1][1] == board[2][0] == symbol:
                self.wins += 1 
                return True
        elif symbol != self.symbol:
            # Check horizontal
            for row in board:
                if row[0] == row[1] == row[2] == symbol:
                    self.losses+=1
                    return True

            # Check vertical
            for col in range(3):
                if board[0][col] == board[1][col] == board[2][col] == symbol:
                    self.losses+=1
                    return True

            # Check diagonal (top-left to bottom-right)
            if board[0][0] == board[1][1] == board[2][2] == symbol:
                self.losses += 1 
                return True

            # Check diagonal (top-right to bottom-left)
            if board[0][2] == board[1][1] == board[2][0] == symbol:
                self.losses += 1 
                return True
        else:
            return False

    def computeStats(self)-> list[str]: 
        """Compute and display the player's statistics.
        Returns:
            stats (list): Player's statistics.
        """ 
        stats= [f"Player 1's User Name: {self.player1name}",
                f"Player 2's User Name: {self.player2name}",
                f"Last Person to Make a Move: {self.lastUsername}",
                f"Number of Games: {self.gamesPlayed}",
                f"Number of Wins: {self.wins}",
                f"Number of Losses: {self.losses}",
                f"Number of Ties: {self.ties}"]
        return stats