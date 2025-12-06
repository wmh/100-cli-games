"""
Game 006: Pac-Man
經典的 Pac-Man 迷宮追逐遊戲
控制: 方向鍵移動, P 暫停, Q 退出
"""

import curses
import time
import random
from collections import deque
from typing import List, Tuple, Optional

# 遊戲常數
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 30
FPS = 15  # 幀率
FRAME_TIME = 1.0 / FPS
PACMAN_MOVE_DELAY = 0.15  # Pac-Man 移動延遲（秒）
GHOST_MOVE_DELAY = 0.18  # 幽靈移動延遲（秒）

# 迷宮佈局（簡化版）
MAZE_LAYOUT = [
    "####################",
    "#........##........#",
    "#.##.###.##.###.##.#",
    "#O##.###.##.###.##O#",
    "#..................#",
    "#.##.#.######.#.##.#",
    "#....#...##...#....#",
    "####.###.##.###.####",
    "####.#..........####",
    "####.#.##--##.#.####",
    "####.#.#    #.#.####",
    "       # GG #       ",
    "####.#.#    #.#.####",
    "####.#.######.#.####",
    "####.#...##...#.####",
    "#........##........#",
    "#.##.###.##.###.##.#",
    "#O.#.....P.....#.O.#",
    "##.#.#.######.#.#.##",
    "#....#...##...#....#",
    "#.######.##.######.#",
    "#..................#",
    "####################"
]

# 方向常數
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0),
    'NONE': (0, 0)
}

# 能量豆效果持續時間
POWER_DURATION = 8.0
GHOST_EATEN_SCORES = [200, 400, 800, 1600]
GHOST_FRIGHTENED_DELAY = 0.25  # 幽靈逃跑時的移動延遲（變慢）


class PacMan:
    """Pac-Man 類別"""
    
    def __init__(self, x: int, y: int):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.direction = DIRECTIONS['NONE']
        self.next_direction = DIRECTIONS['NONE']
        self.move_timer = 0  # 移動計時器
    
    def set_next_direction(self, direction: Tuple[int, int]):
        """設定下一個移動方向"""
        self.next_direction = direction
    
    def can_move(self, dx: int, dy: int, maze) -> bool:
        """檢查是否可以移動到指定方向"""
        new_x = self.x + dx
        new_y = self.y + dy
        return maze.is_walkable(new_x, new_y)
    
    def move(self, maze, dt: float):
        """移動 Pac-Man"""
        self.move_timer += dt
        
        # 控制移動速度
        if self.move_timer < PACMAN_MOVE_DELAY:
            return
        
        self.move_timer = 0
        
        # 嘗試轉向
        if self.next_direction != DIRECTIONS['NONE']:
            if self.can_move(self.next_direction[0], self.next_direction[1], maze):
                self.direction = self.next_direction
        
        # 移動
        if self.direction != DIRECTIONS['NONE']:
            dx, dy = self.direction
            if self.can_move(dx, dy, maze):
                self.x += dx
                self.y += dy
                
                # 隧道傳送（左右邊界）
                if self.x < 0:
                    self.x = maze.width - 1
                elif self.x >= maze.width:
                    self.x = 0
    
    def get_char(self) -> str:
        """根據方向返回顯示字元"""
        if self.direction == DIRECTIONS['RIGHT']:
            return "C"  # 改用 ASCII
        elif self.direction == DIRECTIONS['LEFT']:
            return "C"
        elif self.direction == DIRECTIONS['UP']:
            return "C"
        elif self.direction == DIRECTIONS['DOWN']:
            return "C"
        return "C"
    
    def reset(self):
        """重置到起始位置"""
        self.x = self.start_x
        self.y = self.start_y
        self.direction = DIRECTIONS['NONE']
        self.next_direction = DIRECTIONS['NONE']
        self.move_timer = 0


class Ghost:
    """幽靈類別"""
    
    def __init__(self, name: str, color: int, home_x: int, home_y: int):
        self.name = name
        self.color = color
        self.home_x = home_x
        self.home_y = home_y
        self.x = home_x
        self.y = home_y
        self.direction = DIRECTIONS['UP']
        self.frightened = False
        self.eaten = False
        self.move_timer = 0
    
    def reset(self):
        """重置到起始位置"""
        self.x = self.home_x
        self.y = self.home_y
        self.direction = DIRECTIONS['UP']
        self.frightened = False
        self.eaten = False
    
    def update(self, pacman, maze, dt: float):
        """更新幽靈狀態"""
        self.move_timer += dt
        
        # 控制移動速度（逃跑時變慢）
        delay = GHOST_FRIGHTENED_DELAY if self.frightened else GHOST_MOVE_DELAY
        if self.move_timer < delay:
            return
        
        self.move_timer = 0
        
        if self.eaten:
            # 被吃掉，回家（快速）
            self.move_to_home(maze)
        elif self.frightened:
            # 逃跑模式（變慢）
            self.move_random(maze)
        else:
            # 追逐模式（正常速度）
            self.chase(pacman, maze)
    
    def chase(self, pacman, maze):
        """追逐 Pac-Man（改良版 AI）"""
        # 計算距離
        dx = pacman.x - self.x
        dy = pacman.y - self.y
        
        # 列出所有可能的移動方向
        all_directions = [
            DIRECTIONS['UP'],
            DIRECTIONS['DOWN'],
            DIRECTIONS['LEFT'],
            DIRECTIONS['RIGHT']
        ]
        
        # 計算每個方向移動後與 Pac-Man 的距離
        best_direction = None
        best_distance = float('inf')
        reverse_dir = (-self.direction[0], -self.direction[1])
        
        for direction in all_directions:
            move_dx, move_dy = direction
            new_x = self.x + move_dx
            new_y = self.y + move_dy
            
            # 隧道傳送處理
            if new_x < 0:
                new_x = maze.width - 1
            elif new_x >= maze.width:
                new_x = 0
            
            # 檢查是否可以移動
            if not maze.is_walkable(new_x, new_y):
                continue
            
            # 避免 180 度轉向（除非是唯一選擇）
            if direction == reverse_dir:
                continue
            
            # 計算移動後的距離
            distance = abs(pacman.x - new_x) + abs(pacman.y - new_y)
            
            if distance < best_distance:
                best_distance = distance
                best_direction = direction
        
        # 如果找到好的方向，就移動
        if best_direction:
            move_dx, move_dy = best_direction
            self.x += move_dx
            self.y += move_dy
            
            # 隧道傳送
            if self.x < 0:
                self.x = maze.width - 1
            elif self.x >= maze.width:
                self.x = 0
            
            self.direction = best_direction
            return
        
        # 如果沒有好的方向（可能需要 180 度轉向），就允許 180 度轉向
        for direction in all_directions:
            move_dx, move_dy = direction
            new_x = self.x + move_dx
            new_y = self.y + move_dy
            
            # 隧道傳送處理
            if new_x < 0:
                new_x = maze.width - 1
            elif new_x >= maze.width:
                new_x = 0
            
            if maze.is_walkable(new_x, new_y):
                self.x += move_dx
                self.y += move_dy
                
                # 隧道傳送
                if self.x < 0:
                    self.x = maze.width - 1
                elif self.x >= maze.width:
                    self.x = 0
                
                self.direction = direction
                return
    
    def move_random(self, maze):
        """隨機移動（逃跑模式）"""
        possible_moves = []
        
        for direction in [DIRECTIONS['UP'], DIRECTIONS['DOWN'], 
                         DIRECTIONS['LEFT'], DIRECTIONS['RIGHT']]:
            dx, dy = direction
            new_x = self.x + dx
            new_y = self.y + dy
            
            # 隧道傳送處理
            if new_x < 0:
                new_x = maze.width - 1
            elif new_x >= maze.width:
                new_x = 0
            
            if maze.is_walkable(new_x, new_y):
                # 避免 180 度轉向
                reverse_dir = (-self.direction[0], -self.direction[1])
                if direction != reverse_dir:
                    possible_moves.append(direction)
        
        if possible_moves:
            direction = random.choice(possible_moves)
            dx, dy = direction
            self.x += dx
            self.y += dy
            
            # 隧道傳送
            if self.x < 0:
                self.x = maze.width - 1
            elif self.x >= maze.width:
                self.x = 0
            
            self.direction = direction
    
    def move_to_home(self, maze):
        """回到起始位置"""
        if self.x == self.home_x and self.y == self.home_y:
            self.eaten = False
            self.frightened = False
            return
        
        # 簡單的回家邏輯
        dx = self.home_x - self.x
        dy = self.home_y - self.y
        
        if abs(dx) > abs(dy):
            if dx > 0 and maze.is_walkable(self.x + 1, self.y):
                self.x += 1
            elif dx < 0 and maze.is_walkable(self.x - 1, self.y):
                self.x -= 1
        else:
            if dy > 0 and maze.is_walkable(self.x, self.y + 1):
                self.y += 1
            elif dy < 0 and maze.is_walkable(self.x, self.y - 1):
                self.y -= 1
        
        # 隧道傳送
        if self.x < 0:
            self.x = maze.width - 1
        elif self.x >= maze.width:
            self.x = 0
    
    def get_char(self) -> str:
        """返回顯示字元"""
        if self.eaten:
            return "EE"  # 眼睛 (兩個字元)
        elif self.frightened:
            return "B"   # Blue ghost (可被吃)
        else:
            return "G"   # Ghost (正常幽靈)


class Maze:
    """迷宮類別"""
    
    def __init__(self, layout: List[str]):
        self.layout = [list(row) for row in layout]
        self.height = len(layout)
        self.width = len(layout[0]) if layout else 0
        self.dots_total = 0
        self.dots_remaining = 0
        self.power_pellets = []
        
        # 統計豆子和能量豆
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == '.':
                    self.dots_total += 1
                    self.dots_remaining += 1
                elif cell == 'O':
                    self.dots_total += 1
                    self.dots_remaining += 1
                    self.power_pellets.append((x, y))
    
    def get_cell(self, x: int, y: int) -> str:
        """獲取指定位置的格子內容"""
        # 處理隧道（水平方向）
        if x < 0:
            x = self.width - 1
        elif x >= self.width:
            x = 0
        
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.layout[y][x]
        return '#'
    
    def is_walkable(self, x: int, y: int) -> bool:
        """檢查是否可通行"""
        # 處理隧道（水平方向）
        if x < 0:
            x = self.width - 1
        elif x >= self.width:
            x = 0
        
        cell = self.get_cell(x, y)
        return cell != '#'
    
    def eat_dot(self, x: int, y: int) -> Tuple[int, bool]:
        """吃豆子，返回 (得分, 是否是能量豆)"""
        cell = self.get_cell(x, y)
        
        if cell == '.':
            self.layout[y][x] = ' '
            self.dots_remaining -= 1
            return (10, False)
        elif cell == 'O':
            self.layout[y][x] = ' '
            self.dots_remaining -= 1
            return (50, True)
        
        return (0, False)
    
    def is_level_complete(self) -> bool:
        """檢查關卡是否完成"""
        return self.dots_remaining == 0


class PacManGame:
    """Pac-Man 遊戲主類別"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_colors()
        
        # 初始化迷宮
        self.maze = Maze(MAZE_LAYOUT)
        
        # 找到 Pac-Man 和幽靈的起始位置
        pacman_pos = self.find_start_position('P')
        ghost_positions = self.find_ghost_positions('G')
        
        # 初始化 Pac-Man
        self.pacman = PacMan(pacman_pos[0], pacman_pos[1])
        
        # 初始化幽靈
        self.ghosts = [
            Ghost("Blinky", 1, ghost_positions[0][0], ghost_positions[0][1]),
            Ghost("Pinky", 2, ghost_positions[1][0], ghost_positions[1][1]),
            Ghost("Inky", 3, ghost_positions[2][0], ghost_positions[2][1]),
            Ghost("Clyde", 4, ghost_positions[3][0], ghost_positions[3][1])
        ]
        
        # 遊戲狀態
        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.level = 1
        self.power_mode = False
        self.power_timer = 0
        self.ghost_combo = 0
        self.game_over = False
        self.level_complete = False
        self.paused = False
        
        # 清除迷宮中的標記
        self.clear_markers()
    
    def setup_colors(self):
        """設定顏色"""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)     # Blinky
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Pinky
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Inky
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Clyde
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Pac-Man
        curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Frightened
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)   # UI
    
    def find_start_position(self, marker: str) -> Tuple[int, int]:
        """找到標記的起始位置"""
        for y, row in enumerate(self.maze.layout):
            for x, cell in enumerate(row):
                if cell == marker:
                    return (x, y)
        return (10, 10)  # 預設位置
    
    def find_ghost_positions(self, marker: str) -> List[Tuple[int, int]]:
        """找到所有幽靈起始位置"""
        positions = []
        for y, row in enumerate(self.maze.layout):
            for x, cell in enumerate(row):
                if cell == marker:
                    positions.append((x, y))
        
        # 確保有 4 個位置
        while len(positions) < 4:
            positions.append(positions[0] if positions else (10, 10))
        
        return positions[:4]
    
    def clear_markers(self):
        """清除迷宮中的 P 和 G 標記"""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.layout[y][x] in ['P', 'G']:
                    self.maze.layout[y][x] = ' '
    
    def handle_input(self) -> bool:
        """處理輸入"""
        key = self.stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            return False
        
        if key == ord('p') or key == ord('P'):
            self.paused = not self.paused
            return True
        
        if self.paused or self.game_over:
            return True
        
        # 方向控制
        if key == curses.KEY_UP:
            self.pacman.set_next_direction(DIRECTIONS['UP'])
        elif key == curses.KEY_DOWN:
            self.pacman.set_next_direction(DIRECTIONS['DOWN'])
        elif key == curses.KEY_LEFT:
            self.pacman.set_next_direction(DIRECTIONS['LEFT'])
        elif key == curses.KEY_RIGHT:
            self.pacman.set_next_direction(DIRECTIONS['RIGHT'])
        
        return True
    
    def update(self, dt: float):
        """更新遊戲狀態"""
        if self.paused or self.game_over or self.level_complete:
            return
        
        # 移動 Pac-Man
        self.pacman.move(self.maze, dt)
        
        # 吃豆子
        score_gain, is_power_pellet = self.maze.eat_dot(self.pacman.x, self.pacman.y)
        self.score += score_gain
        
        # 能量豆效果
        if is_power_pellet:
            self.power_mode = True
            self.power_timer = POWER_DURATION
            self.ghost_combo = 0
            
            # 所有幽靈進入逃跑模式
            for ghost in self.ghosts:
                if not ghost.eaten:
                    ghost.frightened = True
        
        # 更新能量模式計時器
        if self.power_mode:
            self.power_timer -= dt
            if self.power_timer <= 0:
                self.power_mode = False
                for ghost in self.ghosts:
                    ghost.frightened = False
        
        # 移動幽靈
        for ghost in self.ghosts:
            ghost.update(self.pacman, self.maze, dt)
        
        # 碰撞檢測
        self.check_collisions()
        
        # 檢查關卡完成
        if self.maze.is_level_complete():
            self.level_complete = True
        
        # 更新最高分
        if self.score > self.high_score:
            self.high_score = self.score
    
    def check_collisions(self):
        """檢查碰撞"""
        for ghost in self.ghosts:
            if ghost.x == self.pacman.x and ghost.y == self.pacman.y:
                if ghost.frightened and not ghost.eaten:
                    # 吃掉幽靈
                    ghost.eaten = True
                    ghost.frightened = False
                    self.score += GHOST_EATEN_SCORES[min(self.ghost_combo, 3)]
                    self.ghost_combo += 1
                elif not ghost.eaten:
                    # 被幽靈吃掉
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.reset_positions()
    
    def reset_positions(self):
        """重置所有位置"""
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()
        self.power_mode = False
        self.power_timer = 0
    
    def render(self):
        """渲染遊戲畫面"""
        self.stdscr.erase()
        
        # 繪製標題和狀態
        title = "PAC-MAN"
        self.stdscr.addstr(0, 2, title, curses.color_pair(7) | curses.A_BOLD)
        
        score_str = f"SCORE: {self.score:05d}"
        hi_str = f"HI: {self.high_score:05d}"
        lives_str = f"LIVES: {'●' * self.lives}"
        
        self.stdscr.addstr(0, 20, score_str, curses.color_pair(7))
        self.stdscr.addstr(0, 40, hi_str, curses.color_pair(7))
        self.stdscr.addstr(0, 58, lives_str, curses.color_pair(5))
        
        # 繪製迷宮（每格佔兩個字元寬）
        maze_start_x = 2
        maze_start_y = 2
        
        for y, row in enumerate(self.maze.layout):
            for x, cell in enumerate(row):
                screen_x = maze_start_x + x * 2  # 寬度加倍
                screen_y = maze_start_y + y
                
                if cell == '#':
                    self.stdscr.addstr(screen_y, screen_x, "██", curses.color_pair(6))
                elif cell == '.':
                    # 使用標準 ASCII 點號，放在中間
                    self.stdscr.addstr(screen_y, screen_x, " .", curses.color_pair(7))
                elif cell == 'O':
                    # 能量豆使用 o 或 O
                    self.stdscr.addstr(screen_y, screen_x, " o", curses.color_pair(7) | curses.A_BOLD)
                elif cell == '-':
                    self.stdscr.addstr(screen_y, screen_x, "--", curses.color_pair(7))
                else:
                    self.stdscr.addstr(screen_y, screen_x, "  ", curses.color_pair(7))
        
        # 繪製幽靈（使用標準 ASCII）
        for ghost in self.ghosts:
            screen_x = maze_start_x + ghost.x * 2
            screen_y = maze_start_y + ghost.y
            color = curses.color_pair(6) if ghost.frightened else curses.color_pair(ghost.color)
            char = ghost.get_char()
            
            if char == "EE":
                # 眼睛（兩個字元）
                self.stdscr.addstr(screen_y, screen_x, "EE", color | curses.A_BOLD)
            else:
                # G 或 B（一個字元，前面加空格）
                self.stdscr.addstr(screen_y, screen_x, f" {char}", color | curses.A_BOLD)
        
        # 繪製 Pac-Man（使用標準 ASCII）
        screen_x = maze_start_x + self.pacman.x * 2
        screen_y = maze_start_y + self.pacman.y
        pac_char = self.pacman.get_char()
        self.stdscr.addstr(screen_y, screen_x, f" {pac_char}", 
                          curses.color_pair(5) | curses.A_BOLD)
        
        # 繪製能量模式提示
        if self.power_mode:
            power_str = f"POWER! {int(self.power_timer)}s"
            self.stdscr.addstr(1, 30, power_str, curses.color_pair(6) | curses.A_BOLD)
        
        # 繪製控制說明
        controls = "Arrow keys: Move | P: Pause | Q: Quit"
        self.stdscr.addstr(SCREEN_HEIGHT - 1, 2, controls, curses.color_pair(7))
        
        # 遊戲狀態訊息
        if self.game_over:
            msg = "GAME OVER! Press Q to quit"
            self.stdscr.addstr(SCREEN_HEIGHT // 2, (SCREEN_WIDTH - len(msg)) // 2, msg,
                             curses.color_pair(1) | curses.A_BOLD)
        elif self.level_complete:
            msg = "LEVEL COMPLETE! Press Q to quit"
            self.stdscr.addstr(SCREEN_HEIGHT // 2, (SCREEN_WIDTH - len(msg)) // 2, msg,
                             curses.color_pair(5) | curses.A_BOLD)
        elif self.paused:
            msg = "PAUSED - Press P to continue"
            self.stdscr.addstr(SCREEN_HEIGHT // 2, (SCREEN_WIDTH - len(msg)) // 2, msg,
                             curses.color_pair(7) | curses.A_BOLD)
        
        self.stdscr.refresh()
    
    def run(self):
        """遊戲主迴圈"""
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.timeout(0)
        
        try:
            curses.cbreak()
            self.stdscr.keypad(True)
        except:
            pass
        
        last_time = time.time()
        
        while True:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # 處理輸入
            if not self.handle_input():
                break
            
            # 更新遊戲
            self.update(dt)
            
            # 渲染
            self.render()
            
            # 控制幀率
            elapsed = time.time() - current_time
            sleep_time = FRAME_TIME - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)


def main():
    """遊戲入口"""
    try:
        curses.wrapper(lambda stdscr: PacManGame(stdscr).run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
