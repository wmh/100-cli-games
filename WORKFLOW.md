# 開發工作流程 - 重要！⚠️

## 🚨 核心原則

### ❌ 絕對禁止
**未經測試和審查，不得 commit 或 push！**

## ✅ 正確的開發流程

### 每日遊戲開發步驟

#### 1. 規劃階段
- [ ] 創建 `days/day_XX/DAY_XX_PLAN.md`
- [ ] 設計遊戲機制
- [ ] 規劃技術實作

#### 2. 開發階段
- [ ] 創建遊戲檔案 `games/game_XXX_name.py`
- [ ] 實作遊戲邏輯
- [ ] 更新主選單 `utils/menu.py`
- [ ] 更新 `README.md`
- [ ] 更新 `GAMES_PLAN.md` 進度

#### 3. ⚠️ **測試階段（必須由使用者執行）**
```bash
# 測試遊戲
python3 games/game_XXX_name.py

# 測試主選單
python3 main.py
```

**測試檢查清單：**
- [ ] 遊戲可正常啟動
- [ ] 畫面無閃爍
- [ ] 控制正常
- [ ] 遊戲邏輯正確
- [ ] 無明顯 bug
- [ ] 遊戲結束正常
- [ ] 能返回選單

#### 4. ⏸️ **等待使用者確認**

**AI 應該說：**
```
✅ Day X 開發完成！

請測試：
python3 games/game_XXX_name.py

測試完成後，告訴我：
- "ok" 或 "通過" → 我會 commit & push
- "有問題" → 告訴我需要修改什麼
```

**絕對不要自動進行下一步！**

#### 5. 📝 Commit 階段（僅在使用者確認後）

**使用者確認後才執行：**
```bash
git add .
git commit -m "詳細的 commit 訊息"
```

#### 6. 🚀 Push 階段（僅在使用者確認後）

**使用者確認後才執行：**
```bash
git push origin main
```

#### 7. 📊 Post-Push 檢查

**Push 成功後立即執行：**
```bash
# 檢查並更新 repository description
gh repo view --json description
gh repo edit --description "🎮 100 CLI Games Challenge - One game per day! X/100 completed: [遊戲列表] ✅ | Flicker-free terminal games with Python & curses"
```

**更新內容：**
- [ ] 完成數量 (X/100)
- [ ] 最新完成的遊戲名稱
- [ ] 保持描述簡潔（GitHub 限制 350 字元）

## 🎯 AI 助手行為準則

### ✅ 應該做的
1. 開發完成後，**停下來**
2. 明確告訴使用者「請測試」
3. 列出測試指令
4. 等待使用者回饋
5. 只在使用者明確許可後才 commit/push

### ❌ 不應該做的
1. ❌ 開發完就直接 commit
2. ❌ commit 後直接 push
3. ❌ 沒經過使用者確認就進行下一個遊戲
4. ❌ 假設測試會通過
5. ❌ 跳過測試階段

## 📋 標準回應模板

### 開發完成時
```
🎮 Day X: [遊戲名稱] 開發完成！

📦 已創建/更新的檔案：
- games/game_XXX_name.py
- utils/menu.py (已更新)
- README.md (已更新)
- GAMES_PLAN.md (已更新進度)
- days/day_XX/DAY_XX_PLAN.md
- days/day_XX/DAY_XX_COMPLETE.md

🧪 請測試遊戲：
```bash
# 直接測試
python3 games/game_XXX_name.py

# 或從選單測試
python3 main.py
```

✅ 測試項目：
- [ ] 啟動正常
- [ ] 畫面流暢
- [ ] 控制正確
- [ ] 邏輯正確
- [ ] 無 bug

⏸️ 測試完成後請告訴我：
- "ok" / "通過" / "good" → 我會 commit & push
- "有問題" → 告訴我哪裡需要修改

⚠️ 我會等待您的確認，不會自動 commit/push
```

## 🔄 異常處理

### 如果發現問題
1. 使用者回報問題
2. AI 修正問題
3. 再次請使用者測試
4. 重複直到通過

### 如果已經誤 push
1. 立即道歉
2. 說明可以用 `git revert` 或 `git reset`
3. 等待使用者指示

## 📝 每日結束檢查

完成一天的工作前確認：
- [ ] 使用者已測試遊戲
- [ ] 使用者明確確認「ok」或「通過」
- [ ] 已獲得 commit 許可
- [ ] 已獲得 push 許可
- [ ] Push 成功
- [ ] Repository description 已更新
- [ ] 檔案已正確組織在 `days/day_XX/` 目錄

## 🎓 學習重點

**記住：**
> 開發者寫程式碼
> 測試者驗證品質
> 只有測試通過才能發布

**使用者是測試者和決策者**
**AI 是開發者和助手**

## 📁 檔案組織規則

### 目錄結構
```
100-cli-games/
├── days/                      # 每日開發記錄
│   ├── day_01/               # Day 1 的所有文檔
│   │   ├── DAY_01_PLAN.md
│   │   ├── DAY_01_COMPLETE.md
│   │   └── [其他開發筆記].md
│   ├── day_02/               # Day 2 的所有文檔
│   └── ...
├── games/                    # 遊戲代碼
│   ├── game_001_name.py
│   └── ...
├── utils/                    # 工具模組
├── README.md                 # 專案說明
├── GAMES_PLAN.md            # 遊戲計畫
└── WORKFLOW.md              # 本文件
```

### 命名規則
- 計畫文檔: `days/day_XX/DAY_XX_PLAN.md`
- 完成文檔: `days/day_XX/DAY_XX_COMPLETE.md`
- 遊戲代碼: `games/game_XXX_name.py`
- 除錯筆記: `days/day_XX/ISSUE_NAME.md`

---
**創建日期**: 2025-12-05
**最後更新**: 2025-12-06
**重要性**: ⭐⭐⭐⭐⭐
**必須遵守**: 是

⚠️ 每次開發新遊戲前，AI 應該重新閱讀此文件！
