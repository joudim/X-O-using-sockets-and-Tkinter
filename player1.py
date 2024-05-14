import socket
from gameboard import BoardClass 
import tkinter as tk

#client 
# X
class ticTacToeUI():
    """Player 2's Tic Tac Toe UI """

    def __init__(self)-> None:
        self.canvasSetup()
        self.initTKVariables()
        self.createIPAdrsEntry()
        self.createPortEntry()
        self.createUsernameEntry()
        self.connectionButton()
        self.gameButtons()
        self.runUI()


    def canvasSetup (self)-> None:
        """Initialize the TicTacToeUI class."""
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Tic Tac Toe- Player1") # sets the window title

    #define a method that intializes my tk variables
    def initTKVariables(self)-> None:
        """Initialize Tkinter variables and labels."""
        self.ipadrs = tk.StringVar()
        self.port= tk.IntVar()
        self.player1name= tk.StringVar()
        self.player2name= tk.StringVar()
        self.connectionLabel= tk.Label(text="")
        self.connectionLabel.grid(row=1, column=2)
        self.statusLabel=tk.Label(text="")
        self.statusLabel.grid(row=3, column=0)
        self.buttons = [[" " for _ in range(3)] for _ in range(3)] 
        self.board= [[" " for _ in range(3)] for _ in range(3)] 
        self.player1Socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameBoard= BoardClass("X")


        #define a method that creates a number entry field
    def createIPAdrsEntry(self)-> None:
        """Create the IP address entry field."""
        tk.Label(self.root, text="Host's IP Address:").grid(row=0, column=0)
        self.ipadrsEntry= tk.Entry(self.root, textvariable=self.ipadrs)
        self.ipadrsEntry.grid(row=0, column=1)

    #define a method that creates a number entry field
    def createPortEntry(self)-> None:
        """Create the port number entry field."""
        tk.Label(self.root, text="Host's Port Number:").grid(row=1, column=0)
        self.portEntry= tk.Entry(self.root, textvariable=self.port)
        self.portEntry.grid(row=1, column=1)

    def createUsernameEntry(self)-> None:
        """Create the username entry field."""
        tk.Label(self.root, text="Enter Your Username:").grid(row=2, column=0)
        self.player1name=tk.Entry(self.root, textvariable=self.player1name)
        self.player1name.grid(row=2, column= 1)

    def connectionButton(self)-> None:
        """Create the connection button."""
        connectionButton = tk.Button(self.root, text="Connect", command=self.connection)
        connectionButton.grid(row=0, column=2)

    
    def connection(self)-> None:
        """Handle the connection between Player 1 and Player 2."""
        ipadrs= self.ipadrs.get()
        port = self.port.get()
        self.player1name= self.player1name.get()
        try:
            self.player1Socket.connect((ipadrs, port)) #Connecting to the host
            self.player1Socket.sendall(self.player1name.encode())
            self.player2name= self.player1Socket.recv(1024).decode()
            self.connectionLabel.config(text=f"Connected to {self.player2name}")
            self.statusLabel.config(text= f"its {self.player1name}'s turn. They are X")
            self.root.update()

        except(Exception): #If connection was unsuccessful, asks user to try again or terminate
                self.connectionLabel.config(text= "Wrong IP Address and/or port number. Try again?") 
                tk.Button(self.root, text="Yes", command=self.retryConnection).grid(row=2, column=2)
                tk.Button(self.root, text="No", command=self.root.destroy).grid(row=3, column=2)
                self.root.update()

                
    def retryConnection(self)-> None:
        """Handle unsuccessful connections."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.initTKVariables()
        self.createIPAdrsEntry()
        self.createPortEntry()
        self.createUsernameEntry()
        self.connectionButton()
        self.gameButtons()


    def gameButtons(self)-> None:
        """Create the game buttons for the Tic Tac Toe board."""
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, command=lambda r=row, c=col: self.buttonClicked(r ,c), width=10, height=5)
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
            self.statusLabel.config(text="")
            xposition= str(row)+ " "+ str(col)
            self.gameBoard.lastUsername = self.player1name
            self.player1Socket.sendall(xposition.encode())
            self.board, self.buttons= self.gameBoard.updateGameBoard(self.board,self.buttons,row, col, "X")
            self.root.update()

            if self.gameBoard.isWinner(self.board, "X"): 
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
                self.statusLabel.config(text= f"its {self.player2name}'s turn. They are O")
                self.root.update()
                self.gameBoard.lastUsername = self.player2name
                oPosition= self.player1Socket.recv(1024).decode()
                row, col = map(int, oPosition.split()) 
                self.board , self.buttons =self.gameBoard.updateGameBoard(self.board,self.buttons,row, col, "O")
                self.root.update()

                if self.gameBoard.isWinner(self.board, "O"):
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
                    self.statusLabel.config(text= f"its {self.player1name}'s turn.  They are X")
                    self.root.update()    
        else:
            self.statusLabel.config(text= "Position taken")
            self.root.update()
    


    def displayGameResult(self)-> None:
        """Display the game statistics and results."""
        self.player1Socket.sendall("Fun Times!".encode())
        self.playAgainLabel.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.gameBoard.player1name= self.player1name
        self.gameBoard.player2name= self.player2name
        stats= self.gameBoard.computeStats()
        for i in range(len(stats)):
            tk.Label(text=f"{stats[i]}").grid(row=7+i, column=1)
        self.player1Socket.close() 


    def resetGame(self)-> None:
        """Reset the game to play again."""
        self.player1Socket.sendall("Play Again!".encode())
        self.playAgainLabel.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.statusLabel.config(text= f"its {self.player1name}'s turn.  They are X")
        self.board, self.buttons= self.gameBoard.resetGameBoard(self.board, self.buttons)
        self.root.update()



    def playAgain(self)-> None:
        """Asks player 1 if they want to play another game."""
        self.playAgainLabel=tk.Label(text="Do you want to play again?")
        self.playAgainLabel.grid(row=3, column=1)
        self.button1=tk.Button(self.root, text="Yes", command=self.resetGame)
        self.button1.grid(row=3, column=2)
        self.button2= tk.Button(self.root, text="No", command=self.displayGameResult)
        self.button2.grid(row=3, column=3)


    #define a method start UI
    def runUI (self)-> None:
        """Start the User Interface for the game."""
        #starts my UI - event handler
        self.root.mainloop()

if __name__ == "__main__":   
    ticTacToeUI()


