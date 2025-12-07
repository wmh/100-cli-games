# Day 9: Wordle - Word Guessing Game ✅

## 完成日期
2025-12-07

## 🎮 遊戲資訊
- **名稱**: Wordle (猜單字)
- **類型**: 文字猜謎遊戲
- **檔案**: `games/game_009_wordle.py`
- **難度**: 中等
- **狀態**: ✅ 完成

## 📝 遊戲特色

### 核心機制
1. **猜測單字**:
   - 輸入5個字母的英文單字
   - 必須是有效的英文單字
   - 每次遊戲有6次機會

2. **顏色提示系統**:
   - 🟩 綠色：字母正確且位置正確
   - 🟨 黃色：字母正確但位置錯誤
   - ⬜ 灰色：字母不在答案中

3. **遊戲目標**:
   - 在6次內猜出正確單字

### 操作方式
```
A-Z  : 輸入字母
ENTER: 提交猜測
BACKSPACE: 刪除字母
N    : 新遊戲（遊戲結束後）
Q    : 退出遊戲
```

## 💻 技術實現

### 核心算法

#### 1. 猜測檢查算法
處理重複字母的正確邏輯：
```python
def check_guess(guess, target):
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
            # 移除已使用的字母
            target_chars[target_chars.index(guess[i])] = None
    
    return result
```

#### 2. 鍵盤狀態更新
```python
def update_keyboard(letter, state):
    # 優先級：green > yellow > gray
    current = keyboard_state.get(letter, 'unused')
    
    if state == 'green':
        keyboard_state[letter] = 'green'
    elif state == 'yellow' and current != 'green':
        keyboard_state[letter] = 'yellow'
    elif current == 'unused':
        keyboard_state[letter] = 'gray'
```

### 單字庫
- 包含 500+ 個常見5字母英文單字
- 從常用單字中隨機選擇答案
- 只接受列表中的有效單字

### 視覺設計

#### 遊戲界面
```
       WORDLE - 猜單字
       
 C  R  A  N  E
 🟩 🟨 ⬜ ⬜ 🟩

 S  T  O  N  E
 🟨 ⬜ 🟩 ⬜ ⬜

 _  _  _  _  _

 _  _  _  _  _

 _  _  _  _  _

 _  _  _  _  _

Keyboard:
 Q  W  E  R  T  Y  U  I  O  P
  A  S  D  F  G  H  J  K  L
   Z  X  C  V  B  N  M

🟩[X] 🟨(X) ⬜ X

Type your guess and press ENTER
BACKSPACE: Delete  Q: Quit
```

#### 鍵盤顏色標記
- `[X]`: 綠色 - 正確位置
- `(X)`: 黃色 - 錯誤位置
- ` X `: 灰色 - 不在單字中
- ` X `: 未使用

### 重複字母處理

#### 範例 1: 目標 "ROBOT"，猜測 "FLOOR"
- F: 灰色（不存在）
- L: 灰色（不存在）
- O: 黃色（第一個O，存在但位置錯）
- O: 綠色（第二個O，位置正確）
- R: 黃色（存在但位置錯）

#### 範例 2: 目標 "SPEED"，猜測 "ERASE"
- E: 黃色（第一個E）
- R: 灰色（不存在）
- A: 灰色（不存在）
- S: 黃色（存在但位置錯）
- E: 綠色（第二個E，位置正確）

## 🎨 特色功能

1. **智能顏色提示**:
   - 正確處理重複字母
   - 清晰的視覺回饋
   - 優先級正確（綠>黃>灰）

2. **虛擬鍵盤**:
   - 顯示所有字母狀態
   - 方括號標記綠色字母
   - 圓括號標記黃色字母

3. **即時輸入反饋**:
   - 輸入時即時顯示
   - 反白顯示當前輸入
   - 只接受有效單字

4. **完整遊戲循環**:
   - 勝利/失敗畫面
   - 顯示正確答案
   - 快速開始新遊戲

## 🧪 測試要點

### 核心功能測試
- ✅ 正確位置標記為綠色
- ✅ 錯誤位置標記為黃色
- ✅ 不存在的字母標記為灰色
- ✅ 重複字母處理正確
- ✅ 只接受5字母單字
- ✅ 只接受有效英文單字

### 遊戲邏輯測試
- ✅ 最多6次猜測
- ✅ 猜中後遊戲結束
- ✅ 用完機會後遊戲結束
- ✅ 顯示正確答案

### 視覺測試
- ✅ 顏色清晰易辨
- ✅ 鍵盤狀態正確
- ✅ 界面不閃爍
- ✅ 輸入反饋即時

## 📊 開發數據

### 程式碼統計
- 總行數: ~350行
- 單字庫: 500+ 單字
- 主要類別:
  - `Wordle`: 主遊戲邏輯
  - 方法數: ~8個

### 關鍵方法
- `check_guess()`: 檢查猜測（處理重複字母）
- `update_keyboard()`: 更新鍵盤狀態
- `is_valid_guess()`: 驗證猜測
- `draw_keyboard()`: 繪製虛擬鍵盤

## 🎓 學習收穫

### 演算法設計
1. **兩遍掃描法**: 先綠後黃，避免重複計算
2. **狀態優先級**: 正確處理字母狀態更新
3. **字符標記**: 用None標記已使用字母

### 遊戲設計
1. **視覺回饋**: 顏色是最好的提示
2. **即時反饋**: 增強使用者體驗
3. **簡單規則**: 容易上手但有挑戰性

## 🌟 亮點與創新

1. **正確的重複字母處理**: 符合原版Wordle邏輯
2. **虛擬鍵盤顯示**: 清楚顯示字母狀態
3. **即時輸入**: 流暢的輸入體驗
4. **大量單字庫**: 500+常用單字

## 🎯 成就達成

✅ 完成第9個遊戲
✅ Puzzle & Logic 類別進展 (3/4)
✅ 純文字遊戲的最佳代表
✅ 熱門遊戲重現

## 📝 總結

Wordle 是純文字遊戲的完美範例：
- 簡單但有趣
- 顏色回饋系統完美
- 重複字母處理複雜但重要
- CLI環境表現出色

這是一個充滿邏輯思考和詞彙挑戰的遊戲，完美展示了文字遊戲在終端環境的魅力。重複字母的正確處理是技術重點。

---
**Day**: 9/10
**Status**: ✅ Complete
**Category**: Puzzle & Logic
**Difficulty**: Medium
**Fun Level**: ⭐⭐⭐⭐⭐

**Next**: Game 10 - Sokoban (推箱子) - THE FINAL GAME! 🎉
