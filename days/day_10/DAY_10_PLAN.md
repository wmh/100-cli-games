# Day 10: Sokoban - 推箱子 (THE FINAL GAME!)

## 🎮 遊戲概述

Sokoban（倉庫番、推箱子）是一款經典的益智遊戲，玩家需要將所有箱子推到指定位置。

## 🎯 遊戲特色

### 為什麼適合 CLI？
- ✅ 經典益智遊戲
- ✅ 回合制，不需要快速反應
- ✅ 方格顯示完美
- ✅ 策略性極強
- ✅ 完美的收尾遊戲

### 核心機制
1. **推箱子**：
   - 玩家只能推，不能拉
   - 一次只能推一個箱子
   - 不能推箱子到牆壁或其他箱子

2. **遊戲目標**：
   - 將所有箱子推到目標位置

3. **勝利條件**：
   - 所有箱子都在目標位置上

## 💻 技術設計

### 核心數據結構
```python
class Sokoban:
    def __init__(self):
        # 地圖元素
        self.WALL = '#'
        self.FLOOR = ' '
        self.PLAYER = '@'
        self.BOX = '$'
        self.TARGET = '.'
        self.BOX_ON_TARGET = '*'
        self.PLAYER_ON_TARGET = '+'
        
        # 遊戲狀態
        self.board = []
        self.player_pos = [0, 0]
        self.boxes = set()
        self.targets = set()
        self.moves = 0
        self.pushes = 0
```

### 關卡設計

#### Level 1 (簡單)
```
#####
#.@$#
#####
```

#### Level 2 (中等)
```
  #####
  #   #
  #$  #
###  $##
#  $ $.#
#   # ##
#@##  #
#######
```

#### Level 3 (困難)
```
    #####
    #   #
    #$  #
  ###  $##
  #  $ $.#
### # ## #
#   # ## ####
# $  $       #
##### #### #@#
    #      ###
    ########
```

### 移動邏輯

```python
def move(self, dx, dy):
    """移動玩家"""
    new_x = player_x + dx
    new_y = player_y + dy
    
    # 檢查目標位置
    if is_wall(new_x, new_y):
        return False
    
    # 如果目標位置有箱子
    if has_box(new_x, new_y):
        box_new_x = new_x + dx
        box_new_y = new_y + dy
        
        # 檢查箱子能否推動
        if is_wall(box_new_x, box_new_y) or has_box(box_new_x, box_new_y):
            return False
        
        # 推動箱子
        move_box(new_x, new_y, box_new_x, box_new_y)
        pushes += 1
    
    # 移動玩家
    player_x = new_x
    player_y = new_y
    moves += 1
    return True
```

### 勝利檢測

```python
def check_win():
    """檢查是否完成關卡"""
    return all(box in targets for box in boxes)
```

### 視覺設計

#### 遊戲界面
```
╔════════════════════════════════╗
║      SOKOBAN - 推箱子          ║
╠════════════════════════════════╣
║ Level: 1/10  Moves: 15  Push: 8║
╠════════════════════════════════╣
║                                ║
║        #######                 ║
║        #     #                 ║
║        # $   #                 ║
║      ### $.$ ##                ║
║      #  $@$. #                 ║
║      # # .## #                 ║
║      #   ## ###                ║
║      #  $     #                ║
║      ###  #   #                ║
║        ########                ║
║                                ║
╠════════════════════════════════╣
║ ↑↓←→: Move  U: Undo            ║
║ R: Restart  N: Next  Q: Quit   ║
╚════════════════════════════════╝
```

#### 符號說明
- `#`: 牆壁
- `@`: 玩家
- `$`: 箱子
- `.`: 目標位置
- `*`: 箱子在目標位置上
- `+`: 玩家在目標位置上
- ` `: 空地

#### 顏色配置
- **牆壁**: 灰色
- **玩家**: 黃色 + 粗體
- **箱子**: 棕色
- **目標**: 綠色背景
- **完成的箱子**: 綠色箱子
- **空地**: 黑色

### 控制系統

```python
# 移動
↑ / w : 向上
↓ / s : 向下
← / a : 向左
→ / d : 向右

# 功能
u / U : 撤銷上一步
r / R : 重新開始關卡
n / N : 下一關（完成後）
q / Q : 退出遊戲
```

## 📋 開發檢查清單

### 階段 1: 核心邏輯
- [ ] 實作地圖解析
- [ ] 實作移動邏輯
- [ ] 實作推箱子邏輯
- [ ] 勝利檢測

### 階段 2: 遊戲功能
- [ ] 撤銷功能（記錄移動歷史）
- [ ] 重新開始關卡
- [ ] 關卡切換
- [ ] 移動計數

### 階段 3: 視覺呈現
- [ ] 繪製地圖
- [ ] 顏色配置
- [ ] 狀態顯示
- [ ] 勝利畫面

### 階段 4: 關卡設計
- [ ] 10個不同難度關卡
- [ ] 從簡單到困難
- [ ] 測試每個關卡可解

## 🎨 關卡設計原則

### 簡單關卡（1-3）
- 3-5個箱子
- 小地圖
- 直接的解法
- 少量死局可能

### 中等關卡（4-7）
- 5-8個箱子
- 中型地圖
- 需要思考順序
- 需要避免死局

### 困難關卡（8-10）
- 8-12個箱子
- 大型地圖
- 複雜的推箱順序
- 容易進入死局

## 🧪 測試要點

1. **移動測試**：
   - [ ] 玩家正常移動
   - [ ] 不能穿牆
   - [ ] 不能穿箱子（不推動時）

2. **推箱子測試**：
   - [ ] 正確推動箱子
   - [ ] 箱子不能推到牆
   - [ ] 箱子不能推到箱子
   - [ ] 推動計數正確

3. **遊戲狀態測試**：
   - [ ] 勝利檢測正確
   - [ ] 撤銷功能正常
   - [ ] 重新開始正常
   - [ ] 關卡切換正常

4. **視覺測試**：
   - [ ] 地圖顯示清晰
   - [ ] 顏色搭配合理
   - [ ] 狀態資訊正確

## 🎮 特殊功能

### 撤銷系統
```python
class MoveHistory:
    def __init__(self):
        self.history = []
    
    def add_move(self, player_pos, box_moved, box_from, box_to):
        self.history.append({
            'player': player_pos.copy(),
            'box_moved': box_moved,
            'box_from': box_from,
            'box_to': box_to
        })
    
    def undo(self):
        if not self.history:
            return None
        return self.history.pop()
```

### 死局檢測（進階，可選）
- 箱子推到角落（不在目標上）
- 箱子沿牆排列（不在目標上）
- 箱子被困在2x2區域

## 📚 經典關卡參考

可以使用經典的 Sokoban 關卡集合：
- Original & Extra (Thinking Rabbit)
- Microban (David W. Skinner)
- Boxworld (多個作者)

## 🎯 成就系統（可選）

- 🏆 完成所有關卡
- ⚡ 最少步數完成
- 🎯 最少推動數完成
- 🔄 不使用撤銷完成

---
**創建時間**: 2025-12-07
**預計完成**: Day 10 - THE FINAL GAME! 🎉
**難度**: ⭐⭐⭐⭐ (中高)
