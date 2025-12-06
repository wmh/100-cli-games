.PHONY: help run install clean test lint format

# 預設目標
help:
	@echo "100 CLI Games - Makefile Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make run          - 運行主選單"
	@echo "  make install      - 安裝依賴"
	@echo "  make clean        - 清理快取檔案"
	@echo "  make test         - 運行測試（如果有）"
	@echo "  make lint         - 檢查代碼風格"
	@echo "  make format       - 格式化代碼"
	@echo ""
	@echo "Game shortcuts:"
	@echo "  make day1         - 運行 Day 1: Breakout"
	@echo "  make day2         - 運行 Day 2: Snake"
	@echo "  make day3         - 運行 Day 3: Pong"
	@echo "  make day4         - 運行 Day 4: Space Invaders"
	@echo "  make day5         - 運行 Day 5: Tetris"
	@echo ""

# 運行主選單
run:
	@python3 main.py

# 安裝依賴
install:
	@echo "安裝 Python 依賴..."
	@pip3 install -r requirements.txt
	@echo "✅ 依賴安裝完成！"

# 清理快取檔案
clean:
	@echo "清理快取檔案..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ 清理完成！"

# 運行測試
test:
	@echo "運行測試..."
	@python3 -m pytest tests/ -v 2>/dev/null || echo "⚠️  沒有找到測試檔案"

# 代碼風格檢查
lint:
	@echo "檢查代碼風格..."
	@python3 -m pylint games/*.py utils/*.py main.py 2>/dev/null || echo "⚠️  需要安裝 pylint: pip3 install pylint"

# 格式化代碼
format:
	@echo "格式化代碼..."
	@python3 -m black games/ utils/ main.py 2>/dev/null || echo "⚠️  需要安裝 black: pip3 install black"

# === 遊戲快捷方式 ===

# Day 1: Breakout
day1:
	@echo "🎮 啟動 Day 1: Breakout (打磚塊)"
	@python3 games/game_001_breakout.py

# Day 2: Snake
day2:
	@echo "🎮 啟動 Day 2: Snake (貪吃蛇)"
	@python3 games/game_002_snake.py

# Day 3: Pong
day3:
	@echo "🎮 啟動 Day 3: Pong (乒乓球)"
	@python3 games/game_003_pong.py

# Day 4: Space Invaders
day4:
	@echo "🎮 啟動 Day 4: Space Invaders (太空侵略者)"
	@python3 games/game_004_space_invaders.py

# Day 5: Tetris
day5:
	@echo "🎮 啟動 Day 5: Tetris (俄羅斯方塊)"
	@python3 games/game_005_tetris.py

# 別名
breakout: day1
snake: day2
pong: day3
invaders: day4
tetris: day5

# 顯示專案資訊
info:
	@echo "📊 專案資訊"
	@echo "============================================"
	@echo "專案名稱: 100 CLI Games Challenge"
	@echo "完成進度: 5/100 遊戲"
	@echo ""
	@echo "已完成遊戲:"
	@echo "  1. Breakout (打磚塊)"
	@echo "  2. Snake (貪吃蛇)"
	@echo "  3. Pong (乒乓球)"
	@echo "  4. Space Invaders (太空侵略者)"
	@echo "  5. Tetris (俄羅斯方塊)"
	@echo ""
	@echo "Python 版本: $(shell python3 --version)"
	@echo "檔案統計:"
	@echo "  遊戲檔案: $(shell ls -1 games/game_*.py 2>/dev/null | wc -l)"
	@echo "  代碼行數: $(shell find games -name '*.py' -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $$1}')"
	@echo ""

# 開發模式 - 監看檔案變化並自動重啟
dev:
	@echo "🔄 開發模式（需要安裝 entr）"
	@echo "監看 Python 檔案變化..."
	@find . -name "*.py" | entr -r make run

# Git 相關
git-status:
	@git status --short

git-log:
	@git log --oneline -10

# 快速提交（僅供開發測試用，正式提交請遵循 WORKFLOW.md）
quick-commit:
	@echo "⚠️  這是快速測試用的 commit，正式開發請遵循 WORKFLOW.md"
	@git add .
	@git status --short
	@echo ""
	@echo "請輸入 commit 訊息（或 Ctrl+C 取消）:"
	@read -p "> " msg; git commit -m "$$msg"
