#!/usr/bin/env python3
"""
消消乐 Match-3 (水果版) - Python Version
使用 Pygame 库
"""

import pygame
import sys
import random

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (255, 248, 231)
BUTTON_COLOR = (255, 152, 0)

# 水果表情
FRUITS = ['🍎', '🍊', '🍇', '🍌', '🥝', '🍓', '🍑', '🍒']

# 配置
BOARD_ROWS = 8
BOARD_COLS = 8
CELL_SIZE = 60
MARGIN = 50
SCREEN_WIDTH = BOARD_COLS * CELL_SIZE + MARGIN * 2
SCREEN_HEIGHT = BOARD_ROWS * CELL_SIZE + MARGIN * 2 + 100

# 初始化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("消消乐 Match-3 - Python")

font = pygame.font.SysFont('SimHei', 24)
small_font = pygame.font.SysFont('SimHei', 16)

class Match3Game:
    def __init__(self):
        self.board = [[random.choice(FRUITS) for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.selected = None
        self.score = 0
        self.moves = 0
        self.animating = False
        self.target_score = 1000
        
        # 确保初始没有匹配
        while self.find_matches():
            self.board = [[random.choice(FRUITS) for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    
    def draw_board(self):
        """绘制棋盘"""
        screen.fill(BG_COLOR)
        
        # 棋盘背景
        pygame.draw.rect(screen, WHITE, (MARGIN - 5, MARGIN - 5, 
                                        BOARD_COLS * CELL_SIZE + 10, 
                                        BOARD_ROWS * CELL_SIZE + 10), border_radius=10)
        
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                x = MARGIN + col * CELL_SIZE
                y = MARGIN + row * CELL_SIZE
                
                # 格子背景
                color = (245, 245, 245) if (row + col) % 2 == 0 else (240, 240, 240)
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                
                # 绘制水果
                if self.board[row][col]:
                    # 使用emoji渲染
                    text = font.render(self.board[row][col], True, BLACK)
                    text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                    screen.blit(text, text_rect)
                
                # 选中高亮
                if self.selected == (row, col):
                    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 3)
    
    def draw_ui(self):
        """绘制UI"""
        # 分数
        score_text = font.render(f"分数: {self.score}", True, BLACK)
        screen.blit(score_text, (MARGIN, SCREEN_HEIGHT - 70))
        
        # 步数
        moves_text = font.render(f"步数: {self.moves}", True, BLACK)
        screen.blit(moves_text, (MARGIN + 150, SCREEN_HEIGHT - 70))
        
        # 目标
        target_text = font.render(f"目标: {self.target_score}", True, (100, 100, 100))
        screen.blit(target_text, (MARGIN + 300, SCREEN_HEIGHT - 70))
        
        # 重新开始
        restart_text = small_font.render("按 R 重新开始", True, (100, 100, 100))
        screen.blit(restart_text, (MARGIN + 480, SCREEN_HEIGHT - 65))
        
        # 游戏结束
        if self.score >= self.target_score:
            win_text = font.render("🎉 恭喜过关!", True, (0, 180, 0))
            screen.blit(win_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2))
    
    def get_click_pos(self, pos):
        """获取点击位置"""
        x, y = pos
        if MARGIN <= x < MARGIN + BOARD_COLS * CELL_SIZE and MARGIN <= y < MARGIN + BOARD_ROWS * CELL_SIZE:
            col = (x - MARGIN) // CELL_SIZE
            row = (y - MARGIN) // CELL_SIZE
            return row, col
        return None
    
    def swap(self, pos1, pos2):
        """交换两个位置"""
        r1, c1 = pos1
        r2, c2 = pos2
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]
    
    def find_matches(self):
        """查找匹配"""
        matches = set()
        
        # 水平匹配
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS - 2):
                if self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] and self.board[row][col]:
                    matches.add((row, col))
                    matches.add((row, col+1))
                    matches.add((row, col+2))
        
        # 垂直匹配
        for col in range(BOARD_COLS):
            for row in range(BOARD_ROWS - 2):
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] and self.board[row][col]:
                    matches.add((row, col))
                    matches.add((row+1, col))
                    matches.add((row+2, col))
        
        return list(matches)
    
    def remove_matches(self, matches):
        """移除匹配的棋子"""
        points = len(matches) * 10
        if len(matches) > 3:
            points += (len(matches) - 3) * 20
        self.score += points
        
        for row, col in matches:
            self.board[row][col] = None
    
    def drop_pieces(self):
        """下落填充"""
        for col in range(BOARD_COLS):
            # 将列中的非空棋子下移
            empty_row = BOARD_ROWS - 1
            for row in range(BOARD_ROWS - 1, -1, -1):
                if self.board[row][col]:
                    self.board[empty_row][col] = self.board[row][col]
                    if empty_row != row:
                        self.board[row][col] = None
                    empty_row -= 1
            
            # 填充新棋子
            for row in range(empty_row, -1, -1):
                self.board[row][col] = random.choice(FRUITS)
    
    def process_matches(self):
        """处理匹配"""
        matches = self.find_matches()
        while matches:
            self.remove_matches(matches)
            self.drop_pieces()
            matches = self.find_matches()
    
    def handle_click(self, pos):
        """处理点击"""
        if self.animating:
            return
        
        cell = self.get_click_pos(pos)
        if not cell:
            return
        
        if not self.selected:
            self.selected = cell
        else:
            r1, c1 = self.selected
            r2, c2 = cell
            
            # 检查是否相邻
            if abs(r1 - r2) + abs(c1 - c2) == 1:
                self.swap(self.selected, cell)
                self.moves += 1
                
                # 检查是否有匹配
                if self.find_matches():
                    self.process_matches()
                else:
                    # 没有匹配，换回来
                    self.swap(self.selected, cell)
                    self.moves -= 1
            
            self.selected = None
    
    def reset(self):
        """重新开始"""
        self.board = [[random.choice(FRUITS) for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.selected = None
        self.score = 0
        self.moves = 0
        
        while self.find_matches():
            self.board = [[random.choice(FRUITS) for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def main():
    game = Match3Game()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
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
