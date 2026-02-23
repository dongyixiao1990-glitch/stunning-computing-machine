#!/usr/bin/env python3
"""
黑白棋 Reversi (Othello) - Python Version
使用 Pygame 库
支持 AI 对战，三个难度级别
"""

import pygame
import sys
import random

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
LIGHT_GREEN = (46, 204, 113)
GOLD = (243, 156, 18)
RED = (200, 50, 50)

# 棋盘配置
BOARD_SIZE = 8
CELL_SIZE = 60
MARGIN = 60
SCREEN_SIZE = BOARD_SIZE * CELL_SIZE + MARGIN * 2

# 初始化
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 100))
pygame.display.set_caption("黑白棋 Reversi - Python")

font = pygame.font.SysFont('SimHei', 24)
small_font = pygame.font.SysFont('SimHei', 16)

class Difficulty:
    EASY = 1
    MEDIUM = 2
    HARD = 3

class ReversiGame:
    def __init__(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        # 初始棋子
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2
        self.current_player = 1  # 1=黑棋(玩家), 2=白棋(AI)
        self.game_over = False
        self.winner = None
        self.valid_moves = []
        self.difficulty = Difficulty.MEDIUM
        self.ai_thinking = False
        self.update_valid_moves()
    
    def draw_board(self):
        """绘制棋盘"""
        screen.fill(GREEN)
        
        # 网格线
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(screen, BLACK,
                          (MARGIN, MARGIN + i * CELL_SIZE),
                          (SCREEN_SIZE - MARGIN, MARGIN + i * CELL_SIZE), 2)
            pygame.draw.line(screen, BLACK,
                          (MARGIN + i * CELL_SIZE, MARGIN),
                          (MARGIN + i * CELL_SIZE, SCREEN_SIZE - MARGIN), 2)
    
    def draw_pieces(self):
        """绘制棋子"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != 0:
                    x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
                    y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
                    
                    color = BLACK if self.board[row][col] == 1 else WHITE
                    pygame.draw.circle(screen, color, (x, y), 26)
                    if color == WHITE:
                        pygame.draw.circle(screen, BLACK, (x, y), 26, 1)
    
    def draw_valid_moves(self):
        """绘制有效落子位置"""
        for row, col in self.valid_moves:
            x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
            y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, GOLD, (x, y), 10)
    
    def draw_ui(self):
        """绘制UI"""
        # 统计
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(2) for row in self.board)
        
        # 分数板背景
        pygame.draw.rect(screen, WHITE, (MARGIN - 10, SCREEN_SIZE + 10, SCREEN_SIZE - MARGIN * 2 + 20, 80))
        pygame.draw.rect(screen, (200, 200, 200), (MARGIN - 10, SCREEN_SIZE + 10, SCREEN_SIZE - MARGIN * 2 + 20, 80), 1)
        
        stats = f"黑棋: {black_count}  白棋: {white_count}"
        text = font.render(stats, True, BLACK)
        screen.blit(text, (MARGIN + 80, SCREEN_SIZE + 20))
        
        # 当前玩家
        if self.ai_thinking:
            player_text = "AI 思考中..."
            color = RED
        else:
            player_text = f"当前: {'黑棋(你)' if self.current_player == 1 else '白棋(AI)'}"
            color = BLACK
        text = font.render(player_text, True, color)
        screen.blit(text, (MARGIN + 250, SCREEN_SIZE + 20))
        
        # 难度提示
        diff_names = {1: "简单", 2: "中等", 3: "困难"}
        diff_text = small_font.render(f"难度: 1-简单 2-中等 3-困难 (当前: {diff_names[self.difficulty]})", True, (100, 100, 100))
        screen.blit(diff_text, (MARGIN + 80, SCREEN_SIZE + 55))
        
        # 操作提示
        restart_text = small_font.render("按 R 重新开始", True, (100, 100, 100))
        screen.blit(restart_text, (MARGIN + 450, SCREEN_SIZE + 55))
        
        if self.game_over:
            if black_count > white_count:
                msg = "🎉 你获胜!"
                color = (0, 150, 0)
            elif white_count > black_count:
                msg = "🤖 AI获胜!"
                color = RED
            else:
                msg = "🤝 平局!"
                color = (100, 100, 100)
            result = font.render(msg, True, color)
            # 绘制半透明背景
            s = pygame.Surface((200, 60))
            s.set_alpha(220)
            s.fill(WHITE)
            screen.blit(s, (SCREEN_SIZE // 2 - 100, SCREEN_SIZE // 2 - 30))
            screen.blit(result, (SCREEN_SIZE // 2 - 60, SCREEN_SIZE // 2 - 20))
    
    def get_click_pos(self, pos):
        """获取点击位置"""
        x, y = pos
        row = (y - MARGIN) // CELL_SIZE
        col = (x - MARGIN) // CELL_SIZE
        
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None
    
    def get_flippable(self, row, col, player):
        """获取可以翻转的棋子"""
        if self.board[row][col] != 0:
            return []
        
        flippable = []
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        opponent = 2 if player == 1 else 1
        
        for dr, dc in directions:
            temp = []
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == opponent:
                temp.append((r, c))
                r += dr
                c += dc
            if temp and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                flippable.extend(temp)
        
        return flippable
    
    def update_valid_moves(self):
        """更新有效落子位置"""
        self.valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.get_flippable(row, col, self.current_player):
                    self.valid_moves.append((row, col))
    
    def make_move(self, row, col):
        """落子"""
        flippable = self.get_flippable(row, col, self.current_player)
        if not flippable:
            return False
        
        self.board[row][col] = self.current_player
        for r, c in flippable:
            self.board[r][c] = self.current_player
        
        # 切换玩家
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_valid_moves()
        
        # 检查游戏结束
        if not self.valid_moves:
            self.current_player = 2 if self.current_player == 1 else 1
            self.update_valid_moves()
            if not self.valid_moves:
                self.game_over = True
                black = sum(row.count(1) for row in self.board)
                white = sum(row.count(2) for row in self.board)
                if black > white:
                    self.winner = 1
                elif white > black:
                    self.winner = 2
        
        return True
    
    def ai_move(self):
        """AI 落子"""
        self.ai_thinking = True
        pygame.display.flip()
        
        # 延迟让玩家看到AI思考
        pygame.time.wait(500)
        
        if self.difficulty == Difficulty.EASY:
            move = self.ai_easy()
        elif self.difficulty == Difficulty.MEDIUM:
            move = self.ai_medium()
        else:
            move = self.ai_hard()
        
        if move:
            self.make_move(move[0], move[1])
        
        self.ai_thinking = False
    
    def ai_easy(self):
        """简单难度 - 随机落子"""
        if not self.valid_moves:
            return None
        return random.choice(self.valid_moves)
    
    def ai_medium(self):
        """中等难度 - 基础策略"""
        if not self.valid_moves:
            return None
        
        # 1. 尝试获胜
        for move in self.valid_moves:
            temp_board = [row[:] for row in self.board]
            row, col = move
            flippable = self.get_flippable(row, col, 2)
            if flippable:
                self.board[row][col] = 2
                for r, c in flippable:
                    self.board[r][c] = 2
                if self.check_win(2):
                    self.board = temp_board
                    return move
                self.board = temp_board
        
        # 2. 阻止对方获胜
        # 模拟玩家落子
        for move in self.valid_moves:
            temp_board = [row[:] for row in self.board]
            row, col = move
            flippable = self.get_flippable(row, col, 2)
            if flippable:
                self.board[row][col] = 2
                for r, c in flippable:
                    self.board[r][c] = 2
                # 检查玩家是否能获胜
                player_can_win = False
                for r in range(BOARD_SIZE):
                    for c in range(BOARD_SIZE):
                        if self.get_flippable(r, c, 1):
                            temp2 = [row[:] for row in self.board]
                            flip = self.get_flippable(r, c, 1)
                            self.board[r][c] = 1
                            for fr, fc in flip:
                                self.board[fr][fc] = 1
                            if self.check_win(1):
                                player_can_win = True
                            self.board = temp2
                self.board = temp_board
                if not player_can_win:
                    return move
        
        # 3. 随机落子
        return random.choice(self.valid_moves)
    
    def ai_hard(self):
        """困难难度 -  Minimax算法 + 评分"""
        if not self.valid_moves:
            return None
        
        best_score = -float('inf')
        best_move = None
        
        for move in self.valid_moves:
            score = self.minimax(move, 3, -float('inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def minimax(self, move, depth, alpha, beta, is_maximizing):
        """Minimax算法"""
        # 应用落子
        row, col = move
        flippable = self.get_flippable(row, col, 2 if is_maximizing else 1)
        
        if not flippable:
            return -1000
        
        temp_board = [r[:] for r in self.board]
        self.board[row][col] = 2 if is_maximizing else 1
        for r, c in flippable:
            self.board[r][c] = 2 if is_maximizing else 1
        
        if depth == 0:
            score = self.evaluate_board(2 if is_maximizing else 1)
            self.board = temp_board
            return score
        
        # 获取下一步合法落子
        next_player = 1 if not is_maximizing else 2
        moves = self.get_all_valid_moves(next_player)
        
        if not moves:
            # 游戏结束
            black = sum(row.count(1) for row in self.board)
            white = sum(row.count(2) for row in self.board)
            score = (white - black) * 100
            self.board = temp_board
            return score
        
        if is_maximizing:
            max_eval = -float('inf')
            for m in moves[:5]:  # 限制搜索数量
                eval = self.minimax(m, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.board = temp_board
            return max_eval
        else:
            min_eval = float('inf')
            for m in moves[:5]:
                eval = self.minimax(m, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.board = temp_board
            return min_eval
    
    def get_all_valid_moves(self, player):
        """获取所有合法落子"""
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.get_flippable(row, col, player):
                    moves.append((row, col))
        return moves
    
    def evaluate_board(self, player):
        """评估棋盘局势"""
        score = 0
        opponent = 1 if player == 2 else 2
        
        # 角点价值最高
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for r, c in corners:
            if self.board[r][c] == player:
                score += 100
            elif self.board[r][c] == opponent:
                score -= 100
        
        # 边点
        for i in range(1, 7):
            if self.board[0][i] == player:
                score += 20
            elif self.board[0][i] == opponent:
                score -= 20
            if self.board[7][i] == player:
                score += 20
            elif self.board[7][i] == opponent:
                score -= 20
            if self.board[i][0] == player:
                score += 20
            elif self.board[i][0] == opponent:
                score -= 20
            if self.board[i][7] == player:
                score += 20
            elif self.board[i][7] == opponent:
                score -= 20
        
        # 棋子数量
        player_count = sum(row.count(player) for row in self.board)
        opponent_count = sum(row.count(opponent) for row in self.board)
        score += (player_count - opponent_count) * 5
        
        # 行动力（合法落子数）
        player_moves = len(self.get_all_valid_moves(player))
        opponent_moves = len(self.get_all_valid_moves(opponent))
        score += (player_moves - opponent_moves) * 2
        
        return score
    
    def check_win(self, player):
        """检查是否获胜"""
        # 检查是否还能落子
        if self.get_all_valid_moves(player):
            return False
        
        # 检查对手是否能落子
        opponent = 1 if player == 2 else 2
        if self.get_all_valid_moves(opponent):
            return False
        
        # 计算最终分数
        black = sum(row.count(1) for row in self.board)
        white = sum(row.count(2) for row in self.board)
        
        if player == 1:
            return black > white
        else:
            return white > black
    
    def reset(self):
        """重新开始"""
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.ai_thinking = False
        self.update_valid_moves()

def main():
    game = ReversiGame()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_1:
                    game.difficulty = Difficulty.EASY
                elif event.key == pygame.K_2:
                    game.difficulty = Difficulty.MEDIUM
                elif event.key == pygame.K_3:
                    game.difficulty = Difficulty.HARD
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game.game_over and game.current_player == 1 and not game.ai_thinking:
                    pos = game.get_click_pos(event.pos)
                    if pos:
                        game.make_move(pos[0], pos[1])
        
        # AI 移动
        if not game.game_over and game.current_player == 2 and not game.ai_thinking:
            game.ai_move()
        
        game.draw_board()
        game.draw_valid_moves()
        game.draw_pieces()
        game.draw_ui()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
