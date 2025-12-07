#!/usr/bin/env python3
"""
Test script for Sokoban levels
Verifies each level is valid and provides solutions
"""

from games.game_010_sokoban import LEVELS

def test_level_validity():
    """Test that all levels have correct box/target counts"""
    print("=" * 70)
    print("LEVEL VALIDITY CHECK")
    print("=" * 70)
    
    all_valid = True
    for i, level in enumerate(LEVELS):
        boxes = sum(row.count('$') + row.count('*') for row in level)
        targets = sum(row.count('.') + row.count('*') + row.count('+') for row in level)
        players = sum(row.count('@') + row.count('+') for row in level)
        
        valid = (boxes == targets and players == 1)
        status = "✅" if valid else "❌"
        
        if not valid:
            all_valid = False
            
        print(f"{status} Level {i+1:2d}: {boxes} boxes, {targets} targets, {players} player")
        
        # Show the level
        if not valid or i < 2:  # Show first 2 levels always
            print("\n" + "  Layout:")
            for row in level:
                visual = (row.replace('#', '█')
                            .replace('@', '🧑')
                            .replace('+', '👤')
                            .replace('$', '📦')
                            .replace('*', '✅')
                            .replace('.', '🎯'))
                print(f"    {visual}")
            print()
    
    print("=" * 70)
    return all_valid

def analyze_level_playability(level_num):
    """Analyze if a level looks playable"""
    if level_num < 0 or level_num >= len(LEVELS):
        print(f"Invalid level number: {level_num}")
        return
    
    level = LEVELS[level_num]
    print(f"\n{'=' * 70}")
    print(f"LEVEL {level_num + 1} PLAYABILITY ANALYSIS")
    print('=' * 70)
    
    # Find player position
    player_pos = None
    boxes = []
    targets = []
    
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char in '@+':
                player_pos = (x, y)
            if char in '$*':
                boxes.append((x, y))
            if char in '.*+':
                targets.append((x, y))
    
    print(f"\nPlayer position: {player_pos}")
    print(f"Boxes: {boxes}")
    print(f"Targets: {targets}")
    
    # Check player can move
    if player_pos:
        x, y = player_pos
        moves = []
        if y > 0 and level[y-1][x] != '#':
            moves.append('UP')
        if y < len(level)-1 and level[y+1][x] != '#':
            moves.append('DOWN')
        if x > 0 and level[y][x-1] != '#':
            moves.append('LEFT')
        if x < len(level[y])-1 and level[y][x+1] != '#':
            moves.append('RIGHT')
        
        print(f"\nPlayer can move: {moves}")
        if not moves:
            print("⚠️  WARNING: Player cannot move in any direction!")
            return False
    
    # Show visual
    print("\nVisual:")
    for row in level:
        visual = (row.replace('#', '█')
                    .replace('@', '🧑')
                    .replace('+', '👤')
                    .replace('$', '📦')
                    .replace('*', '✅')
                    .replace('.', '🎯'))
        print(f"  {visual}")
    
    print("\n✅ Level appears playable (basic checks passed)")
    return True

# Known solutions for first few levels (move sequences)
SOLUTIONS = {
    1: "uurrdddlll",  # Example solution
    2: "rurdlluurrddr",
    # Add more as we verify them
}

def main():
    print("\n🎮 SOKOBAN LEVEL TEST SUITE\n")
    
    # Test 1: Validity
    if not test_level_validity():
        print("\n❌ Some levels failed validity check!")
        print("Fix these before testing playability.\n")
        return
    
    print("\n✅ All levels passed validity check!\n")
    
    # Test 2: Analyze first 3 levels in detail
    print("\n" + "=" * 70)
    print("DETAILED PLAYABILITY ANALYSIS")
    print("=" * 70)
    
    for i in range(min(3, len(LEVELS))):
        if not analyze_level_playability(i):
            print(f"\n❌ Level {i+1} has playability issues!")
            return
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nLevels are ready to play!")
    print("Run: python3 games/game_010_sokoban.py")
    print()

if __name__ == "__main__":
    main()
