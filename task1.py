import tkinter as tk
from tkinter import Frame, Label, Button, messagebox, Entry

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Drawing App")
        self.root.configure(background='navy')
        self.root.geometry("800x600+500+200")
        self.root.resizable(0, 0)
        self.toggle_buttons = []  # List to keep track of toggle buttons
        self.rectangle_color = None
        self.rows = None
        self.cols = None
        self.create_color_frame()
        self.create_input_frame()
        self.create_output_frame()
        self.create_main_frame()
        self.root.mainloop()

    def create_input_frame(self):
        self.inputFrame = Frame(self.root, borderwidth=0, relief="groove")
        self.inputFrame.place(x=20, y=20, width=160, height=80)

        # Add labels and entry widgets
        Label(self.inputFrame, text="Rows:").grid(row=0, column=0)
        self.rowEntry = Entry(self.inputFrame)
        self.rowEntry.grid(row=0, column=1)

        Label(self.inputFrame, text="Columns:").grid(row=1, column=0)
        self.columnEntry = Entry(self.inputFrame)
        self.columnEntry.grid(row=1, column=1)

        # Add a button to save the input
        Button(self.inputFrame, text="Set Grid Size", command=self.save_grid_size).grid(row=2, column=0, columnspan=2)

        # Initialize rows and columns
        self.rows = None
        self.cols = None
    def save_grid_size(self):
        try:
            self.rows = int(self.rowEntry.get())
            self.cols = int(self.columnEntry.get())

            # Clear existing grids and color matrix
            self.canvasInput.delete("all")
            self.canvasOutput.delete("all")
            self.color_matrix = [[None for _ in range(self.cols)] for _ in range(self.rows)]
            self.distance_matrix = [[None for _ in range(self.cols)] for _ in range(self.rows)]  # Initialize the distance_matrix

            # Initialize the new grids
            self.init_rectangle_grid()
            self.init_output_rectangle_grid()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for rows and columns")
    def create_output_frame(self):
        self.outputFrame = Frame(self.root, borderwidth=0, relief="groove")
        self.outputFrame.place(x=640, y=20, width=140, height=80)
        self.solveButton = Button(self.outputFrame, text="Solve maze", font=("Helvetica", 15, "bold"), bg="blue", fg="white", command=self.print_matrix)
        self.solveButton.place(x=0, y=0, width=140, height=80)

    def a_star_algorithm(self, start, goal, grid):
        
        open_set = {start: 0}
        closed_set = set()

        # Store the path taken
        came_from = {}

        
        g_score = {start: 0}

        
        f_score = {start: self.manhattan_distance(start, goal)}

        while open_set:
            
            current = min(open_set, key=lambda node: f_score[node])
            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            del open_set[current]
            closed_set.add(current)

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # Neighbors
                neighbor = (current[0] + dx, current[1] + dy)
                tentative_g_score = g_score[current] + 1

                if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] != '#' and neighbor not in closed_set:
                    if neighbor not in open_set:
                        open_set[neighbor] = 0
                    elif tentative_g_score >= g_score[neighbor]:
                        continue

                    # This path is the best until now
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.manhattan_distance(neighbor, goal)
        return None  
    
    def calculate_and_display_manhattan_distances(self, goal):
        if not hasattr(self, 'distance_matrix'):
            self.distance_matrix = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                # Check if the cell is not a wall and is within the bounds of the maze
                if 0 <= row < self.rows and 0 <= col < self.cols and self.symbol_matrix[row][col] != '#':
                    distance = self.manhattan_distance((row, col), goal)
                    self.distance_matrix[row][col] = distance
                    # Draw the distance on the canvas
                    self.canvasOutput.create_text(col*self.size+self.size//2, row*self.size+self.size//2,
                                                  text=str(distance), font=("Helvetica", 15), fill="white")
                else:
                    # If it's a wall or out of bounds, do not calculate or display the distance
                    self.distance_matrix[row][col] = None


    def print_matrix(self):
        self.convert_color_matrix_to_symbols()
        for row in self.symbol_matrix:
            print(' '.join(map(str, row)))
        self.copy_input_to_output()

        # Find start and goal positions
        start = goal = None
        for i, row in enumerate(self.symbol_matrix):
            for j, val in enumerate(row):
                if val == 'S':
                    start = (i, j)
                elif val == 'G':
                    goal = (i, j)

        if start and goal:
            self.calculate_and_display_manhattan_distances(goal)
            path = self.a_star_algorithm(start, goal, self.symbol_matrix)
            if path:
                print("Path found:", path)
                self.display_path(path)
            else:
                print("No path found")
        else:
            messagebox.showerror("Error", "Start or goal not defined")

    # Corrected manhattan_distance method
    def manhattan_distance(self, start, goal):  # Added self parameter
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    def display_path(self, path):
        for x, y in path:
            self.canvasOutput.create_rectangle(y*self.size, x*self.size, (y+1)*self.size, (x+1)*self.size, fill="green", outline="blue")



    def convert_color_matrix_to_symbols(self):
        # Define the mapping from color codes to symbols
        color_to_symbol = {
            "#d91818": 'S',  # Start
            "#326ba8": '#',  # Wall
            "#23a805": 'G',  # Goal
            "#05070f": '*'   # Path
        }

        self.symbol_matrix = []

        # Check if the color matrix exists
        if hasattr(self, 'color_matrix'):
            for row in self.color_matrix:
                symbol_row = []
                for color in row:
                    symbol = color_to_symbol.get(color)
                    symbol_row.append(symbol)
                self.symbol_matrix.append(symbol_row)


    def create_color_frame(self):
        self.colorFrame = Frame(self.root, borderwidth=0, relief="groove")
        self.colorFrame.place(x=200, y=20, width=400, height=80)
        self.add_color_frame_widgets()

    def create_main_frame(self):
        self.mainFrame = Frame(self.root, borderwidth=0, relief="groove")
        self.mainFrame.place(x=20, y=120, width=760, height=440)
        self.mainInputFrameLabel = Label(self.mainFrame, text="Input Maze", font=("Helvetica", 15, "bold"))
        self.mainInputFrameLabel.place(x=140, y=0)
        self.mainOutputFrameLabel = Label(self.mainFrame, text="Output Maze", font=("Helvetica", 15, "bold"))
        self.mainOutputFrameLabel.place(x=500, y=0)
        self.create_main_input_frame()
        self.create_main_output_frame()

    def create_main_input_frame(self):
        self.mainInputFrame = Frame(self.mainFrame, borderwidth=0, relief="groove")
        self.mainInputFrame.place(x=20, y=50, width=690/2, height=380)
        self.mainInputFrameLabel = Label(self.mainInputFrame, text="Input Maze", font=("Helvetica", 15, "bold"))
        self.mainInputFrameLabel.place(x = 40, y = 0)
        self.canvasInput = tk.Canvas(self.mainInputFrame, width=690/2, height=400)
        self.canvasInput.pack()
        self.canvasInput.bind("<Button-1>", self.fill_rectangle)
        self.canvasInput.bind("<B1-Motion>", self.fill_rectangle)
         

    def create_main_output_frame(self):
        self.mainOutputFrame = Frame(self.mainFrame, borderwidth=0, relief="groove")
        self.mainOutputFrame.place(x=395, y=50, width=345, height=380)
        self.canvasOutput = tk.Canvas(self.mainOutputFrame, width=345, height=380)
        self.canvasOutput.pack()
    
    def copy_input_to_output(self):
        for y in range(self.rows):
            for x in range(self.cols):
                color = self.color_matrix[y][x] if self.color_matrix[y][x] is not None else ""
                self.canvasOutput.create_rectangle(x*self.size, y*self.size, (x+1)*self.size, (y+1)*self.size, fill=color, outline="blue")

    def init_output_rectangle_grid(self):
        if self.rows is not None and self.cols is not None:
            self.output_rectangles = []
            if self.rows > self.cols:
                rect_width = 345 // self.rows
            else:
                rect_width = 345 // self.cols
            rect_size = rect_width
            for col in range(self.rows):
                y = col * rect_size
                row_rectangles = []
                for row in range(self.cols):
                    x = row * rect_size
                    rect = self.canvasOutput.create_rectangle(x, y, x + rect_size, y + rect_size, fill="", outline="blue")
                    row_rectangles.append(rect)
                self.output_rectangles.append(row_rectangles)

    def init_rectangle_grid(self):
        if self.rows is not None and self.cols is not None:
            self.rectangles = []
            if self.rows > self.cols:
                rect_width = 345 // self.rows
                rect_height = 345 // self.rows
            else:
                rect_width = 345 // self.cols
                rect_height = 345 // self.cols
            self.size = rect_width  # Assuming square rectangles for simplicity

            for col in range(self.cols):
                x = col * rect_width
                row_rectangles = []
                for row in range(self.rows):
                    y = row * rect_height
                    rect = self.canvasInput.create_rectangle(x, y, x + rect_width, y + rect_height, fill="", outline="blue")
                    row_rectangles.append(rect)
                self.rectangles.append(row_rectangles)
    def fill_rectangle(self, event):
        if self.rectangle_color is None:
            messagebox.showwarning("Warning", "Choose a color")
            return
        x, y = event.x // self.size, event.y // self.size
        if x < len(self.rectangles) and y < len(self.rectangles[0]):
            self.canvasInput.itemconfig(self.rectangles[x][y], fill=self.rectangle_color)
            self.color_matrix[y][x] = self.rectangle_color

    def add_color_frame_widgets(self):
        self.color_frame_label = Label(self.colorFrame, text="Color", font=("Helvetica", 15, "bold"))
        self.color_frame_label.place(x=175, y=0)

        self._init_toggle_button(25, 40, "#326ba8", self.colorFrame)
        self._init_toggle_button(140, 40, "#d91818", self.colorFrame)
        self._init_toggle_button(240, 40, "#05070f", self.colorFrame)
        self._init_toggle_button(340, 40, "#23a805", self.colorFrame)

    def _init_toggle_button(self, x, y, bg, parent, **kwargs):
        button = Button(parent, bg=bg, activebackground=bg, highlightthickness=0, **kwargs)
        button.is_active = False
        button.place(x=x, y=y, width=30, height=30)
        button.config(command=lambda: self._toggle_button_border(button))
        self.toggle_buttons.append(button)

    def _toggle_button_border(self, button):
        for btn in self.toggle_buttons:
            btn.config(borderwidth=2)
            btn.is_active = False
        button.config(highlightbackground="black", borderwidth=5)
        self.rectangle_color = button.cget('bg')
        button.is_active = True


if __name__ == "__main__":
    app = App()
