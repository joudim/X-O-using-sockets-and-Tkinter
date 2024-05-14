import socket
from gameboard import BoardClass 
import tkinter as tk
#Host
# O
class ticTacToeUI():
    """Player 2's Tic Tac Toe UI """

    def __init__(self)-> None:
        """Initialize the TicTacToeUI class."""
        self.canvasSetup()
        self.initTKVariables()
        self.createIPAdrsEntry()
        self.createPortEntry()
        self.createUsernameEntry()
        self.connectionButton()
        self.gameButtons()
        self.runUI()

    def canvasSetup (self)-> None:
        """Set up the Tkinter canvas for the game."""
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Tic Tac Toe- Player2") # sets the window title

    def initTKVariables(self)-> None:
        """Initialize Tkinter variables and labels."""
        self.ipadrs = tk.StringVar()
        self.port= tk.IntVar()
        self.player2name= tk.StringVar()
        self.player1name= tk.StringVar()
        self.connectionLabel= tk.Label(text=" ")
        self.connectionLabel.grid(row=1, column=2)
        self.statusLabel=tk.Label(text="")
        self.statusLabel.grid(row=3, column=0)
        self.buttons = [[" " for _ in range(3)] for _ in range(3)] 
        self.board= [[" " for _ in range(3)] for _ in range(3)] 
        self.player2Socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameBoard= BoardClass("O")

    def createIPAdrsEntry(self)-> None:
        """Create the IP address entry field."""
        tk.Label(self.root, text="Your IP Address:").grid(row=0, column=0)
        self.ipadrsEntry= tk.Entry(self.root, textvariable=self.ipadrs)
        self.ipadrsEntry.grid(row=0, column=1)

    def createPortEntry(self)-> None:
        """Create the port number entry field."""
        tk.Label(self.root, text="Select a Port Number:").grid(row=1, column=0)
        self.portEntry= tk.Entry(self.root, textvariable=self.port)
        self.portEntry.grid(row=1, column=1)

    def createUsernameEntry(self)-> None:
        """Create the username entry field."""
        tk.Label(self.root, text="Enter Your Username:").grid(row=2, column=0)
        self.player2name=tk.Entry(self.root, textvariable=self.player2name)
        self.player2name.grid(row=2, column= 1)

        
    def connectionButton(self)-> None:
        """Create the connection button."""
        connectionButton = tk.Button(self.root, text="Connect", command=self.connection)
        connectionButton.grid(row=0, column=2)
        return True

    def connection(self)-> None:
        """Handle the connection between Player 1 and Player 2."""
        ipadrs= self.ipadrs.get()
        port = self.port.get()
        self.player2name= self.player2name.get()
        #create a socket object on my server
        self.player2Socket.bind((ipadrs,port))
        self.player2Socket.listen(1)
        self.connectionLabel.config(text="Waiting for a player to connect")
        self.root.update()

        #Connect to player one 
        self.player2Socket, address= self.player2Socket.accept()
        self.player1name= self.player2Socket.recv(1024).decode()
        self.player2Socket.sendall(self.player2name.encode())
        self.connectionLabel.config(text=f"Connected to {self.player1name}")
        self.root.update()
        self.statusLabel.config(text= f"its {self.player1name}'s turn. They are X")
        self.root.update()

        xposition = self.player2Socket.recv(1024).decode()
        row, col = map(int, xposition.split()) 


        self.board, self.buttons= self.gameBoard.updateGameBoard(self.board,self.buttons,row, col, "X")
        self.root.update()

        self.statusLabel.config(text= f"its {self.player2name}'s turn They are O")
        self.root.update()
        self.gameBoard.lastUsername = self.player2name


    def gameButtons(self)-> None:
        """Create the game buttons for the Tic Tac Toe board."""
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, command=lambda r=row, c=col: self.buttonClicked(r, c), width=10, height=5)
                button.grid(row=row + 4, column=col)
                self.buttons[row][col] = button
                self.board[row][col]= button.cget("text")

    def disableButtons(self)-> None:
        """Disable game buttons when the game ends."""
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(state="disabled")

    def buttonClicked(self, row, col)-> None:
        """Handle button clicks on the Tic Tac Toe board.
        
        Args:
            row (int): The row position of the move.
            col (int): The column position of the move.
        """
        if self.board[row][col]== "":
            self.gameBoard.lastUsername = self.player2name
            self.statusLabel.config(text="")
            oPosition= str(row)+ " "+ str(col)
            self.player2Socket.sendall(oPosition.encode())
            self.board, self.buttons= self.gameBoard.updateGameBoard(self.board,self.buttons,row, col, "O")
            self.root.update()
            if self.gameBoard.isWinner(self.board, "O"):
                self.statusLabel.config(text="You Win!")
                self.root.update()
                self.gameBoard.updateGamesPlayed()
                self.disableButtons()
                self.playAgain()

            elif self.gameBoard.boardIsFull(self.board): 
                self.statusLabel.config(text="It's a Tie!")
                self.root.update()
                self.gameBoard.updateGamesPlayed()
                self.disableButtons()
                self.playAgain()

            else:
                self.statusLabel.config(text= f"its {self.player1name}'s turn. They are X")
                self.root.update()
                self.gameBoard.lastUsername = self.player1name
                xPosition= self.player2Socket.recv(1024).decode()
                row, col = map(int, xPosition.split()) 
                self.board, self.buttons= self.gameBoard.updateGameBoard(self.board,self.buttons,row, col, "X")
                self.root.update()

                if self.gameBoard.isWinner(self.board, "X"): 
                    self.statusLabel.config(text="You Lost!")
                    self.root.update()
                    self.gameBoard.updateGamesPlayed()
                    self.disableButtons()
                    self.playAgain()

                elif self.gameBoard.boardIsFull(self.board): 
                    self.statusLabel.config(text="It's a Tie!")
                    self.root.update()
                    self.gameBoard.updateGamesPlayed()
                    self.disableButtons()
                    self.playAgain()
                else:
                    self.statusLabel.config(text= f"its {self.player2name}'s turn They are O")
                    self.root.update()
        else:
            self.statusLabel.config(text= "Position taken")
            self.root.update()
            

    def displayGameResult(self)-> None:
        """Display the game statistics and results."""
        self.gameBoard.player1name= self.player1name
        self.gameBoard.player2name= self.player2name
        stats= self.gameBoard.computeStats()
        for i in range(len(stats)):
            tk.Label(text=stats[i]).grid(row=7+i, column=1)
        self.player2Socket.close() 


    def playAgain(self)-> None:
        """Handle the option to play another game."""
        response= self.player2Socket.recv(1024).decode()
        if response== "Play Again!":
            self.board, self.buttons= self.gameBoard.resetGameBoard(self.board, self.buttons)
            self.statusLabel.config(text= f"its {self.player1name}'s turn. They are X")
            self.root.update()
            self.gameBoard.lastUsername = self.player1name

            xposition = self.player2Socket.recv(1024).decode()
            row, col = map(int, xposition.split()) 
            self.board, self.buttons= self.gameBoard.updateGameBoard(self.board,self.buttons,row, col, "X")
            self.root.update()

            self.statusLabel.config(text= f"its {self.player2name}'s turn They are O")
            self.root.update()
            self.gameBoard.lastUsername = self.player2name

        elif response== "Fun Times!": 
            tk.Label(text=response).grid(row=3, column=1) 
            self.displayGameResult()


    #define a method start UI
    def runUI (self)-> None:
        """Start the User Interface for the game."""
        #starts my UI - event handler
        self.root.mainloop()

if __name__ == "__main__":   
    ticTacToeUI()