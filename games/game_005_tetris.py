"""
Game 005: Tetris
經典的俄羅斯方塊益智遊戲
控制: ← → 移動, ↑ 旋轉, ↓ 軟下落, 空格 硬下落, C 暫存, P 暫停, Q 退出
"""

import curses
import time
import random
import copy
from typing import List, Tuple, Optional

# 遊戲常數
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 30
FPS = 30
FRAME_TIME = 1.0 / FPS

# 遊戲板設定
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_LEFT = 5
BOARD_TOP = 3

# 方塊形狀定義 (旋轉狀態)
SHAPES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    'O': [
        [[1, 1], [1, 1]]
    ],
    'T': [
        [[0, 1, 0], [1, 1, 1]],
        [[1, 0], [1, 1], [1, 0]],
        [[1, 1, 1], [0, 1, 0]],
        [[0, 1], [1, 1], [0, 1]]
    ],
    'S': [
        [[0, 1, 1], [1, 1, 0]],
        [[1, 0], [1, 1], [0, 1]]
    ],
    'Z': [
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1], [1, 1], [1, 0]]
    ],
    'J': [
        [[1, 0, 0], [1, 1, 1]],
        [[1, 1], [1, 0], [1, 0]],
        [[1, 1, 1], [0, 0, 1]],
        [[0, 1], [0, 1], [1, 1]]
    ],
    'L': [
        [[0, 0, 1], [1, 1, 1]],
        [[1, 0], [1, 0], [1, 1]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1], [0, 1], [0, 1]]
    ]
}

# 計分規則
SCORE_LINES = {
    1: 100,
    2: 300,
    3: 500,
    4: 800
}


class Piece:
    """方塊類別"""
    
    def __init__(self, shape_type: str):
        self.type = shape_type
        self.rotation = 0
        self.shape = SHAPES[shape_type][0]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self, clockwise: bool = True):
        """旋轉方塊"""
        rotations = SHAPES[self.type]
        if clockwise:
            self.rotation = (self.rotation + 1) % len(rotations)
        else:
            self.rotation = (self.rotation - 1) % len(rotations)
        self.shape = rotations[self.rotation]
    
    def get_blocks(self) -> List[Tuple[int, int]]:
        """獲取方塊佔據的座標"""
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + x, self.y + y))
        return blocks
    
    def copy(self):
        """複製方塊"""
        return copy.deepcopy(self)


class Board:
    """遊戲板類別"""
    
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def is_valid_position(self, piece: Piece) -> bool:
        """檢查方塊位置是否有效"""
        for x, y in piece.get_blocks():
            # 檢查邊界
            if x < 0 or x >= self.width:
                return False
            if y >= self.height:
                return False
            
            # 檢查是否與已固定方塊重疊
            if y >= 0 and self.grid[y][x] is not None:
                return False
        
        return True
    
    def lock_piece(self, piece: Piece):
        """固定方塊到遊戲板"""
        for x, y in piece.get_blocks():
            if 0 <= y < self.height:
                self.grid[y][x] = piece.type
    
    def clear_lines(self) -> int:
        """清除完整的行，返回清除的行數"""
        lines_cleared = 0
        y = self.height - 1
        
        while y >= 0:
            if all(cell is not None for cell in self.grid[y]):
                # 刪除這一行
                del self.grid[y]
                # 在頂部插入新的空行
                self.grid.insert(0, [None for _ in range(self.width)])
                lines_cleared += 1
            else:
                y -= 1
        
        return lines_cleared
    
    def is_game_over(self) -> bool:
        """檢查遊戲是否結束（頂部有方塊）"""
        return any(cell is not None for cell in self.grid[0])


class Tetris:
    """Tetris 遊戲主類別"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_colors()
        
        # 遊戲狀態
        self.board = Board()
        self.current_piece = None
        self.next_piece = None
        self.hold_piece = None
        self.can_hold = True
        
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        
        # 計時器
        self.drop_timer = 0
        self.drop_delay = 1.0
        
        # 生成第一個方塊
        self.spawn_piece()
        self.next_piece = self.create_random_piece()
    
    def setup_colors(self):
        """設定顏色"""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)    # I
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # O
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # T
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   # S
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)     # Z
        curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)    # J
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)   # L (用白色代替橙色)
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)   # UI
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Ghost (淺色)
    
    def get_color_pair(self, shape_type: str) -> int:
        """獲取方塊類型對應的顏色"""
        color_map = {
            'I': 1, 'O': 2, 'T': 3, 'S': 4,
            'Z': 5, 'J': 6, 'L': 7
        }
        return curses.color_pair(color_map.get(shape_type, 8))
    
    def create_random_piece(self) -> Piece:
        """創建隨機方塊"""
        shape_type = random.choice(list(SHAPES.keys()))
        return Piece(shape_type)
    
    def spawn_piece(self):
        """生成新方塊"""
        if self.next_piece:
            self.current_piece = self.next_piece
            self.next_piece = self.create_random_piece()
        else:
            self.current_piece = self.create_random_piece()
        
        self.can_hold = True
        
        # 檢查是否能放置新方塊
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
    
    def get_drop_delay(self) -> float:
        """根據等級計算下落延遲"""
        return max(0.1, 1.0 - (self.level - 1) * 0.05)
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """移動方塊"""
        self.current_piece.x += dx
        self.current_piece.y += dy
        
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False
        
        return True
    
    def rotate_piece(self, clockwise: bool = True):
        """旋轉方塊（包含 wall kick）"""
        original_x = self.current_piece.x
        original_y = self.current_piece.y
        original_rotation = self.current_piece.rotation
        original_shape = self.current_piece.shape
        
        # 嘗試旋轉
        self.current_piece.rotate(clockwise)
        
        # 如果位置無效，嘗試 wall kick
        if not self.board.is_valid_position(self.current_piece):
            # 嘗試各種偏移
            offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]
            success = False
            
            for dx, dy in offsets:
                self.current_piece.x = original_x + dx
                self.current_piece.y = original_y + dy
                
                if self.board.is_valid_position(self.current_piece):
                    success = True
                    break
            
            if not success:
                # 恢復原狀
                self.current_piece.x = original_x
                self.current_piece.y = original_y
                self.current_piece.rotation = original_rotation
                self.current_piece.shape = original_shape
    
    def soft_drop(self) -> int:
        """軟下落（加速下落）"""
        if self.move_piece(0, 1):
            return 1  # 每格 1 分
        return 0
    
    def hard_drop(self):
        """硬下落（瞬間落到底部）"""
        drop_distance = 0
        while self.move_piece(0, 1):
            drop_distance += 1
        
        self.score += drop_distance * 2  # 每格 2 分
        self.lock_and_spawn()
    
    def hold_current_piece(self):
        """暫存當前方塊"""
        if not self.can_hold:
            return
        
        if self.hold_piece is None:
            # 第一次暫存
            self.hold_piece = Piece(self.current_piece.type)
            self.spawn_piece()
        else:
            # 交換暫存方塊
            temp_type = self.current_piece.type
            self.current_piece = Piece(self.hold_piece.type)
            self.hold_piece = Piece(temp_type)
        
        self.can_hold = False
    
    def lock_and_spawn(self):
        """固定方塊並生成新方塊"""
        self.board.lock_piece(self.current_piece)
        
        # 清除完整的行
        lines_cleared = self.board.clear_lines()
        if lines_cleared > 0:
            self.lines += lines_cleared
            self.score += SCORE_LINES.get(lines_cleared, 0) * self.level
            
            # 每 10 行升一級
            self.level = self.lines // 10 + 1
            self.drop_delay = self.get_drop_delay()
        
        # 生成新方塊
        self.spawn_piece()
        
        # 檢查遊戲是否結束
        if self.board.is_game_over():
            self.game_over = True
    
    def get_ghost_piece(self) -> Optional[Piece]:
        """獲取幽靈方塊（顯示落點）"""
        if not self.current_piece:
            return None
        
        ghost = self.current_piece.copy()
        while self.board.is_valid_position(ghost):
            ghost.y += 1
        ghost.y -= 1
        
        return ghost
    
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
        
        # 移動控制
        if key == curses.KEY_LEFT:
            self.move_piece(-1, 0)
        elif key == curses.KEY_RIGHT:
            self.move_piece(1, 0)
        elif key == curses.KEY_DOWN:
            self.score += self.soft_drop()
        
        # 旋轉
        elif key == curses.KEY_UP:
            self.rotate_piece(clockwise=True)
        elif key == ord('z') or key == ord('Z'):
            self.rotate_piece(clockwise=False)
        
        # Hard drop
        elif key == ord(' '):
            self.hard_drop()
        
        # Hold
        elif key == ord('c') or key == ord('C'):
            self.hold_current_piece()
        
        return True
    
    def update(self, dt: float):
        """更新遊戲狀態"""
        if self.paused or self.game_over:
            return
        
        # 自動下落
        self.drop_timer += dt
        if self.drop_timer >= self.drop_delay:
            self.drop_timer = 0
            
            if not self.move_piece(0, 1):
                # 無法下落，固定方塊
                self.lock_and_spawn()
    
    def render(self):
        """渲染遊戲畫面"""
        self.stdscr.erase()
        
        # 繪製標題
        title = "T E T R I S"
        self.stdscr.addstr(1, (SCREEN_WIDTH - len(title)) // 2, title, 
                          curses.color_pair(8) | curses.A_BOLD)
        
        # 繪製遊戲板邊框
        for y in range(BOARD_HEIGHT + 1):
            self.stdscr.addstr(BOARD_TOP + y, BOARD_LEFT - 1, "│", curses.color_pair(8))
            self.stdscr.addstr(BOARD_TOP + y, BOARD_LEFT + BOARD_WIDTH * 2, "│", curses.color_pair(8))
        
        for x in range(BOARD_WIDTH * 2 + 1):
            self.stdscr.addstr(BOARD_TOP + BOARD_HEIGHT, BOARD_LEFT - 1 + x, "─", curses.color_pair(8))
        
        self.stdscr.addstr(BOARD_TOP + BOARD_HEIGHT, BOARD_LEFT - 1, "└", curses.color_pair(8))
        self.stdscr.addstr(BOARD_TOP + BOARD_HEIGHT, BOARD_LEFT + BOARD_WIDTH * 2, "┘", curses.color_pair(8))
        
        # 繪製已固定的方塊
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board.grid[y][x] is not None:
                    shape_type = self.board.grid[y][x]
                    screen_x = BOARD_LEFT + x * 2
                    screen_y = BOARD_TOP + y
                    self.stdscr.addstr(screen_y, screen_x, "██", self.get_color_pair(shape_type))
        
        # 繪製幽靈方塊（使用空心方塊字元）
        ghost = self.get_ghost_piece()
        if ghost and ghost.y != self.current_piece.y:
            for x, y in ghost.get_blocks():
                if 0 <= y < BOARD_HEIGHT:
                    screen_x = BOARD_LEFT + x * 2
                    screen_y = BOARD_TOP + y
                    # 網點/點狀字元選項:
                    # ∴∴ - 三點符號
                    # ∵∵ - 反三點
                    # ∷∷ - 雙點
                    # ⋮⋮ - 垂直三點
                    # ⋯⋯ - 中線三點
                    # ⁚⁚ - 上標雙點
                    # ··  - 中點
                    # ::  - 冒號
                    # ░░ - 淺色陰影（25%）
                    # ▒▒ - 中等陰影（50%）
                    # 目前使用: 冒號（簡單清晰）
                    self.stdscr.addstr(screen_y, screen_x, "::", curses.color_pair(9) | curses.A_DIM)
        
        # 繪製當前方塊
        if self.current_piece:
            for x, y in self.current_piece.get_blocks():
                if 0 <= y < BOARD_HEIGHT:
                    screen_x = BOARD_LEFT + x * 2
                    screen_y = BOARD_TOP + y
                    self.stdscr.addstr(screen_y, screen_x, "██", 
                                     self.get_color_pair(self.current_piece.type))
        
        # 右側資訊欄
        info_x = BOARD_LEFT + BOARD_WIDTH * 2 + 4
        
        # Next piece
        self.stdscr.addstr(BOARD_TOP, info_x, "NEXT:", curses.color_pair(8) | curses.A_BOLD)
        if self.next_piece:
            for dy, row in enumerate(self.next_piece.shape):
                for dx, cell in enumerate(row):
                    if cell:
                        self.stdscr.addstr(BOARD_TOP + 1 + dy, info_x + dx * 2, "██",
                                         self.get_color_pair(self.next_piece.type))
        
        # Hold piece
        self.stdscr.addstr(BOARD_TOP, info_x + 12, "HOLD:", curses.color_pair(8) | curses.A_BOLD)
        if self.hold_piece:
            for dy, row in enumerate(SHAPES[self.hold_piece.type][0]):
                for dx, cell in enumerate(row):
                    if cell:
                        self.stdscr.addstr(BOARD_TOP + 1 + dy, info_x + 12 + dx * 2, "██",
                                         self.get_color_pair(self.hold_piece.type))
        
        # 分數資訊
        info_y = BOARD_TOP + 5
        self.stdscr.addstr(info_y, info_x, f"SCORE: {self.score:06d}", curses.color_pair(8))
        self.stdscr.addstr(info_y + 1, info_x, f"LINES: {self.lines:03d}", curses.color_pair(8))
        self.stdscr.addstr(info_y + 2, info_x, f"LEVEL: {self.level:02d}", curses.color_pair(8))
        
        # 控制說明
        controls_y = BOARD_TOP + 9
        controls = [
            "CONTROLS:",
            "← → : Move",
            "↑   : Rotate CW",
            "Z   : Rotate CCW",
            "↓   : Soft Drop",
            "Space: Hard Drop",
            "C   : Hold",
            "P   : Pause",
            "Q   : Quit"
        ]
        
        for i, text in enumerate(controls):
            if i == 0:
                self.stdscr.addstr(controls_y + i, info_x, text, 
                                 curses.color_pair(8) | curses.A_BOLD)
            else:
                self.stdscr.addstr(controls_y + i, info_x, text, curses.color_pair(8))
        
        # 遊戲狀態訊息
        if self.game_over:
            msg = "GAME OVER! Press Q to quit"
            self.stdscr.addstr(SCREEN_HEIGHT // 2, (SCREEN_WIDTH - len(msg)) // 2, msg,
                             curses.color_pair(5) | curses.A_BOLD)
        elif self.paused:
            msg = "PAUSED - Press P to continue"
            self.stdscr.addstr(SCREEN_HEIGHT // 2, (SCREEN_WIDTH - len(msg)) // 2, msg,
                             curses.color_pair(8) | curses.A_BOLD)
        
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
        curses.wrapper(lambda stdscr: Tetris(stdscr).run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
