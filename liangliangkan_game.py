#!/usr/bin/env python3
"""
连连看 Lianliankan (冰箱食物版) - Python Version
使用 Pygame 库
"""

import pygame
import sys
import random

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (232, 245, 233)
SELECTED_COLOR = (255, 248, 225)
GREEN = (46, 125, 50)
BUTTON_COLOR = (255, 152, 0)

# 冰箱食物
FOODS = ['🥛', '🧈', '🥚', '🧀', '🥬', '🍅', '🥒', '🍌', '🍎', '🍊', '🍇', '🥕']

# 配置
COLS = 10
ROWS = 8
CELL_SIZE = 50
MARGIN = 30
SCREEN_WIDTH = COLS * CELL_SIZE + MARGIN * 2
SCREEN_HEIGHT = ROWS * CELL_SIZE + MARGIN * 2 + 80

# 初始化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("连连看 - 冰箱食物版")

font = pygame.font.SysFont('SimHei', 24)
small_font = pygame.font.SysFont('SimHei', 16)

class LianliankanGame:
    def __init__(self):
        self.cols = COLS
        self.rows = ROWS
        self.selected = None
        self.score = 0
        self.pairs_left = 0
        self.init_board()
    
    def init_board(self):
        """初始化棋盘"""
        total = self.cols * self.rows
        pairs = total // 2
        
        tiles = []
        for i in range(pairs):
            food = FOODS[i % len(FOODS)]
            tiles.append({'icon': food, 'id': i})
            tiles.append({'icon': food, 'id': i})
        
        random.shuffle(tiles)
        
        self.board = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(tiles[r * self.cols + c])
            self.board.append(row)
        
        self.pairs_left = pairs
    
    def draw_board(self):
        """绘制棋盘"""
        screen.fill(BG_COLOR)
        
        for row in range(self.rows):
            for col in range(self.cols):
                x = MARGIN + col * CELL_SIZE
                y = MARGIN + row * CELL_SIZE
                
                tile = self.board[row][col]
                if tile:
                    # 格子背景
                    color = SELECTED_COLOR if self.selected == (row, col) else WHITE
                    pygame.draw.rect(screen, color, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=8)
                    pygame.draw.rect(screen, (200, 200, 200), (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), 1, border_radius=8)
                    
                    # 食物图标
                    text = font.render(tile['icon'], True, BLACK)
                    text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                    screen.blit(text, text_rect)
    
    def draw_ui(self):
        """绘制UI"""
        # 剩余对数
        text = font.render(f"剩余: {self.pairs_left} 对", True, GREEN)
        screen.blit(text, (MARGIN, SCREEN_HEIGHT - 60))
        
        # 提示
        hint_text = small_font.render("按 H 提示  按 S 洗牌  按 R 重来", True, (100, 100, 100))
        screen.blit(hint_text, (MARGIN + 200, SCREEN_HEIGHT - 50))
        
        # 胜利
        if self.pairs_left == 0:
            win_text = font.render("🎉 恭喜通关!", True, BUTTON_COLOR)
            screen.blit(win_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 20))
    
    def get_click_pos(self, pos):
        """获取点击位置"""
        x, y = pos
        if MARGIN <= x < MARGIN + self.cols * CELL_SIZE and MARGIN <= y < MARGIN + self.rows * CELL_SIZE:
            col = (x - MARGIN) // CELL_SIZE
            row = (y - MARGIN) // CELL_SIZE
            if self.board[row][col]:
                return row, col
        return None
    
    def can_connect(self, p1, p2):
        """检查两点是否可以连接"""
        r1, c1 = p1
        r2, c2 = p2
        
        # 直连
        if self.check_line(r1, c1, r2, c2):
            return True
        
        # 一折
        if self.check_one_corner(r1, c1, r2, c2):
            return True
        
        # 两折
        if self.check_two_corners(r1, c1, r2, c2):
            return True
        
        return False
    
    def is_empty(self, r, c):
        """检查是否为空"""
        return r < 0 or r >= self.rows or c < 0 or c >= self.cols or self.board[r][c] is None
    
    def check_line(self, r1, c1, r2, c2):
        """检查直线连接"""
        if r1 == r2:
            min_c, max_c = min(c1, c2), max(c1, c2)
            for c in range(min_c + 1, max_c):
                if not self.is_empty(r1, c):
                    return False
            return True
        if c1 == c2:
            min_r, max_r = min(r1, r2), max(r1, r2)
            for r in range(min_r + 1, max_r):
                if not self.is_empty(r, c1):
                    return False
            return True
        return False
    
    def check_one_corner(self, r1, c1, r2, c2):
        """检查一折连接"""
        # 角1: (r1, c2)
        if self.is_empty(r1, c2) and self.check_line(r1, c1, r1, c2) and self.check_line(r1, c2, r2, c2):
            return True
        # 角2: (r2, c1)
        if self.is_empty(r2, c1) and self.check_line(r1, c1, r2, c1) and self.check_line(r2, c1, r2, c2):
            return True
        return False
    
    def check_two_corners(self, r1, c1, r2, c2):
        """检查两折连接"""
        # 扫描所有行
        for r in range(-1, self.rows + 1):
            if self.is_empty(r, c1) and self.is_empty(r, c2):
                if self.check_line(r1, c1, r, c1) and self.check_line(r, c1, r, c2) and self.check_line(r, c2, r2, c2):
                    return True
        
        # 扫描所有列
        for c in range(-1, self.cols + 1):
            if self.is_empty(r1, c) and self.is_empty(r2, c):
                if self.check_line(r1, c1, r1, c) and self.check_line(r1, c, r2, c) and self.check_line(r2, c, r2, c2):
                    return True
        
        return False
    
    def find_hint(self):
        """查找提示"""
        tiles = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]:
                    tiles.append((r, c, self.board[r][c]['id']))
        
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i][2] == tiles[j][2]:
                    if self.can_connect((tiles[i][0], tiles[i][1]), (tiles[j][0], tiles[j][1])):
                        return (tiles[i][0], tiles[i][1]), (tiles[j][0], tiles[j][1])
        return None
    
    def shuffle(self):
        """洗牌"""
        tiles = [self.board[r][c] for r in range(self.rows) for c in range(self.cols) if self.board[r][c]]
        random.shuffle(tiles)
        
        idx = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]:
                    self.board[r][c] = tiles[idx]
                    idx += 1
        
        self.selected = None
    
    def handle_click(self, pos):
        """处理点击"""
        cell = self.get_click_pos(pos)
        if not cell:
            return
        
        if not self.selected:
            self.selected = cell
        else:
            r1, c1 = self.selected
            r2, c2 = cell
            
            if (r1, c1) == (r2, c2):
                self.selected = None
            elif self.board[r1][c1]['id'] == self.board[r2][c2]['id']:
                if self.can_connect((r1, c1), (r2, c2)):
                    # 消除
                    self.board[r1][c1] = None
                    self.board[r2][c2] = None
                    self.pairs_left -= 1
                    self.selected = None
                else:
                    self.selected = cell
            else:
                self.selected = cell
    
    def reset(self):
        """重新开始"""
        self.selected = None
        self.init_board()

def main():
    game = LianliankanGame()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_h:
                    hint = game.find_hint()
                    if hint:
                        game.selected = hint[0]
                elif event.key == pygame.K_s:
                    game.shuffle()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
        
        game.draw_board()
        game.draw_ui()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
