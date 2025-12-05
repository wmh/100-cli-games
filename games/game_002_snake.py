"""
Game 002: Snake (貪吃蛇)
Classic snake game with smooth curses rendering
"""
import curses
import time
import random
from collections import deque

class Snake:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.width = 60
        self.height = 25
        
        # Snake starts in center, moving right
        start_x = self.width // 2
        start_y = self.height // 2
        self.snake = deque([(start_x, start_y), (start_x-1, start_y), (start_x-2, start_y)])
        
        self.direction = (1, 0)  # (dx, dy) - moving right
        self.next_direction = (1, 0)
        
        self.food = None
        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.game_over = False
        self.paused = False
        self.running = True
        
        self.base_speed = 0.15
        self.speed = self.base_speed
        
        self.init_curses()
        self.spawn_food()
        self.draw_static()
    
    def init_curses(self):
        """Initialize curses settings"""
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(0)
        
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Snake
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Food
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Head
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Border
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Text
    
    def draw_static(self):
        """Draw static border"""
        try:
            self.stdscr.clear()
            
            # Draw border
            self.stdscr.addstr(0, 0, '╔' + '═' * (self.width - 2) + '╗', 
                             curses.color_pair(4))
            for y in range(1, self.height - 1):
                self.stdscr.addstr(y, 0, '║', curses.color_pair(4))
                self.stdscr.addstr(y, self.width - 1, '║', curses.color_pair(4))
            self.stdscr.addstr(self.height - 1, 0, '╚' + '═' * (self.width - 2) + '╝',
                             curses.color_pair(4))
            
            self.stdscr.noutrefresh()
        except curses.error:
            pass
    
    def spawn_food(self):
        """Spawn food at random empty location"""
        while True:
            x = random.randint(2, self.width - 3)
            y = random.randint(2, self.height - 3)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def draw(self):
        """Draw game elements (incremental rendering)"""
        try:
            # Draw snake
            for i, (x, y) in enumerate(self.snake):
                if i == 0:  # Head
                    self.stdscr.addstr(y, x, '■', curses.color_pair(3) | curses.A_BOLD)
                else:  # Body
                    self.stdscr.addstr(y, x, '▓', curses.color_pair(1))
            
            # Draw food
            if self.food:
                fx, fy = self.food
                self.stdscr.addstr(fy, fx, '●', curses.color_pair(2) | curses.A_BOLD)
            
            # Draw status
            status = f" Score: {self.score}  Length: {len(self.snake)}  Level: {self.level}  "
            controls = "(↑↓←→ or WASD, Space=Pause, Q=Quit)"
            self.stdscr.addstr(self.height + 1, 0, status.ljust(self.width), curses.color_pair(5))
            
            if self.paused:
                msg = "*** PAUSED - Press Space to continue ***"
                msg_x = (self.width - len(msg)) // 2
                self.stdscr.addstr(self.height // 2, msg_x, msg, 
                                 curses.color_pair(3) | curses.A_BOLD)
            
            self.stdscr.noutrefresh()
            curses.doupdate()
            
        except curses.error:
            pass
    
    def handle_input(self):
        """Handle keyboard input"""
        key = self.stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            self.running = False
            return
        
        if key == ord(' '):
            self.paused = not self.paused
            return
        
        if self.paused:
            return
        
        # Direction changes (can't reverse)
        dx, dy = self.direction
        
        if key == curses.KEY_UP or key == ord('w') or key == ord('W'):
            if dy != 1:  # Not moving down
                self.next_direction = (0, -1)
        elif key == curses.KEY_DOWN or key == ord('s') or key == ord('S'):
            if dy != -1:  # Not moving up
                self.next_direction = (0, 1)
        elif key == curses.KEY_LEFT or key == ord('a') or key == ord('A'):
            if dx != 1:  # Not moving right
                self.next_direction = (-1, 0)
        elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('D'):
            if dx != -1:  # Not moving left
                self.next_direction = (1, 0)
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        nx, ny = new_head
        if nx <= 0 or nx >= self.width - 1 or ny <= 0 or ny >= self.height - 1:
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Erase tail before moving (for smooth animation)
        if self.snake:
            tail_x, tail_y = self.snake[-1]
            try:
                self.stdscr.addstr(tail_y, tail_x, ' ')
            except curses.error:
                pass
        
        # Check food collision
        if new_head == self.food:
            self.snake.appendleft(new_head)
            self.score += 10
            self.food_eaten += 1
            
            # Level up every 5 food
            if self.food_eaten % 5 == 0:
                self.level += 1
                self.speed = self.base_speed * (0.9 ** (self.level - 1))
            
            self.spawn_food()
        else:
            # Normal move (add head, remove tail)
            self.snake.appendleft(new_head)
            self.snake.pop()
    
    def run(self):
        """Main game loop"""
        last_update = time.time()
        
        while self.running:
            current_time = time.time()
            
            self.handle_input()
            
            # Update game at appropriate speed
            if not self.paused and current_time - last_update >= self.speed:
                self.update()
                last_update = current_time
            
            self.draw()
            
            if self.game_over:
                try:
                    msg_y = self.height // 2
                    self.stdscr.addstr(msg_y, self.width // 2 - 10,
                                     "🐍 GAME OVER! 🐍", 
                                     curses.color_pair(2) | curses.A_BOLD)
                    self.stdscr.addstr(msg_y + 2, self.width // 2 - 10,
                                     f"Final Score: {self.score}",
                                     curses.color_pair(5))
                    self.stdscr.addstr(msg_y + 3, self.width // 2 - 10,
                                     f"Length: {len(self.snake)}",
                                     curses.color_pair(5))
                    self.stdscr.addstr(msg_y + 5, self.width // 2 - 15,
                                     "Press any key...",
                                     curses.color_pair(5))
                    self.stdscr.refresh()
                except curses.error:
                    pass
                self.stdscr.nodelay(0)
                self.stdscr.getch()
                break
            
            time.sleep(0.01)  # Small delay to reduce CPU usage

def game_main(stdscr):
    """Main game function for curses wrapper"""
    game = Snake(stdscr)
    game.run()

def main():
    """Entry point"""
    try:
        curses.wrapper(game_main)
    except KeyboardInterrupt:
        pass
    
    print("\n🐍 SNAKE (貪吃蛇) 🐍")
    print("Press Enter to return to menu...")
    input()

if __name__ == "__main__":
    main()
