# Day 9: Wordle - 猜單字遊戲

## 🎮 遊戲概述

Wordle 是一款流行的文字猜謎遊戲，玩家有6次機會猜一個5字母的英文單字。每次猜測後會獲得顏色提示。

## 🎯 遊戲特色

### 為什麼適合 CLI？
- ✅ 純文字遊戲的最佳代表
- ✅ 顏色回饋系統完美
- ✅ 回合制，可以慢慢思考
- ✅ 簡單但有趣
- ✅ 目前很流行

### 核心機制
1. **猜測單字**：
   - 輸入5個字母的英文單字
   - 必須是有效的英文單字
   - 每次遊戲有6次機會

2. **顏色提示系統**：
   - 🟩 綠色：字母正確且位置正確
   - 🟨 黃色：字母正確但位置錯誤
   - ⬜ 灰色：字母不在答案中

3. **遊戲目標**：
   - 在6次內猜出正確單字

4. **勝利條件**：
   - 猜中正確單字

## 💻 技術設計

### 核心數據結構
```python
class Wordle:
    def __init__(self):
        self.word_length = 5
        self.max_attempts = 6
        
        # 單字列表
        self.word_list = []  # 可猜的單字
        self.answer_list = []  # 答案候選單字
        
        # 遊戲狀態
        self.target_word = ""
        self.attempts = []  # 已猜測的單字
        self.current_guess = ""
        
        # 鍵盤狀態
        self.keyboard_state = {}  # 每個字母的狀態
        
        self.game_over = False
        self.won = False
```

### 核心算法

#### 1. 檢查猜測
```python
def check_guess(guess, target):
    """檢查猜測，返回每個字母的狀態"""
    result = ['gray'] * 5
    target_chars = list(target)
    
    # 第一遍：標記正確位置（綠色）
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = 'green'
            target_chars[i] = None  # 標記已使用
    
    # 第二遍：標記錯誤位置（黃色）
    for i in range(5):
        if result[i] == 'gray' and guess[i] in target_chars:
            result[i] = 'yellow'
            target_chars[target_chars.index(guess[i])] = None
    
    return result
```

#### 2. 單字驗證
```python
def is_valid_word(word):
    """檢查是否為有效單字"""
    return (len(word) == 5 and 
            word.isalpha() and 
            word.lower() in word_list)
```

#### 3. 鍵盤狀態更新
```python
def update_keyboard(letter, state):
    """更新鍵盤上字母的狀態"""
    # 優先級：green > yellow > gray
    current = keyboard_state.get(letter, 'unused')
    
    if state == 'green':
        keyboard_state[letter] = 'green'
    elif state == 'yellow' and current != 'green':
        keyboard_state[letter] = 'yellow'
    elif current == 'unused':
        keyboard_state[letter] = 'gray'
```

### 視覺設計

#### 遊戲界面
```
╔════════════════════════════════╗
║        WORDLE - 猜單字         ║
╠════════════════════════════════╣
║                                ║
║      🟩 🟨 ⬜ ⬜ 🟩           ║
║      C  R  A  N  E             ║
║                                ║
║      🟨 ⬜ 🟩 ⬜ ⬜           ║
║      S  T  O  N  E             ║
║                                ║
║      ⬜ ⬜ ⬜ ⬜ ⬜           ║
║      _ _ _ _ _                 ║
║                                ║
║      ⬜ ⬜ ⬜ ⬜ ⬜           ║
║      _ _ _ _ _                 ║
║                                ║
║      ⬜ ⬜ ⬜ ⬜ ⬜           ║
║      _ _ _ _ _                 ║
║                                ║
║      ⬜ ⬜ ⬜ ⬜ ⬜           ║
║      _ _ _ _ _                 ║
║                                ║
╠════════════════════════════════╣
║  Keyboard:                     ║
║  🟩: Correct position          ║
║  🟨: Wrong position            ║
║  ⬜: Not in word               ║
║                                ║
║  Q W E R T Y U I O P           ║
║   A S D F G H J K L            ║
║    Z X C V B N M               ║
║                                ║
║  Type your guess and press ↵   ║
║  Q: Quit                       ║
╚════════════════════════════════╝
```

#### 顏色方案
- **綠色背景**: 字母位置正確
- **黃色背景**: 字母存在但位置錯誤
- **灰色背景**: 字母不在答案中
- **白色背景**: 未猜測的格子

### 控制系統

```python
# 輸入系統
- 直接輸入字母（自動轉大寫）
- ENTER: 提交猜測
- BACKSPACE: 刪除字母
- Q: 退出遊戲
- N: 新遊戲（遊戲結束後）
```

## 📋 開發檢查清單

### 階段 1: 單字庫
- [ ] 準備常用5字母英文單字列表
- [ ] 準備答案候選列表（常見單字）
- [ ] 實作單字驗證功能

### 階段 2: 核心邏輯
- [ ] 實作猜測檢查算法
- [ ] 實作鍵盤狀態更新
- [ ] 處理重複字母情況

### 階段 3: 視覺呈現
- [ ] 設計方格界面
- [ ] 實作顏色回饋系統
- [ ] 顯示虛擬鍵盤狀態
- [ ] 輸入提示

### 階段 4: 遊戲體驗
- [ ] 勝利/失敗畫面
- [ ] 統計數據（嘗試次數、勝率）
- [ ] 每日單字模式（可選）
- [ ] 提示功能（可選）

## 🎨 特殊效果

### 動畫效果
- 猜測提交後的翻牌動畫（可選）
- 勝利時的慶祝動畫
- 失敗時顯示答案

### 鍵盤視覺化
顯示虛擬鍵盤，用顏色標記已使用的字母：
```
Q W E R T Y U I O P
 A S D F G H J K L
  Z X C V B N M
```

## 🧪 測試要點

1. **猜測檢查測試**：
   - [ ] 正確位置標記為綠色
   - [ ] 錯誤位置標記為黃色
   - [ ] 不存在的字母標記為灰色
   - [ ] 重複字母處理正確

2. **單字驗證測試**：
   - [ ] 只接受5字母單字
   - [ ] 只接受有效英文單字
   - [ ] 大小寫正確處理

3. **遊戲邏輯測試**：
   - [ ] 最多6次猜測
   - [ ] 猜中後遊戲結束
   - [ ] 用完機會後遊戲結束

4. **視覺測試**：
   - [ ] 顏色清晰易辨
   - [ ] 鍵盤狀態正確
   - [ ] 界面不閃爍

## 🎲 單字列表

### 簡化版（開發用）
使用常見的5字母英文單字：
```python
common_words = [
    "APPLE", "BREAD", "CHAIR", "DANCE", "EARTH",
    "FLAME", "GRAPE", "HEART", "IMAGE", "JUICE",
    "KNIFE", "LIGHT", "MUSIC", "NIGHT", "OCEAN",
    "PEACE", "QUEEN", "RIVER", "STORM", "TIGER",
    "UNCLE", "VOICE", "WATER", "YOUNG", "ZEBRA"
]
```

### 完整版（可選）
- 使用完整的5字母英文單字字典
- 約12,000+個單字
- 答案從常見單字中選擇（約2,000個）

## 🚀 挑戰功能

### 基礎版本
- 隨機選擇單字
- 6次猜測機會
- 基本顏色回饋

### 進階功能（未來）
- 每日挑戰模式（每天固定單字）
- 統計數據追蹤
- 困難模式（必須使用已知的綠色/黃色字母）
- 提示系統
- 時間限制模式

## 🎓 重要考量

### 重複字母處理
最複雜的部分是處理重複字母：

**範例 1**: 目標 "ROBOT"，猜測 "FLOOR"
- F: 灰色（不存在）
- L: 灰色（不存在）
- O: 黃色（存在但位置錯）- 第一個O
- O: 綠色（位置正確）- 第二個O
- R: 黃色（存在但位置錯）

**範例 2**: 目標 "SPEED"，猜測 "ERASE"
- E: 黃色（存在但位置錯）- 第一個E
- R: 灰色（不存在）
- A: 灰色（不存在）
- S: 黃色（存在但位置錯）
- E: 綠色（位置正確）- 第二個E

### 演算法正確性
1. 先標記所有綠色（正確位置）
2. 再標記黃色（錯誤位置），但不能重複使用已匹配的字母
3. 其餘為灰色

## 📚 參考資料
- 原始 Wordle 遊戲機制
- 常見5字母英文單字列表
- 顏色回饋系統設計

---
**創建時間**: 2025-12-07
**預計完成**: Day 9
**難度**: ⭐⭐⭐ (中等)
