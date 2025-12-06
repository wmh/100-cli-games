# Day 5: Tetris - 俄羅斯方塊

## 遊戲概述
經典的俄羅斯方塊益智遊戲。不同形狀的方塊從頂部落下，玩家需要旋轉和移動方塊，消除完整的橫行來得分。

## 遊戲機制

### 核心玩法
1. **方塊控制**
   - ← → 鍵：左右移動
   - ↓ 鍵：加速下落
   - ↑ 鍵或空白鍵：順時針旋轉
   - Z 鍵：逆時針旋轉
   - 空格鍵：瞬間落到底部（Hard Drop）
   - P 鍵：暫停
   - Q 鍵：退出

2. **方塊類型（7種）**
   - I 型：████ (4格直線，青色)
   - O 型：█████ (2x2方塊，黃色)
   - T 型：▀█▀ (T字形，紫色)
   - S 型：_██ (S字形，綠色)
   - Z 型：██_ (Z字形，紅色)
   - J 型：█▀▀ (J字形，藍色)
   - L 型：▀▀█ (L字形，橙色)

3. **遊戲規則**
   - 方塊從頂部中央產生並自動下落
   - 玩家可以移動和旋轉方塊
   - 方塊無法再移動時固定在遊戲區域
   - 完整的橫行會被消除並獲得分數
   - 方塊堆疊到頂部 = 遊戲結束

4. **計分系統**
   - 1 行：100 分
   - 2 行：300 分（+100 獎勵）
   - 3 行：500 分（+200 獎勵）
   - 4 行（Tetris）：800 分（+300 獎勵）
   - Hard Drop：每格 2 分
   - Soft Drop：每格 1 分

5. **難度系統**
   - 每消除 10 行升一級
   - 等級越高，下落速度越快
   - 最高等級：20

## 技術實作

### 遊戲物件

```python
# 方塊形狀定義
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

# 顏色定義
COLORS = {
    'I': curses.COLOR_CYAN,
    'O': curses.COLOR_YELLOW,
    'T': curses.COLOR_MAGENTA,
    'S': curses.COLOR_GREEN,
    'Z': curses.COLOR_RED,
    'J': curses.COLOR_BLUE,
    'L': 208  # 橙色（需要自定義）
}

# 當前方塊
class Piece:
    def __init__(self, shape_type):
        self.type = shape_type
        self.shape = SHAPES[shape_type][0]
        self.rotation = 0
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.color = COLORS[shape_type]
    
    def rotate(self, clockwise=True):
        """旋轉方塊"""
        rotations = SHAPES[self.type]
        if clockwise:
            self.rotation = (self.rotation + 1) % len(rotations)
        else:
            self.rotation = (self.rotation - 1) % len(rotations)
        self.shape = rotations[self.rotation]
    
    def get_blocks(self):
        """獲取方塊佔據的座標"""
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + x, self.y + y))
        return blocks

# 遊戲板
class Board:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
    
    def is_valid_position(self, piece):
        """檢查方塊位置是否有效"""
        for x, y in piece.get_blocks():
            if x < 0 or x >= self.width or y >= self.height:
                return False
            if y >= 0 and self.grid[y][x]:
                return False
        return True
    
    def lock_piece(self, piece):
        """固定方塊到遊戲板"""
        for x, y in piece.get_blocks():
            if y >= 0:
                self.grid[y][x] = piece.type
    
    def clear_lines(self):
        """清除完整的行"""
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * self.width)
                lines_cleared += 1
            else:
                y -= 1
        return lines_cleared
```

### 遊戲狀態

```python
GameState:
  - board: Board                 # 遊戲板
  - current_piece: Piece         # 當前方塊
  - next_piece: Piece           # 下一個方塊
  - hold_piece: Piece or None   # 暫存方塊
  - can_hold: bool              # 是否可以暫存
  - score: int                  # 分數
  - lines: int                  # 消除行數
  - level: int                  # 等級
  - game_over: bool             # 遊戲結束
  - paused: bool                # 暫停
  - drop_timer: float           # 下落計時器
  - drop_delay: float           # 下落延遲
```

### 渲染設計

```
遊戲畫面佈局：
┌───────────────────────────────────────────────────┐
│ TETRIS                                            │
├─────────────────┬─────────────────────────────────┤
│                 │  NEXT:        HOLD:             │
│                 │   ██           ▀▀█              │
│                 │   ██                            │
│                 ├─────────────────────────────────┤
│  ░░░░░░░░░░    │  SCORE: 0000                   │
│  ░░░░░░░░░░    │  LINES: 0                       │
│  ░░░░░░░░░░    │  LEVEL: 1                       │
│  ░░░░░░░░░░    ├─────────────────────────────────┤
│  ░░░░░░░░░░    │  CONTROLS:                      │
│  ░░░░░░░░░░    │  ← → : Move                     │
│  ░░░░░░░░░░    │  ↑/Space: Rotate                │
│  ░░░░░░░░░░    │  ↓ : Soft Drop                  │
│  ░░░░░░░░░░    │  Space: Hard Drop               │
│  ░░░░░░░░░░    │  C: Hold                        │
│  ░░░░░░░░░░    │  P: Pause                       │
│  ░░░░░░░░░░    │  Q: Quit                        │
│  ░░██░░░░░░    │                                 │
│  ░░██░░░░░░    │  Ghost piece: ▓▓                │
│  ░███░░░░░░    │  (shows drop position)          │
│  ░███████░░    │                                 │
│  ████████░░    │                                 │
│  ████████░░    │                                 │
│  ████████░░    │                                 │
│  ██████████    │                                 │
└─────────────────┴─────────────────────────────────┘
```

### 畫面規格
- 遊戲區域：10x20 格子
- 每格 2 個字元寬（使用 ██）
- 顯示區域總寬：80 字元
- 總高度：30 行
- FPS：30（但下落速度由等級決定）

## 物理與邏輯

### 下落邏輯
```python
# 等級決定下落速度
def get_drop_delay(level):
    # 等級越高，延遲越短
    base_delay = 1.0
    return max(0.1, base_delay - (level - 1) * 0.05)

# 自動下落
def auto_drop(dt):
    drop_timer += dt
    if drop_timer >= drop_delay:
        drop_timer = 0
        move_piece_down()

# 軟下落（玩家按下↓）
def soft_drop():
    if move_piece_down():
        score += 1  # 每格 1 分

# 硬下落（玩家按空格）
def hard_drop():
    drop_distance = 0
    while move_piece_down():
        drop_distance += 1
    score += drop_distance * 2  # 每格 2 分
    lock_piece()
```

### 旋轉系統
```python
# SRS (Super Rotation System)
def rotate_with_wallkick(piece, clockwise=True):
    # 嘗試旋轉
    original_shape = piece.shape
    original_rotation = piece.rotation
    piece.rotate(clockwise)
    
    # 如果新位置無效，嘗試 wall kick
    if not board.is_valid_position(piece):
        # 嘗試偏移位置
        offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]
        for dx, dy in offsets:
            piece.x += dx
            piece.y += dy
            if board.is_valid_position(piece):
                return True  # 旋轉成功
            piece.x -= dx
            piece.y -= dy
        
        # 所有偏移都失敗，恢復原狀
        piece.shape = original_shape
        piece.rotation = original_rotation
        return False
    
    return True
```

### 碰撞檢測
```python
def is_valid_position(piece, board):
    for x, y in piece.get_blocks():
        # 檢查邊界
        if x < 0 or x >= board.width:
            return False
        if y >= board.height:
            return False
        
        # 檢查是否與已固定方塊重疊
        if y >= 0 and board.grid[y][x]:
            return False
    
    return True
```

### Ghost Piece（幽靈方塊）
```python
def get_ghost_piece(piece, board):
    ghost = copy.deepcopy(piece)
    while board.is_valid_position(ghost):
        ghost.y += 1
    ghost.y -= 1
    return ghost
```

## 開發步驟

### Phase 1: 基礎結構
- [ ] 創建 game_005_tetris.py
- [ ] 設定 curses 畫面
- [ ] 定義方塊形狀和顏色
- [ ] 建立 Board 和 Piece 類別

### Phase 2: 核心遊戲邏輯
- [ ] 方塊生成系統
- [ ] 自動下落機制
- [ ] 移動控制（左右下）
- [ ] 旋轉系統

### Phase 3: 消除系統
- [ ] 行消除檢測
- [ ] 消除動畫
- [ ] 計分系統
- [ ] 等級系統

### Phase 4: 進階功能
- [ ] Ghost piece（預覽落點）
- [ ] Next piece 顯示
- [ ] Hold piece 系統
- [ ] Hard drop 功能

### Phase 5: UI 與體驗
- [ ] 分數/等級顯示
- [ ] 遊戲結束畫面
- [ ] 暫停功能
- [ ] 控制說明

### Phase 6: 優化與測試
- [ ] 性能優化
- [ ] 難度平衡
- [ ] 錯誤處理
- [ ] 完整測試

## 測試清單

### 功能測試
- [ ] 所有7種方塊正確顯示
- [ ] 移動控制流暢
- [ ] 旋轉正常（包括邊界旋轉）
- [ ] 下落速度隨等級增加
- [ ] 行消除正確
- [ ] 計分準確
- [ ] 遊戲結束判定正確

### 體驗測試
- [ ] 30 FPS 流暢運行
- [ ] 無閃爍
- [ ] 控制反應靈敏
- [ ] 難度曲線合理
- [ ] Ghost piece 清晰可見

### 邊界測試
- [ ] 方塊無法移出邊界
- [ ] 旋轉不會穿牆
- [ ] 滿板時正確結束
- [ ] 極限速度穩定

## 預期挑戰

1. **旋轉系統複雜**
   - 7種方塊，每種多個旋轉狀態
   - Wall kick 系統實作
   - 解決：使用預定義的旋轉矩陣

2. **性能問題**
   - 頻繁的碰撞檢測
   - 大量渲染更新
   - 解決：只更新變化的部分

3. **難度平衡**
   - 速度增長曲線
   - 分數系統平衡
   - 解決：參考經典 Tetris 的數值

4. **Ghost Piece 渲染**
   - 與當前方塊區分
   - 不影響遊戲邏輯
   - 解決：使用半透明字元（▓）

## 成功標準

- ✅ 所有 7 種方塊正確實作
- ✅ 旋轉系統流暢自然
- ✅ 消除系統準確無誤
- ✅ 難度漸進合理
- ✅ 畫面流暢 30 FPS
- ✅ 無明顯 bug
- ✅ 遊戲性良好

## 時間預估
- 規劃：30 分鐘 ✅
- 開發：3-4 小時（方塊系統較複雜）
- 測試：45 分鐘
- 總計：約 4-5 小時

---
**創建日期**: 2025-12-06
**遊戲編號**: 005
**難度評估**: ⭐⭐⭐⭐⭐ (5/5) - 最複雜的方塊遊戲
**預計完成時間**: 2025-12-06
