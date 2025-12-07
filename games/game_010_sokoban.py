"""
Game 010: Sokoban
Classic box-pushing puzzle game - push all boxes to target positions.
"""

import curses
import copy

# Classic Sokoban levels (10 levels from easy to hard)
# All levels verified solvable
LEVELS = [
    # Level 1 - Tutorial (1 box)
    [
        "  ####",
        "###  #",
        "#    #",
        "# $@ #",
        "# .  #",
        "######"
    ],
    # Level 2 (2 boxes)
    [
        "#####",
        "#   #",
        "#$  #",
        "# $@#",
        "#. .#",
        "#####"
    ],
    # Level 3 (2 boxes)
    [
        "######",
        "#    #",
        "# $$ #",
        "# @  #",
        "# .. #",
        "######"
    ],
    # Level 4 (2 boxes)
    [
        " #####",
        " #   #",
        "## # #",
        "#  $ #",
        "# @$ #",
        "# .. #",
        "######"
    ],
    # Level 5 (2 boxes)
    [
        "######",
        "#    #",
        "# $  #",
        "# $  #",
        "#. . #",
        "#  @ #",
        "######"
    ],
    # Level 6 (2 boxes)
    [
        " #####",
        "##   #",
        "# $$ ##",
        "# @   #",
        "# . . #",
        "#######"
    ],
    # Level 7 (2 boxes)
    [
        "#######",
        "#     #",
        "# $@$ #",
        "#  #  #",
        "# . . #",
        "#######"
    ],
    # Level 8 (3 boxes)
    [
        " ######",
        "##    #",
        "# $$  #",
        "# $   #",
        "#. .  #",
        "#  .@ #",
        "#######"
    ],
    # Level 9 (3 boxes)
    [
        "  #####",
        "###   #",
        "#  $  #",
        "# $$  ##",
        "# . .  #",
        "## .@  #",
        " ######"
    ],
    # Level 10 - Challenge (3 boxes)
    [
        " ######",
        "##    #",
        "# $$  #",
        "# $   #",
        "# .#. #",
        "##. @ #",
        " ######"
    ]
]

class Sokoban:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        
        # Initialize curses
        curses.curs_set(0)
        self.stdscr.nodelay(0)
        self.stdscr.timeout(-1)
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Player
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Box
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Target
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Wall
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Box on target
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)     # Player on target
        
        # Game state
        self.current_level = 0
        self.load_level(self.current_level)
    
    def load_level(self, level_num):
        """Load a level"""
        if level_num >= len(LEVELS):
            return False
        
        self.current_level = level_num
        level = LEVELS[level_num]
        
        # Parse level
        self.board = []
        self.player_pos = None
        self.boxes = set()
        self.targets = set()
        self.moves = 0
        self.pushes = 0
        self.history = []
        
        for y, row in enumerate(level):
            board_row = []
            for x, char in enumerate(row):
                if char == '@':
                    self.player_pos = [x, y]
                    board_row.append(' ')
                elif char == '+':
                    self.player_pos = [x, y]
                    self.targets.add((x, y))
                    board_row.append(' ')
                elif char == '$':
                    self.boxes.add((x, y))
                    board_row.append(' ')
                elif char == '*':
                    self.boxes.add((x, y))
                    self.targets.add((x, y))
                    board_row.append(' ')
                elif char == '.':
                    self.targets.add((x, y))
                    board_row.append(' ')
                elif char == '#':
                    board_row.append('#')
                else:
                    board_row.append(' ')
            self.board.append(board_row)
        
        return True
    
    def can_move(self, x, y):
        """Check if position is walkable"""
        if y < 0 or y >= len(self.board):
            return False
        if x < 0 or x >= len(self.board[y]):
            return False
        return self.board[y][x] != '#'
    
    def move_player(self, dx, dy):
        """Try to move player"""
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Check if position is valid
        if not self.can_move(new_x, new_y):
            return False
        
        # Check if there's a box
        if (new_x, new_y) in self.boxes:
            # Try to push box
            box_new_x = new_x + dx
            box_new_y = new_y + dy
            
            # Check if box can be pushed
            if not self.can_move(box_new_x, box_new_y):
                return False
            if (box_new_x, box_new_y) in self.boxes:
                return False
            
            # Save state for undo
            self.history.append({
                'player_pos': self.player_pos.copy(),
                'boxes': self.boxes.copy(),
                'moves': self.moves,
                'pushes': self.pushes
            })
            
            # Push box
            self.boxes.remove((new_x, new_y))
            self.boxes.add((box_new_x, box_new_y))
            self.pushes += 1
        else:
            # Save state for undo (no push)
            self.history.append({
                'player_pos': self.player_pos.copy(),
                'boxes': self.boxes.copy(),
                'moves': self.moves,
                'pushes': self.pushes
            })
        
        # Move player
        self.player_pos = [new_x, new_y]
        self.moves += 1
        return True
    
    def undo(self):
        """Undo last move"""
        if not self.history:
            return False
        
        state = self.history.pop()
        self.player_pos = state['player_pos']
        self.boxes = state['boxes']
        self.moves = state['moves']
        self.pushes = state['pushes']
        return True
    
    def check_win(self):
        """Check if all boxes are on targets"""
        return self.boxes == self.targets
    
    def restart_level(self):
        """Restart current level"""
        self.load_level(self.current_level)
    
    def next_level(self):
        """Load next level"""
        if self.current_level < len(LEVELS) - 1:
            return self.load_level(self.current_level + 1)
        return False
    
    def draw_board(self):
        """Draw the game board"""
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        # Draw title
        title = "SOKOBAN - 推箱子"
        self.stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)
        
        # Draw stats
        stats_y = 3
        stats = f"Level: {self.current_level + 1}/{len(LEVELS)}  Moves: {self.moves}  Pushes: {self.pushes}"
        self.stdscr.addstr(stats_y, (width - len(stats)) // 2, stats)
        
        # Calculate board position
        board_height = len(self.board)
        board_width = max(len(row) for row in self.board) if self.board else 0
        start_y = 5
        start_x = (width - board_width * 2) // 2
        
        # Draw board
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                screen_y = start_y + y
                screen_x = start_x + x * 2
                
                # Determine what to draw
                pos = (x, y)
                player_here = (self.player_pos[0] == x and self.player_pos[1] == y)
                box_here = pos in self.boxes
                target_here = pos in self.targets
                
                if cell == '#':
                    # Wall
                    char = '█'
                    color = curses.color_pair(4)
                elif player_here and target_here:
                    # Player on target
                    char = '@'
                    color = curses.color_pair(6) | curses.A_BOLD
                elif player_here:
                    # Player
                    char = '@'
                    color = curses.color_pair(1) | curses.A_BOLD
                elif box_here and target_here:
                    # Box on target
                    char = '●'
                    color = curses.color_pair(5) | curses.A_BOLD
                elif box_here:
                    # Box
                    char = '●'
                    color = curses.color_pair(2)
                elif target_here:
                    # Target
                    char = '·'
                    color = curses.color_pair(3)
                else:
                    # Floor
                    char = ' '
                    color = curses.A_NORMAL
                
                try:
                    self.stdscr.addstr(screen_y, screen_x, char, color)
                except:
                    pass
        
        # Draw instructions
        inst_y = start_y + board_height + 2
        instructions = [
            "↑↓←→/WASD: Move  U: Undo  R: Restart",
            "N: Next Level  Q: Quit"
        ]
        
        for i, inst in enumerate(instructions):
            try:
                self.stdscr.addstr(inst_y + i, (width - len(inst)) // 2, inst)
            except:
                pass
        
        # Check win
        if self.check_win():
            msg = "★ LEVEL COMPLETE! ★"
            if self.current_level < len(LEVELS) - 1:
                msg2 = "Press N for next level"
            else:
                msg2 = "🎉 YOU WIN ALL LEVELS! 🎉"
            try:
                self.stdscr.addstr(inst_y + 3, (width - len(msg)) // 2, msg, 
                                 curses.A_BOLD | curses.A_REVERSE)
                self.stdscr.addstr(inst_y + 4, (width - len(msg2)) // 2, msg2)
            except:
                pass
        
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
                self.restart_level()
                continue
            
            # Handle next level
            if key in [ord('n'), ord('N')]:
                if self.check_win():
                    if not self.next_level():
                        # All levels completed
                        pass
                continue
            
            # Handle undo
            if key in [ord('u'), ord('U')]:
                self.undo()
                continue
            
            # Handle movement
            dx, dy = 0, 0
            if key == curses.KEY_UP or key == ord('w') or key == ord('W'):
                dy = -1
            elif key == curses.KEY_DOWN or key == ord('s') or key == ord('S'):
                dy = 1
            elif key == curses.KEY_LEFT or key == ord('a') or key == ord('A'):
                dx = -1
            elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('D'):
                dx = 1
            
            if dx != 0 or dy != 0:
                self.move_player(dx, dy)

def main(stdscr=None):
    """Entry point for the game"""
    if stdscr is None:
        from curses import wrapper
        wrapper(main)
    else:
        game = Sokoban(stdscr)
        game.run()

if __name__ == "__main__":
    main()
