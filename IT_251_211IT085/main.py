import tkinter as tk
from sudokuconnections import SudokuConnections
from sudoku import Sudoku


class SudokuBoard:
    def __init__(self, master):
        # Initialize the SudokuBoard object
        self.master = master  # The main Tkinter window
        self.master.title("Sudoku Board")  # Set the title of the window
        # Create a label widget with the text "Sudoku Board"
        self.label = tk.Label(self.master, text="Sudoku Board")
        self.label.pack()  # Add the label widget to the main window
        # Create a canvas widget with width 500 and height 500
        self.canvas = tk.Canvas(self.master, width=400, height=500)
        self.canvas.pack()  # Add the canvas widget to the main window
        # Call the getBoard() method to generate a new Sudoku board
        self.board = self.getBoard()
        # Create a SudokuConnections object to represent the connections between cells
        self.sudokuGraph = SudokuConnections()
        # Call the __getMappedMatrix() method to map the Sudoku board to a 2D array of cells
        self.mappedGrid = self.__getMappedMatrix()
        self.printBoard()  # Call the printBoard() method to draw the Sudoku board on the canvas

        # Add a label widget to display the output
        self.output_label = tk.Label(self.master, text="")
        self.output_label.pack()

        # Add a button widget to solve the Sudoku puzzle
        self.solve_button = tk.Button(self.master, text="Solve", command=self.solveGraphColoring)
        self.solve_button.pack()

        # Add a button widget to clear the Sudoku board
        self.clear_button = tk.Button(
            self.master, text="Clear", command=self.clearBoard)
        self.clear_button.pack()

        self.flag = True  # A flag to indicate whether the puzzle has been solved or not

    '''
    This private method initializes and returns a matrix of size 16x16 with each element initialized to 0. 
    It also assigns a unique value to each element in the matrix from 1 to 256 (16x16). 
    This is used to map each cell of the Sudoku board to a unique value for graph coloring.
    '''

    def __getMappedMatrix(self):
        matrix = [[0 for cols in range(16)] for rows in range(16)]
        count = 1
        for rows in range(16):
            for cols in range(16):
                matrix[rows][cols] = count
                count += 1
        return matrix

    '''
    This method generates a new Sudoku board using the Sudoku class from the Sudokupy library. 
    It sets the difficulty level to 0.3, which means that approximately 30% of the cells will be filled initially.
    It then converts any None values to 0 to simplify the display process. Returns the generated board.
    '''

    def getBoard(self):
        board1 = Sudoku(4).difficulty(0.3)
        board = board1.board
        # board[0][0]=1
        # board[0][1]=1
        #  (uncomment to obtain incorrect sudoku board)
        
        for row in range(16):
            for col in range(16):
                if board[row][col] == None:
                    board[row][col] = 0
        return board

    def clearBoard(self):
        # Generate a new random Sudoku board with the same difficulty level as the current board
        self.board = self.getBoard()

        # Delete all items in the canvas
        self.canvas.delete("all")

        # Update the canvas to display the new board
        self.printBoard()

    def printBoard(self):
        # Define a dictionary mapping integers to characters to be used for displaying the Sudoku board
        character = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
                     8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G"}

        for i in range(len(self.board)):
            # Create lines to separate 4x4 grids horizontally and vertically
            if i % 4 == 0:
                self.canvas.create_line(
                    (0, i * 25), (400, i * 25), width=2)  # horizontal
                self.canvas.create_line(
                    (i * 25, 0), (i * 25, 400), width=2)  # vertical

            # Loop through each element in the row of the board matrix
            for j in range(len(self.board[i])):
                x = j * 25  # X-coordinate for the text to be displayed
                y = i * 25  # Y-coordinate for the text to be displayed

                # If the current cell of the board is not empty, display the corresponding character
                if self.board[i][j] != 0:
                    self.canvas.create_text(
                        x + 12.5, y + 12.5, text=str(character[self.board[i][j]]))
                # If the current cell of the board is empty, display a blank space
                else:
                    self.canvas.create_text(x + 12.5, y + 12.5, text=" ")
                    self.canvas.create_line((0, 400), (400, 400), width=2)
                    self.canvas.create_line((400, 0), (400, 400), width=2)
                    self.canvas.create_line((0, 3), (400, 3), width=2)
                    self.canvas.create_line((3, 0), (3, 400), width=2)
        for i in range(1, 16):
            self.canvas.create_line((25*i, 0), (25*i, 400), width=1)
        for i in range(1, 16):
            self.canvas.create_line((0, 25*i), (400, 25*i), width=1)

    '''
    This method checks if the Sudoku board has any blank cells (denoted by 0)
    If a blank cell is found, the method returns the row and column indices of that cell If no blank cells are found, the method returns None
    '''

    def is_Blank(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    return (row, col)
        return None

    '''
    This function checks if the given number is valid to be placed at the given position.
    It takes in two parameters: - num: The number that we want to check if it is valid at the given position - pos: The position (row, column) where we want to check if the number is valid 
    It first checks if the number already exists in the same row or not.
    If it exists in the same row, it means the number is not valid and the function returns False.
    Next, it checks if the number already exists in the same column or not. If it exists in the same column, it means the number is not valid and the function returns False.
    Finally, it checks if the number already exists in the same 4x4 block or not.
    If it exists in the same block, it means the number is not valid and the function returns False.
    If the number does not violate any of the above conditions, it is considered valid and the function returns True.
    '''

    def isValid(self, num, pos):
        # ROW
        for col in range(len(self.board[0])):
            if self.board[pos[0]][col] == num and pos[0] != col:
                return False

        # COL
        for row in range(len(self.board)):
            if self.board[row][pos[1]] == num and pos[1] != row:
                return False

        # BLOCK
        x = pos[1]//4
        y = pos[0]//4

        for row in range(y*4, y*4+4):
            for col in range(x*4, x*4+4):
                if self.board[row][col] == num and (row, col) != pos:
                    return False

        return True

   

    def graphColoringInitializeColor(self):
        """
        Initializes the colors for the graph based on the given board.

        Returns:
        - color (list): A list containing the colors for each vertex in the graph.
         - given (list): A list containing the ids of vertices whose values are already given in the board.
        """
        color = [0] * (self.sudokuGraph.graph.totalV +
                       1)  # Initialize color list with zeros
        given = []  # Initialize list of already given values

        # Iterate through each cell in the board
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] != 0:  # If the cell is not blank
                    # Get the index of the corresponding vertex in the graph
                    idx = self.mappedGrid[row][col]
                    # Set the color of the vertex to the value of the cell
                    color[idx] = self.board[row][col]
                    # Add the vertex to the list of already given values
                    given.append(idx)

        return color, given  # Return the final color and given lists
    
    def solveGraphColoring(self, m=16):
        color, given = self.graphColoringInitializeColor()
        if self.__graphColorUtility(m=m, color=color, v=1, given=given) is None:
            self.output_label.config(text="No solution found :(")
            self.flag=True
            return False
        count = 1
        for row in range(16):
            for col in range(16):
                self.board[row][col] = color[count]
                count += 1
        self.printBoard()
        self.output_label.config(text="Solution found!")
        return color

    def __graphColorUtility(self, m, color, v, given):
        # Base case: If all vertices are colored, return True
        if v == self.sudokuGraph.graph.totalV + 1:
            return True

        # Try different colors for vertex v
        for c in range(1, m+1):
            # Check if it is safe to assign color c to vertex v
            if self.__isSafe2Color(v, color, c, given) == True:
                # Assign color c to vertex v

                color[v] = c

                if self.__graphColorUtility(m, color, v+1, given):
                    # Recur to assign colors to the rest of the vertices
                    return True
            # Backtrack: if vertex v is not given, then reset the color to 0 and try another color
            if v not in given:
                color[v] = 0

    '''
    This function checks if it is safe to assign a given color c to vertex v in the graph coloring algorithm.
    If the vertex has already been given a value, then it returns True only if the color c matches the given value.
    If the vertex has not been given a value, then it returns False if any of its neighbours have already been colored with c.
    Otherwise, it returns True, indicating that it is safe to color the vertex with c.
    '''            

    def __isSafe2Color(self, v, color, c, given):
        if v in given and color[v] == c:
            return True
        elif v in given:
            return False

        for i in range(1, self.sudokuGraph.graph.totalV+1):
            if color[i] == c and self.sudokuGraph.graph.isNeighbour(v, i):
                return False
        return True


root = tk.Tk()
board = SudokuBoard(root)
# to be uncommented in case of invalid input
# if board.solveGraphColoring() is None:
#     board.output_label.config(text="No solution found :(")
# else:      
root.mainloop()
