#!/usr/bin/env python3
"""
五子棋 Gobang (Five in a Row) - Python Version
使用 Pygame 库
"""

import pygame
import sys
from enum import Enum

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (240, 212, 160)  # 木纹色
LINE_COLOR = (0, 0, 0)
GRID_SIZE = 15
CELL_SIZE = 40
MARGIN = 60

# 初始化 Pygame
pygame.init()
SCREEN_SIZE = GRID_SIZE * CELL_SIZE + MARGIN * 2
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 80))
pygame.display.set_caption("五子棋 Gobang - Python")

# 字体
font = pygame.font.SysFont('SimHei', 24)
small_font = pygame.font.SysFont('SimHei', 18)

class Player(Enum):
    BLACK = 1
    WHITE = 2

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class GobangGame:
    def __init__(self):
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.current_player = Player.BLACK
        self.game_over = False
        self.winner = None
        self.difficulty = Difficulty.MEDIUM
        self.ai_thinking = False
        
    def draw_board(self):
        """绘制棋盘"""
        screen.fill(BG_COLOR)
        
        # 绘制网格线
        for i in range(GRID_SIZE):
            # 横线
            pygame.draw.line(screen, LINE_COLOR, 
                           (MARGIN, MARGIN + i * CELL_SIZE),
                           (SCREEN_SIZE - MARGIN, MARGIN + i * CELL_SIZE), 1)
            # 竖线
            pygame.draw.line(screen, LINE_COLOR,
                           (MARGIN + i * CELL_SIZE, MARGIN),
                           (MARGIN + i * CELL_SIZE, SCREEN_SIZE - MARGIN), 1)
        
        # 绘制星位 (天元和四角星)
        star_points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        for x, y in star_points:
            pygame.draw.circle(screen, BLACK, 
                             (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE), 4)
    
    def draw_pieces(self):
        """绘制棋子"""
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] != 0:
                    x = MARGIN + j * CELL_SIZE
                    y = MARGIN + i * CELL_SIZE
                    color = BLACK if self.board[i][j] == 1 else WHITE
                    
                    # 画棋子
                    pygame.draw.circle(screen, color, (x, y), 16)
                    if color == WHITE:
                        pygame.draw.circle(screen, BLACK, (x, y), 16, 1)
    
    def draw_ui(self):
        """绘制UI"""
        # 当前玩家
        player_text = f"当前: {'黑方' if self.current_player == Player.BLACK else '白方 (AI)'}"
        if self.ai_thinking:
            player_text = "AI 思考中..."
        
        text = font.render(player_text, True, BLACK)
        screen.blit(text, (MARGIN, SCREEN_SIZE + 10))
        
        # 难度选择
        diff_text = small_font.render("难度: 1-简单 2-中等 3-困难", True, (100, 100, 100))
        screen.blit(diff_text, (MARGIN + 200, SCREEN_SIZE + 15))
        
        # 重新开始
        restart_text = small_font.render("按 R 重新开始", True, (100, 100, 100))
        screen.blit(restart_text, (MARGIN + 450, SCREEN_SIZE + 15))
        
        # 游戏结束
        if self.game_over:
            winner_text = f"游戏结束! {'黑方' if self.winner == Player.BLACK else '白方'} 获胜!"
            result = font.render(winner_text, True, (200, 0, 0))
            screen.blit(result, (SCREEN_SIZE // 2 - 120, SCREEN_SIZE // 2))
    
    def get_click_pos(self, pos):
        """获取点击的棋盘位置"""
        x, y = pos
        if x < MARGIN or x > SCREEN_SIZE - MARGIN or y < MARGIN or y > SCREEN_SIZE - MARGIN:
            return None
        
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - MARGIN) / CELL_SIZE)
        
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return row, col
        return None
    
    def is_valid_move(self, row, col):
        """检查是否有效落子"""
        return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and self.board[row][col] == 0
    
    def check_win(self, row, col):
        """检查是否获胜"""
        player = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            
            # 正方向
            for i in range(1, 5):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] == player:
                    count += 1
                else:
                    break
            
            # 反方向
            for i in range(1, 5):
                r, c = row - dr * i, col - dc * i
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] == player:
                    count += 1
                else:
                    break
            
            if count >= 5:
                return True
        return False
    
    def make_move(self, row, col):
        """落子"""
        if not self.is_valid_move(row, col):
            return False
        
        player_val = 1 if self.current_player == Player.BLACK else 2
        self.board[row][col] = player_val
        
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True
        
        self.current_player = Player.WHITE if self.current_player == Player.BLACK else Player.BLACK
        return True
    
    def ai_move(self):
        """AI 落子 - 简单版"""
        self.ai_thinking = True
        pygame.display.flip()
        
        # 延迟让玩家看到AI思考
        pygame.time.wait(300)
        
        # 1. 尝试获胜
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    self.board[i][j] = 2
                    if self.check_win(i, j):
                        self.board[i][j] = 0
                        self.make_move(i, j)
                        self.ai_thinking = False
                        return
                    self.board[i][j] = 0
        
        # 2. 阻止对方获胜
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    self.board[i][j] = 1
                    if self.check_win(i, j):
                        self.board[i][j] = 0
                        self.make_move(i, j)
                        self.ai_thinking = False
                        return
                    self.board[i][j] = 0
        
        # 3. 随机落子（简单模式）
        if self.difficulty == Difficulty.EASY:
            empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0]
            if empty:
                import random
                row, col = random.choice(empty)
                self.make_move(row, col)
                self.ai_thinking = False
                return
        
        # 4. 评分落子（中等/困难）
        best_score = -float('inf')
        best_move = None
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    score = self.evaluate_position(i, j)
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            self.make_move(best_move[0], best_move[1])
        
        self.ai_thinking = False
    
    def evaluate_position(self, row, col):
        """评估位置分数"""
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            my_count = 0
            opp_count = 0
            empty_count = 0
            
            for i in range(1, 5):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    if self.board[r][c] == 2:
                        my_count += 1
                    elif self.board[r][c] == 1:
                        opp_count += 1
                    else:
                        empty_count += 1
                else:
                    break
            
            # 评分
            if my_count >= 4:
                score += 100000
            elif my_count == 3 and empty_count >= 1:
                score += 10000
            elif my_count == 2:
                score += 100
            
            if opp_count >= 4:
                score += 80000
            elif opp_count == 3 and empty_count >= 1:
                score += 5000
        
        return score
    
    def reset(self):
        """重新开始"""
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.current_player = Player.BLACK
        self.game_over = False
        self.winner = None

def main():
    game = GobangGame()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    game.difficulty = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD][int(pygame.key.name(event.key)) - 1]
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game.game_over and game.current_player == Player.BLACK:
                    pos = game.get_click_pos(event.pos)
                    if pos:
                        game.make_move(pos[0], pos[1])
        
        # AI 移动
        if not game.game_over and game.current_player == Player.WHITE:
            game.ai_move()
        
        # 绘制
        game.draw_board()
        game.draw_pieces()
        game.draw_ui()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
