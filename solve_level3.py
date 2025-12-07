#!/usr/bin/env python3
"""
Level 3 solver - manual step by step simulation
"""
from games.game_010_sokoban import LEVELS
import copy

def print_state(board, step_num, move=""):
    """Print current board state"""
    print(f"\n步驟 {step_num}: {move}")
    for y, row in enumerate(board):
        line = ""
        for x, char in enumerate(row):
            if char == '#':
                line += '█'
            elif char == '@':
                line += '🧑'
            elif char == '+':
                line += '👤'
            elif char == '$':
                line += '📦'
            elif char == '*':
                line += '✅'
            elif char == '.':
                line += '🎯'
            else:
                line += '  '
        print(f"  {line}")

def move_player(board, direction):
    """Simulate one move"""
    # Find player
    px, py = None, None
    for y, row in enumerate(board):
        for x, char in enumerate(row):
            if char in '@+':
                px, py = x, y
                break
        if px is not None:
            break
    
    if px is None:
        return board, False, "Player not found"
    
    # Direction vectors
    dirs = {
        'W': (0, -1), 'UP': (0, -1),
        'S': (0, 1), 'DOWN': (0, 1),
        'A': (-1, 0), 'LEFT': (-1, 0),
        'D': (1, 0), 'RIGHT': (1, 0)
    }
    
    if direction not in dirs:
        return board, False, "Invalid direction"
    
    dx, dy = dirs[direction]
    nx, ny = px + dx, py + dy
    
    # Check bounds
    if ny < 0 or ny >= len(board) or nx < 0 or nx >= len(board[ny]):
        return board, False, "Out of bounds"
    
    next_cell = board[ny][nx]
    
    # Hit wall
    if next_cell == '#':
        return board, False, "Hit wall"
    
    # Move to empty space or target
    if next_cell in ' .':
        new_board = [list(row) for row in board]
        # Clear current position
        new_board[py][px] = '.' if board[py][px] == '+' else ' '
        # Move player
        new_board[ny][nx] = '+' if next_cell == '.' else '@'
        return [''.join(row) for row in new_board], True, "Moved"
    
    # Try to push box
    if next_cell in '$*':
        bx, by = nx + dx, ny + dy
        # Check behind box
        if by < 0 or by >= len(board) or bx < 0 or bx >= len(board[by]):
            return board, False, "Can't push - out of bounds"
        
        behind = board[by][bx]
        if behind == '#':
            return board, False, "Can't push - wall behind"
        if behind in '$*':
            return board, False, "Can't push - box behind"
        
        # Can push!
        new_board = [list(row) for row in board]
        # Clear current player position
        new_board[py][px] = '.' if board[py][px] == '+' else ' '
        # Move player to box position
        new_board[ny][nx] = '+' if next_cell == '*' else '@'
        # Move box
        new_board[by][bx] = '*' if behind == '.' else '$'
        return [''.join(row) for row in new_board], True, f"Pushed box to ({bx},{by})"
    
    return board, False, "Unknown cell"

# Start with Level 3
level = list(LEVELS[2])
print("=" * 60)
print("Level 3 完整模擬解法")
print("=" * 60)

print_state(level, 0, "初始狀態")

# Try different solutions
solutions_to_try = [
    "AWWDDDSSWWAASSD",  # Complete solution
    "AWWDDDSSAAWWDDS",  # Try 2
]

for sol_num, solution in enumerate(solutions_to_try, 1):
    print(f"\n\n{'='*60}")
    print(f"嘗試解法 {sol_num}: {solution}")
    print('='*60)
    
    board = list(level)
    moves = solution.replace(' ', '')
    success = True
    
    for i, move in enumerate(moves, 1):
        board, ok, msg = move_player(board, move)
        if not ok:
            print(f"\n❌ 移動失敗於步驟 {i} ({move}): {msg}")
            success = False
            break
        print_state(board, i, f"{move} - {msg}")
    
    if success:
        # Check if solved
        boxes_on_targets = sum(row.count('*') for row in board)
        total_boxes = sum(row.count('$') + row.count('*') for row in board)
        if boxes_on_targets == total_boxes:
            print(f"\n✅ 成功！所有箱子都在目標上！")
            print(f"\n正確解法：{solution}")
            break
        else:
            print(f"\n⚠️  未完成：{boxes_on_targets}/{total_boxes} 箱子在目標上")
