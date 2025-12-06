# Day 6: Pac-Man - 小精靈迷宮遊戲

## 遊戲概述
經典的 Pac-Man 迷宮追逐遊戲。玩家控制小精靈在迷宮中吃豆子，躲避或追逐幽靈。

## 遊戲機制

### 核心玩法
1. **玩家控制**
   - ← → ↑ ↓ 鍵：控制 Pac-Man 移動
   - Q 鍵：退出遊戲
   - P 鍵：暫停

2. **遊戲目標**
   - 吃掉迷宮中所有小豆子
   - 避開幽靈（或吃能量豆後追逐幽靈）
   - 獲得最高分

3. **遊戲元素**
   - **Pac-Man**: 玩家角色 (◐ 或 C)
   - **小豆子**: 普通豆子 (·) - 10 分
   - **能量豆**: 大豆子 (●) - 50 分
   - **幽靈**: 4 個不同顏色的幽靈
   - **水果**: 額外獎勵（櫻桃、草莓等）

4. **幽靈系統**
   - **Blinky (紅色)**: 直接追逐 Pac-Man
   - **Pinky (粉紅)**: 嘗試堵截 Pac-Man
   - **Inky (青色)**: 複雜的追逐邏輯
   - **Clyde (橙色)**: 隨機移動

5. **能量豆效果**
   - 吃下能量豆後，幽靈變成藍色可被吃掉
   - 持續時間：10 秒
   - 吃幽靈得分：200/400/800/1600 分（連續吃）

6. **生命系統**
   - 初始 3 條命
   - 被幽靈碰到失去 1 條命
   - 失去所有生命 = 遊戲結束

## 技術實作

### 迷宮設計

```python
# 迷宮佈局（簡化版）
MAZE = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#●####.#####.##.#####.####●#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#     ",
    "     #.##          ##.#     ",
    "     #.## ###--### ##.#     ",  # 幽靈之家
    "######.## #      # ##.######",
    "      .   #      #   .      ",
    "######.## #      # ##.######",
    "     #.## ######## ##.#     ",
    "     #.##          ##.#     ",
    "     #.## ######## ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#●..##................##..●#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

# 符號說明:
# # = 牆壁
# . = 小豆子
# ● = 能量豆
# 空格 = 可通行空間
# - = 幽靈之家的門
```

### 遊戲物件

```python
class PacMan:
    def __init__(self):
        self.x = 14  # 起始位置
        self.y = 23
        self.direction = (0, 0)  # (dx, dy)
        self.next_direction = (0, 0)
        self.lives = 3
        self.score = 0
        self.power_mode = False
        self.power_timer = 0
    
    def move(self, maze):
        # 嘗試轉向
        if self.can_move(self.next_direction, maze):
            self.direction = self.next_direction
        
        # 移動
        if self.can_move(self.direction, maze):
            self.x += self.direction[0]
            self.y += self.direction[1]
            
            # 隧道傳送（左右邊界）
            if self.x < 0:
                self.x = maze_width - 1
            elif self.x >= maze_width:
                self.x = 0
    
    def get_char(self):
        # 根據方向返回不同字元
        if self.direction == (1, 0):   # 右
            return "◐"
        elif self.direction == (-1, 0): # 左
            return "◑"
        elif self.direction == (0, -1): # 上
            return "◓"
        elif self.direction == (0, 1):  # 下
            return "◒"
        return "●"


class Ghost:
    def __init__(self, name, color, home_x, home_y):
        self.name = name
        self.color = color
        self.x = home_x
        self.y = home_y
        self.direction = (0, -1)  # 初始向上
        self.frightened = False
        self.eaten = False
        self.mode = "scatter"  # scatter, chase, frightened
    
    def update_ai(self, pacman, maze):
        if self.frightened:
            # 隨機逃跑
            self.move_random(maze)
        elif self.mode == "chase":
            # 追逐 Pac-Man
            self.chase_pacman(pacman, maze)
        else:
            # Scatter 模式 - 回到角落
            self.move_to_corner(maze)
    
    def chase_pacman(self, pacman, maze):
        # 使用 BFS 或簡單的追逐邏輯
        target = (pacman.x, pacman.y)
        
        # 根據幽靈類型調整目標
        if self.name == "Pinky":
            # 預測 Pac-Man 前方 4 格
            target = (pacman.x + pacman.direction[0] * 4,
                     pacman.y + pacman.direction[1] * 4)
        elif self.name == "Inky":
            # 複雜邏輯...
            pass
        elif self.name == "Clyde":
            # 距離遠時追逐，近時逃跑
            dist = abs(self.x - pacman.x) + abs(self.y - pacman.y)
            if dist < 8:
                target = (0, 0)  # 逃到角落
        
        # 移動到目標
        self.move_towards(target, maze)
    
    def get_char(self):
        if self.frightened:
            return "Ö"  # 可被吃的狀態
        elif self.eaten:
            return "oo"  # 眼睛（回家中）
        else:
            return "M"  # 正常幽靈


class Maze:
    def __init__(self, layout):
        self.layout = [list(row) for row in layout]
        self.width = len(layout[0])
        self.height = len(layout)
        self.dots_remaining = self.count_dots()
    
    def get_cell(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.layout[y][x]
        return '#'
    
    def eat_dot(self, x, y):
        cell = self.get_cell(x, y)
        if cell == '.':
            self.layout[y][x] = ' '
            self.dots_remaining -= 1
            return 10  # 得分
        elif cell == '●':
            self.layout[y][x] = ' '
            self.dots_remaining -= 1
            return 50  # 得分
        return 0
    
    def is_walkable(self, x, y):
        cell = self.get_cell(x, y)
        return cell != '#'
```

### 遊戲狀態

```python
GameState:
  - pacman: PacMan
  - ghosts: List[Ghost]  # 4 個幽靈
  - maze: Maze
  - score: int
  - level: int
  - lives: int
  - power_mode: bool
  - power_timer: float
  - game_over: bool
  - level_complete: bool
  - ghost_combo: int  # 連續吃幽靈計數
```

### 渲染設計

```
遊戲畫面佈局：
┌──────────────────────────────────────────────────┐
│ PAC-MAN          SCORE: 0000    HI: 9999  LIVES: │
├──────────────────────────────────────────────────┤
│ ############################                     │
│ #............##............#                     │
│ #.####.#####.##.#####.####.#                     │
│ #●####.#####.##.#####.####●#                     │
│ #..........................#                     │
│ #.####.##.########.##.####.#                     │
│ #......##....##....##......#                     │
│ ######.##### ## #####.######                     │
│      #.##    M     ##.#                          │
│      #.## ###--### ##.#     ← 幽靈之家          │
│ ######.## # M  M # ##.######                     │
│       .   #   M  #   .                           │
│ ######.## #      # ##.######                     │
│      #.## ######## ##.#                          │
│ ######.## ######## ##.######                     │
│ #............##............#                     │
│ #.####.#####.##.#####.####.#                     │
│ #●..##.......◐........##..●#                     │
│ ###.##.##.########.##.##.###                     │
│ #......##....##....##......#                     │
│ #.##########.##.##########.#                     │
│ #..........................#                     │
│ ############################                     │
├──────────────────────────────────────────────────┤
│ Controls: Arrow keys to move | P: Pause | Q: Quit│
└──────────────────────────────────────────────────┘

◐/◑/◓/◒ - Pac-Man (不同方向)
M - 幽靈（紅/粉/青/橙）
Ö - 可被吃的幽靈（藍色）
· - 小豆子
● - 能量豆
# - 牆壁
```

### 畫面規格
- 迷宮大小：28x30
- 總寬度：80 字元
- 總高度：30 行
- FPS：30
- 使用 curses 消除閃爍

## AI 邏輯

### 幽靈行為模式

```python
# 遊戲開始後的模式切換
GHOST_MODES = [
    ("scatter", 7),   # 7 秒 scatter
    ("chase", 20),    # 20 秒 chase
    ("scatter", 7),   # 7 秒 scatter
    ("chase", 20),    # 20 秒 chase
    ("scatter", 5),   # 5 秒 scatter
    ("chase", 20),    # 20 秒 chase
    ("scatter", 5),   # 5 秒 scatter
    ("chase", -1)     # 無限 chase
]

# 追逐邏輯（簡化版 BFS）
def find_path_to_target(ghost_pos, target_pos, maze):
    # 使用 BFS 找最短路徑
    queue = [(ghost_pos, [])]
    visited = set()
    
    while queue:
        (x, y), path = queue.pop(0)
        
        if (x, y) == target_pos:
            return path
        
        if (x, y) in visited:
            continue
        visited.add((x, y))
        
        # 檢查四個方向
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if maze.is_walkable(nx, ny):
                queue.append(((nx, ny), path + [(dx, dy)]))
    
    return []  # 找不到路徑
```

## 開發步驟

### Phase 1: 基礎結構
- [ ] 創建 game_006_pacman.py
- [ ] 設定 curses 畫面
- [ ] 定義迷宮佈局
- [ ] 建立 PacMan, Ghost, Maze 類別

### Phase 2: 基本移動
- [ ] Pac-Man 移動控制
- [ ] 牆壁碰撞檢測
- [ ] 吃豆子邏輯
- [ ] 得分系統

### Phase 3: 幽靈系統
- [ ] 幽靈生成與初始位置
- [ ] 基本追逐 AI
- [ ] 碰撞檢測（Pac-Man vs 幽靈）
- [ ] 生命系統

### Phase 4: 能量豆系統
- [ ] 能量豆效果
- [ ] 幽靈變藍可被吃
- [ ] 計時器系統
- [ ] 幽靈復活機制

### Phase 5: 進階 AI
- [ ] 4 種不同的幽靈行為
- [ ] Scatter/Chase 模式切換
- [ ] 路徑尋找算法

### Phase 6: 優化與測試
- [ ] 關卡完成邏輯
- [ ] 遊戲結束畫面
- [ ] 性能優化
- [ ] 完整測試

## 測試清單

### 功能測試
- [ ] Pac-Man 移動流暢
- [ ] 吃豆子正常
- [ ] 幽靈追逐正確
- [ ] 能量豆效果正常
- [ ] 碰撞檢測準確
- [ ] 得分系統正確
- [ ] 生命系統正常

### 體驗測試
- [ ] 30 FPS 流暢運行
- [ ] 無閃爍
- [ ] AI 有挑戰性但不過分
- [ ] 遊戲節奏良好

### 邊界測試
- [ ] 隧道傳送正常
- [ ] 迷宮邊界處理
- [ ] 所有豆子吃完過關
- [ ] 幽靈不會卡住

## 預期挑戰

1. **迷宮設計**
   - 需要平衡的迷宮佈局
   - 解決：參考經典 Pac-Man 迷宮

2. **幽靈 AI**
   - 4 種不同的行為模式
   - 解決：簡化版本，重點在追逐邏輯

3. **路徑尋找**
   - BFS/A* 算法實作
   - 解決：使用簡單的 BFS

4. **性能問題**
   - 多個幽靈同時計算路徑
   - 解決：限制計算頻率

## 成功標準

- ✅ Pac-Man 控制流暢自然
- ✅ 幽靈 AI 有挑戰性
- ✅ 能量豆效果明顯
- ✅ 迷宮設計合理
- ✅ 畫面流暢 30 FPS
- ✅ 無明顯 bug
- ✅ 遊戲性良好

## 簡化策略

由於 Pac-Man 相當複雜，我們可以：
1. 使用較小的迷宮（20x20 而非原版 28x30）
2. 簡化幽靈 AI（只實作基本追逐）
3. 暫時不實作水果獎勵
4. 先做單關，之後再加多關卡

## 時間預估
- 規劃：30 分鐘 ✅
- 開發：3-4 小時（迷宮和 AI 較複雜）
- 測試：30 分鐘
- 總計：約 4-5 小時

---
**創建日期**: 2025-12-06
**遊戲編號**: 006
**難度評估**: ⭐⭐⭐⭐⭐ (5/5) - 迷宮和 AI 很複雜
**預計完成時間**: 2025-12-06
