# Snake 速度平衡修正

## 問題描述
左右移動和上下移動的速度差異很大

## 原因分析
終端字元的寬高比不是 1:1，而是約 1:2
- 字元寬度：約 1 單位
- 字元高度：約 2 單位

因此：
- 水平移動 1 格 = 實際視覺距離 1
- 垂直移動 1 格 = 實際視覺距離 2

結果：水平看起來比垂直快一倍！

## 解決方案

### 修正方式：雙倍水平距離
```python
# Before (不平衡)
direction = (1, 0)   # 左右移動 1 格
direction = (0, 1)   # 上下移動 1 格

# After (平衡)
direction = (2, 0)   # 左右移動 2 格 ✅
direction = (0, 1)   # 上下移動 1 格 ✅
```

### 具體修改

#### 1. 初始方向
```python
# 改為左右移動 2 格
self.direction = (2, 0)
self.next_direction = (2, 0)
```

#### 2. 初始蛇身位置
```python
# 調整間距為 2 格
self.snake = deque([
    (start_x, start_y), 
    (start_x-2, start_y),  # 改為 -2
    (start_x-4, start_y)   # 改為 -4
])
```

#### 3. 方向控制
```python
# 左右方向改為 ±2
if key == curses.KEY_LEFT:
    self.next_direction = (-2, 0)  # 改為 -2
elif key == curses.KEY_RIGHT:
    self.next_direction = (2, 0)   # 改為 2
    
# 上下方向保持 ±1
elif key == curses.KEY_UP:
    self.next_direction = (0, -1)  # 保持 -1
elif key == curses.KEY_DOWN:
    self.next_direction = (0, 1)   # 保持 1
```

#### 4. 食物生成對齊
```python
def spawn_food(self):
    x = random.randint(2, self.width - 3)
    # 確保 x 是偶數，對齊蛇的移動格子
    if x % 2 != 0:
        x += 1
    # ...
```

#### 5. 反向檢查
```python
# 檢查值改為 ±2
if dx != 2:    # 不是往右
    self.next_direction = (-2, 0)  # 可以往左
if dx != -2:   # 不是往左
    self.next_direction = (2, 0)   # 可以往右
```

## 效果對比

### Before (不平衡)
```
水平速度：████████ (快)
垂直速度：████     (慢)
比率：2:1 ❌
```

### After (平衡)
```
水平速度：████     (正常)
垂直速度：████     (正常)
比率：1:1 ✅
```

## 視覺效果

### 移動軌跡
```
Before:
■▓▓▓▓▓▓▓▓  (密集，快)
■
▓
▓           (稀疏，慢)
▓

After:
■ ▓ ▓ ▓    (均勻)
■
▓
▓
▓           (均勻)
```

## 其他考慮方案

### 方案 A：時間延遲調整 (未採用)
```python
# 水平移動時延遲加倍
if dx != 0:
    time.sleep(self.speed * 2)
else:
    time.sleep(self.speed)
```
❌ 缺點：會導致控制不一致

### 方案 B：雙倍水平距離 (已採用) ✅
```python
# 水平移動 2 格
self.direction = (2, 0)
```
✅ 優點：
- 簡單直接
- 控制一致
- 視覺平衡

### 方案 C：縮小遊戲區域寬度
❌ 缺點：浪費空間

## 測試要點

請確認：
- [ ] 左右移動速度舒適
- [ ] 上下移動速度舒適
- [ ] 左右和上下速度看起來一致
- [ ] 能正常吃到食物
- [ ] 轉彎流暢
- [ ] 沒有卡住或跳躍

---
**修正時間**: 2025-12-05
**狀態**: ✅ 已修正，待測試確認
