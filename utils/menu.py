"""Menu system for game selection with cursor navigation"""
import curses
import subprocess
import sys

GAMES = [
    {"id": 1, "name": "Breakout (打磚塊)", "file": "game_001_breakout"},
    {"id": 2, "name": "Snake (貪吃蛇)", "file": "game_002_snake"},
    {"id": 3, "name": "Pong (乒乓球)", "file": "game_003_pong"},
    {"id": 4, "name": "Space Invaders (太空侵略者)", "file": "game_004_space_invaders"},
    {"id": 5, "name": "Tetris (俄羅斯方塊)", "file": "game_005_tetris"},
    {"id": 6, "name": "Pac-Man (小精靈)", "file": "game_006_pacman"},
    {"id": 7, "name": "2048 (數字合併)", "file": "game_007_2048"},
    {"id": 8, "name": "Minesweeper (踩地雷)", "file": "game_008_minesweeper"},
    {"id": 9, "name": "Wordle (猜單字)", "file": "game_009_wordle"},
    {"id": 10, "name": "Sokoban (推箱子)", "file": "game_010_sokoban"},
]

def draw_menu(stdscr, selected_idx, redraw_all=False):
    """Draw the menu with cursor selection"""
    h, w = stdscr.getmaxyx()
    
    if redraw_all:
        stdscr.clear()
        # Header
        title = "🎮 10 CLI GAMES COLLECTION 🎮"
        subtitle = "Quality over Quantity!"
        
        try:
            stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD)
            stdscr.addstr(3, (w - len(subtitle)) // 2, subtitle)
            
            # Progress
            progress = f"Progress: 10/10 Games (100%) 🎉"
            stdscr.addstr(4, (w - len(progress)) // 2, progress)
            
            # Separator
            stdscr.addstr(5, 2, "─" * (w - 4))
            
            # Footer instructions
            instructions = "↑↓ Navigate | ENTER Select | Q Quit"
            stdscr.addstr(h - 2, (w - len(instructions)) // 2, instructions, curses.A_DIM)
        except curses.error:
            pass
    
    # Games list - always redraw
    start_y = 7
    try:
        for idx, game in enumerate(GAMES):
            y = start_y + idx
            if y >= h - 4:
                break
            
            # Format game line
            game_line = f" {game['id']:2d}. {game['name']}"
            
            # Highlight selected item
            if idx == selected_idx:
                stdscr.addstr(y, 4, "▶", curses.A_BOLD)
                stdscr.addstr(y, 6, game_line, curses.A_REVERSE | curses.A_BOLD)
            else:
                stdscr.addstr(y, 4, " ")
                stdscr.addstr(y, 6, game_line)
    except curses.error:
        pass
    
    stdscr.refresh()

def run_game(game):
    """Run the selected game"""
    try:
        # Run the game in a subprocess
        subprocess.run([sys.executable, f"games/{game['file']}.py"])
        return True
    except FileNotFoundError:
        return False
    except Exception:
        return False

def main_menu(stdscr):
    """Main menu loop with cursor navigation"""
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(0)  # Wait for input (prevent flickering)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    selected_idx = 0
    total_games = len(GAMES)
    
    # Initial full draw
    draw_menu(stdscr, selected_idx, redraw_all=True)
    
    while True:
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            # Wrap around: from first to last
            selected_idx = (selected_idx - 1) % total_games
            draw_menu(stdscr, selected_idx)
        elif key == curses.KEY_DOWN:
            # Wrap around: from last to first
            selected_idx = (selected_idx + 1) % total_games
            draw_menu(stdscr, selected_idx)
        elif key == ord('\n') or key == ord(' '):
            # Enter pressed - run game
            game = GAMES[selected_idx]
            curses.endwin()  # Restore terminal
            run_game(game)
            stdscr = curses.initscr()  # Reinitialize
            curses.curs_set(0)
            stdscr.nodelay(0)
            draw_menu(stdscr, selected_idx, redraw_all=True)
        elif key == ord('q') or key == ord('Q'):
            break

def show_menu():
    """Entry point for the menu system"""
    try:
        curses.wrapper(main_menu)
    except KeyboardInterrupt:
        pass
