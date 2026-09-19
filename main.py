import tkinter as tk
import random

# Game Settings
GRID_SIZE = 8
CELL_SIZE = 50
BOARD_MARGIN = 20
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 650

# Predefined Block Shapes (Matrix Coordinates)
SHAPES = [
    [(0, 0)],  # 1x1 Dot
    [(0, 0), (0, 1)],  # 1x2 Horizontal Line
    [(0, 0), (1, 0)],  # 2x1 Vertical Line
    [(0, 0), (0, 1), (0, 2)],  # 1x3 Horizontal Line
    [(0, 0), (1, 0), (2, 0)],  # 3x1 Vertical Line
    [(0, 0), (0, 1), (1, 0), (1, 1)],  # 2x2 Square
    [(0, 0), (1, 0), (1, 1)],  # L-shape small
    [(0, 0), (0, 1), (0, 2), (1, 2)],  # L-shape standard
]

COLORS = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33F3", "#33FFF0"]

class BlockBlastGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Block Blast")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg="#1e1e24")
        
        self.score = 0
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected_piece_index = None
        
        # Setup UI
        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 20, "bold"), fg="white", bg="#1e1e24")
        self.score_label.pack(pady=10)
        
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=420, bg="#1e1e24", highlightthickness=0)
        self.canvas.pack()
        
        # Spawn Initial Pieces
        self.available_pieces = []
        self.spawn_pieces()
        
        # Event Bindings
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        self.draw_game()

    def spawn_pieces(self):
        """Generates 3 new pieces for the player."""
        self.available_pieces = []
        for _ in range(3):
            shape = random.choice(SHAPES)
            color = random.choice(COLORS)
            self.available_pieces.append({"shape": shape, "color": color})

    def draw_game(self):
        self.canvas.delete("all")
        
        # 1. Draw Board Grid
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1 = BOARD_MARGIN + c * CELL_SIZE
                y1 = BOARD_MARGIN + r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                # Check if cell is filled
                if self.grid[r][c] != 0:
                    fill_color = self.grid[r][c]
                else:
                    fill_color = "#2e2e38"
                    
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="#1e1e24", width=2)
        
        # 2. Draw Available Pieces Tray (At the bottom)
        tray_y = BOARD_MARGIN + (GRID_SIZE * CELL_SIZE) + 30
        for idx, piece in enumerate(self.available_pieces):
            if piece is None:
                continue
            
            # Highlight selected piece
            outline_color = "white" if idx == self.selected_piece_index else "#1e1e24"
            
            # Position offset for each of the 3 pieces
            offset_x = 40 + idx * 150
            
            # Draw individual blocks inside the piece
            for pr, pc in piece["shape"]:
                x1 = offset_x + pc * 25
                y1 = tray_y + pr * 25
                x2 = x1 + 25
                y2 = y1 + 25
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=piece["color"], outline=outline_color, tags=f"piece_{idx}")

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        tray_y = BOARD_MARGIN + (GRID_SIZE * CELL_SIZE) + 30
        
        # Check if clicking on the pieces tray
        if y >= tray_y:
            for idx in range(3):
                offset_x = 40 + idx * 150
                if offset_x <= x <= offset_x + 100:
                    if idx < len(self.available_pieces) and self.available_pieces[idx] is not None:
                        self.selected_piece_index = idx
                        self.draw_game()
            return

        # Check if clicking on the board while a piece is selected
        if self.selected_piece_index is not None:
            # Convert screen click to grid row/col
            col = int((x - BOARD_MARGIN) // CELL_SIZE)
            row = int((y - BOARD_MARGIN) // CELL_SIZE)
            
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                piece = self.available_pieces[self.selected_piece_index]
                
                if self.can_place_piece(row, col, piece["shape"]):
                    self.place_piece(row, col, piece)
                    self.available_pieces[self.selected_piece_index] = None
                    self.selected_piece_index = None
                    
                    # Clear lines and score
                    self.check_and_clear_lines()
                    
                    # If all 3 pieces are used, spawn a new set
                    if all(p is None for p in self.available_pieces):
                        self.spawn_pieces()
                        
                    self.draw_game()
                    
                    if self.check_game_over():
                        self.game_over_popup()

    def can_place_piece(self, row, col, shape):
        """Checks if a piece fits on the board without overlapping or going out of bounds."""
        for pr, pc in shape:
            target_r = row + pr
            target_c = col + pc
            if target_r >= GRID_SIZE or target_c >= GRID_SIZE:
                return False
            if self.grid[target_r][target_c] != 0:
                return False
        return True

    def place_piece(self, row, col, piece):
        for pr, pc in piece["shape"]:
            self.grid[row + pr][col + pc] = piece["color"]
        self.score += len(piece["shape"]) * 10
        self.score_label.config(text=f"Score: {self.score}")

    def check_and_clear_lines(self):
        """Checks all rows and columns to find full lines, then blasts them."""
        rows_to_clear = [r for r in range(GRID_SIZE) if all(self.grid[r][c] != 0 for c in range(GRID_SIZE))]
        cols_to_clear = [c for c in range(GRID_SIZE) if all(self.grid[r][c] != 0 for r in range(GRID_SIZE))]
        
        # Clear identified items
        for r in rows_to_clear:
            for c in range(GRID_SIZE):
                self.grid[r][c] = 0
        for c in cols_to_clear:
            for r in range(GRID_SIZE):
                self.grid[r][c] = 0
                
        # Award bonus points for clearing lines
        cleared_lines = len(rows_to_clear) + len(cols_to_clear)
        if cleared_lines > 0:
            self.score += cleared_lines * 100
            self.score_label.config(text=f"Score: {self.score}")

    def check_game_over(self):
        """Returns True if none of the remaining pieces can fit anywhere on the board."""
        for piece in self.available_pieces:
            if piece is None:
                continue
            # Try placing this piece in every single grid slot
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if self.can_place_piece(r, c, piece["shape"]):
                        return False
        return True

    def game_over_popup(self):
        top = tk.Toplevel(self.root)
        top.title("Game Over")
        top.geometry("250x150")
        top.configure(bg="#1e1e24")
        
        label = tk.Label(top, text=f"Game Over!\nFinal Score: {self.score}", font=("Helvetica", 14), fg="white", bg="#1e1e24")
        label.pack(pady=20)
        
        btn = tk.Button(top, text="Restart", command=lambda: [top.destroy(), self.reset_game()], font=("Helvetica", 12), bg="#FF5733", fg="white")
        btn.pack()

    def reset_game(self):
        self.score = 0
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.selected_piece_index = None
        self.score_label.config(text="Score: 0")
        self.spawn_pieces()
        self.draw_game()

if __name__ == "__main__":
    window = tk.Tk()
    game = BlockBlastGame(window)
    window.mainloop()
