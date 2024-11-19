# JEU DE LA VIE 
# Avec l'aide de Perplexity I.A.
# J-P Perroud 20 juillet 2024

import  tkinter as tk
from    tkinter import ttk
import  random

class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.master.title("___|[ JEU DE LA VIE DE CONWAY ]|___")
        self.cell_size = 20
        self.width = 40
        self.height = 20
        self.grid = []
        self.running = False
        self.step_mode = False

        self.create_widgets()
        self.create_grid()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.width*self.cell_size, 
                                height=self.height*self.cell_size, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.toggle_cell)

        control_frame = ttk.Frame(self.master)
        control_frame.pack(pady=10)

        ttk.Button(control_frame, text="Start", command=self.start).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Stop", command=self.stop).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Step", command=self.step).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Run", command=self.run).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Clear", command=self.clear).grid(row=0, column=4, padx=5)
        ttk.Button(control_frame, text="Random", command=self.randomize).grid(row=0, column=5, padx=5)

        ttk.Label(control_frame, text="Width:").grid(row=1, column=0, padx=5, pady=5)
        self.width_entry = ttk.Entry(control_frame, width=5)
        self.width_entry.grid(row=1, column=1, padx=5, pady=5)
        self.width_entry.insert(0, str(self.width))

        ttk.Label(control_frame, text="Height:").grid(row=1, column=2, padx=5, pady=5)
        self.height_entry = ttk.Entry(control_frame, width=5)
        self.height_entry.grid(row=1, column=3, padx=5, pady=5)
        self.height_entry.insert(0, str(self.height))

        ttk.Button(control_frame, text="Resize", command=self.resize_grid).grid(row=1, column=4, padx=5, pady=5)

    def create_grid(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.canvas.delete("all")
        self.canvas.config(width=self.width*self.cell_size, height=self.height*self.cell_size)
        for i in range(self.height):
            for j in range(self.width):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

    def toggle_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = 1 - self.grid[row][col]
            color = "black" if self.grid[row][col] else "white"
            self.canvas.create_rectangle(col*self.cell_size, row*self.cell_size, 
                                         (col+1)*self.cell_size, (row+1)*self.cell_size, 
                                         fill=color, outline="gray")

    def resize_grid(self):
        try:
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())
            if new_width > 0 and new_height > 0:
                self.width = new_width
                self.height = new_height
                self.create_grid()
            else:
                raise ValueError("Width and height must be positive integers")
        except ValueError as e:
            tk.messagebox.showerror("Invalid Input", str(e))

    def start(self):
        if not self.running:
            self.running = True
            self.step_mode = False
            self.update()

    def stop(self):
        self.running = False
        self.step_mode = False

    def step(self):
        self.running = False
        self.step_mode = True
        self.update()

    def run(self):
        self.running = True
        self.step_mode = False
        self.update()

    def clear(self):
        self.stop()
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.update_canvas()

    def randomize(self):
        self.stop()
        self.grid = [[random.choice([0, 1]) for _ in range(self.width)] for _ in range(self.height)]
        self.update_canvas()

    def update(self):
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j]:
                    if neighbors in [2, 3]:
                        new_grid[i][j] = 1
                elif neighbors == 3:
                    new_grid[i][j] = 1
        self.grid = new_grid
        self.update_canvas()
        
        if self.running and not self.step_mode:
            self.master.after(100, self.update)

    def count_neighbors(self, row, col):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r = (row + i) % self.height
                c = (col + j) % self.width
                count += self.grid[r][c]
        return count

    def update_canvas(self):
        self.canvas.delete("all")
        for i in range(self.height):
            for j in range(self.width):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "black" if self.grid[i][j] else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()
