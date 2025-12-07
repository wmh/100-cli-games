"""
Game 008: Minesweeper
Classic logic puzzle game - find all mines without stepping on them.
"""

import curses
import random
import time

class Minesweeper:
    def __init__(self, stdscr, width=10, height=10, mines=15):
        self.stdscr = stdscr
        self.width = width
        self.height = height
        self.mines_count = mines
        
        # Initialize curses
        curses.curs_set(0)
        self.stdscr.nodelay(0)
        self.stdscr.timeout(-1)
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)    # 1
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # 2
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # 3
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)    # 4
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)     # 5
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)    # 6
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLACK)   # 7
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)   # 8
        curses.init_pair(9, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Flag
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)    # Mine
        curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_BLUE)   # Cursor
        
        # Initialize game
        self.reset_game()
    
    def reset_game(self):
        """Reset the game state"""
        # Game state
        self.board = [[False] * self.width for _ in range(self.height)]
        self.revealed = [[False] * self.width for _ in range(self.height)]
        self.flags = [[False] * self.width for _ in range(self.height)]
        self.numbers = [[0] * self.width for _ in range(self.height)]
        
        self.game_over = False
        self.won = False
        self.first_click = True
        self.start_time = None
        
        # Cursor position
        self.cursor_x = self.width // 2
        self.cursor_y = self.height // 2
    
    def generate_mines(self, avoid_x, avoid_y):
        """Generate mines, avoiding first click position"""
        positions = [(x, y) for x in range(self.width) 
                     for y in range(self.height)
                     if (x, y) != (avoid_x, avoid_y)]
        
        mine_positions = random.sample(positions, self.mines_count)
        
        for x, y in mine_positions:
            self.board[y][x] = True
        
        # Calculate numbers
        self.calculate_numbers()
    
    def calculate_numbers(self):
        """Calculate number of adjacent mines for each cell"""
        for y in range(self.height):
            for x in range(self.width):
                if not self.board[y][x]:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:
                                continue
                            ny, nx = y + dy, x + dx
                            if (0 <= ny < self.height and 
                                0 <= nx < self.width and 
                                self.board[ny][nx]):
                                count += 1
                    self.numbers[y][x] = count
    
    def reveal(self, x, y):
        """Reveal a cell, flood fill if it's 0"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        
        if self.revealed[y][x] or self.flags[y][x]:
            return
        
        self.revealed[y][x] = True
        
        # Hit a mine
        if self.board[y][x]:
            self.game_over = True
            return
        
        # If no adjacent mines, reveal neighbors
        if self.numbers[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    self.reveal(x + dx, y + dy)
    
    def toggle_flag(self, x, y):
        """Toggle flag on a cell"""
        if not self.revealed[y][x]:
            self.flags[y][x] = not self.flags[y][x]
    
    def count_flags(self):
        """Count total flags placed"""
        return sum(sum(row) for row in self.flags)
    
    def check_win(self):
        """Check if player has won"""
        for y in range(self.height):
            for x in range(self.width):
                # If non-mine cell not revealed
                if not self.board[y][x] and not self.revealed[y][x]:
                    return False
        return True
    
    def get_elapsed_time(self):
        """Get elapsed time in seconds"""
        if self.start_time is None:
            return 0
        return int(time.time() - self.start_time)
    
    def draw_board(self):
        """Draw the game board"""
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        # Draw title
        title = "MINESWEEPER - 踩地雷"
        self.stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)
        
        # Draw stats
        stats_y = 3
        mines_left = self.mines_count - self.count_flags()
        elapsed = self.get_elapsed_time()
        
        stats_line = f"Mines: {self.mines_count}  Flags: {self.count_flags()}  Time: {elapsed}s"
        self.stdscr.addstr(stats_y, (width - len(stats_line)) // 2, stats_line)
        
        # Calculate board position (4 chars width per cell for better ratio)
        board_start_y = 5
        cell_width = 4
        board_start_x = (width - self.width * cell_width) // 2
        
        # Draw board
        for y in range(self.height):
            row_y = board_start_y + y
            for x in range(self.width):
                col_x = board_start_x + x * cell_width
                
                # Determine what to display
                is_cursor = (x == self.cursor_x and y == self.cursor_y)
                
                if self.game_over and self.board[y][x]:
                    # Show all mines when game over
                    char = ' * ' if self.revealed[y][x] else ' * '
                    color = curses.color_pair(10)
                elif self.revealed[y][x]:
                    # Revealed cell
                    if self.numbers[y][x] == 0:
                        char = '   '
                        color = curses.A_NORMAL
                    else:
                        char = f' {self.numbers[y][x]} '
                        color = curses.color_pair(self.numbers[y][x])
                elif self.flags[y][x]:
                    # Flagged cell
                    char = ' ⚑ '
                    color = curses.color_pair(9)
                else:
                    # Hidden cell
                    char = ' ░ '
                    color = curses.A_NORMAL
                
                # Apply cursor highlight
                if is_cursor and not self.game_over and not self.won:
                    color |= curses.A_REVERSE
                
                try:
                    self.stdscr.addstr(row_y, col_x, char, color)
                except:
                    pass
        
        # Draw instructions
        instructions_y = board_start_y + self.height + 2
        instructions = [
            "↑↓←→: Move  SPACE: Reveal",
            "F: Flag  R: Restart  Q: Quit"
        ]
        
        for i, inst in enumerate(instructions):
            self.stdscr.addstr(instructions_y + i, (width - len(inst)) // 2, inst)
        
        # Draw game status
        if self.won:
            msg = f"★ YOU WIN! Time: {elapsed}s ★"
            msg_y = board_start_y + self.height // 2
            msg_x = (width - len(msg)) // 2
            self.stdscr.addstr(msg_y, msg_x, msg, curses.A_BOLD | curses.A_REVERSE)
        elif self.game_over:
            msg = "💥 GAME OVER! Press R to restart 💥"
            msg_y = board_start_y + self.height // 2
            msg_x = (width - len(msg)) // 2
            self.stdscr.addstr(msg_y, msg_x, msg, curses.A_BOLD | curses.A_REVERSE)
        
        self.stdscr.refresh()
    
    def run(self):
        """Main game loop"""
        while True:
            self.draw_board()
            
            # Get input
            try:
                key = self.stdscr.getch()
            except:
                continue
            
            # Handle quit
            if key in [ord('q'), ord('Q')]:
                break
            
            # Handle restart
            if key in [ord('r'), ord('R')]:
                self.reset_game()
                continue
            
            # Don't allow moves if game is over
            if self.game_over or self.won:
                continue
            
            # Handle movement
            if key == curses.KEY_UP and self.cursor_y > 0:
                self.cursor_y -= 1
            elif key == curses.KEY_DOWN and self.cursor_y < self.height - 1:
                self.cursor_y += 1
            elif key == curses.KEY_LEFT and self.cursor_x > 0:
                self.cursor_x -= 1
            elif key == curses.KEY_RIGHT and self.cursor_x < self.width - 1:
                self.cursor_x += 1
            
            # Handle reveal
            elif key == ord(' '):
                # First click - generate mines
                if self.first_click:
                    self.generate_mines(self.cursor_x, self.cursor_y)
                    self.first_click = False
                    self.start_time = time.time()
                
                self.reveal(self.cursor_x, self.cursor_y)
                
                # Check win
                if self.check_win():
                    self.won = True
            
            # Handle flag
            elif key in [ord('f'), ord('F')]:
                self.toggle_flag(self.cursor_x, self.cursor_y)

def show_difficulty_menu(stdscr):
    """Show difficulty selection menu"""
    difficulties = [
        ("Easy (8x8, 10 mines)", 8, 8, 10),
        ("Medium (10x10, 15 mines)", 10, 10, 15),
        ("Hard (16x16, 40 mines)", 16, 16, 40),
    ]
    
    selected = 0
    
    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        
        title = "MINESWEEPER - Select Difficulty"
        stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD)
        
        start_y = 5
        for i, (name, _, _, _) in enumerate(difficulties):
            y = start_y + i * 2
            if i == selected:
                stdscr.addstr(y, (w - len(name)) // 2 - 2, "▶ " + name, curses.A_REVERSE)
            else:
                stdscr.addstr(y, (w - len(name)) // 2, name)
        
        instructions = "↑↓: Select  ENTER: Start  Q: Quit"
        stdscr.addstr(h - 2, (w - len(instructions)) // 2, instructions)
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(difficulties) - 1:
            selected += 1
        elif key == ord('\n'):
            return difficulties[selected][1:]  # Return (width, height, mines)
        elif key in [ord('q'), ord('Q')]:
            return None

def main(stdscr=None):
    """Entry point for the game"""
    if stdscr is None:
        from curses import wrapper
        wrapper(main)
    else:
        # Show difficulty menu
        difficulty = show_difficulty_menu(stdscr)
        if difficulty is None:
            return
        
        width, height, mines = difficulty
        game = Minesweeper(stdscr, width, height, mines)
        game.run()

if __name__ == "__main__":
    main()
