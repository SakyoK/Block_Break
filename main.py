import pygame
import sys
from constants import *
from sprites import Paddle, Ball, Block

class BreakoutGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Breakout Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont(None, FONT_SIZE_LARGE)
        self.font_small = pygame.font.SysFont(None, FONT_SIZE_SMALL)
        
        # 状態管理
        self.state = "START"
        self.lives = LIVES
        self.reset_game()

    def reset_game(self):
        """ゲームの初期化（ライフが減った時やリトライ時）"""
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.paddle = Paddle()
        self.ball = Ball()
        self.all_sprites.add(self.paddle, self.ball)
        self.create_blocks()

    def create_blocks(self):
        for row in range(5):
            for col in range(SCREEN_WIDTH // (BLOCK_WIDTH + 5)):
                block = Block(col * (BLOCK_WIDTH + 5) + 10, row * (BLOCK_HEIGHT + 5) + 50)
                self.blocks.add(block)
                self.all_sprites.add(block)

    def draw_text(self, text, font, color, y_offset):
        """画面に中央揃えでテキストを表示"""
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
        self.screen.blit(surf, rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # キー入力による画面遷移
                if event.type == pygame.KEYDOWN:
                    if self.state == "START":
                        if event.key == pygame.K_SPACE:
                            self.state = "PLAYING"
                    elif self.state == "GAMEOVER" or self.state == "CLEAR": # CLEARを追加
                        if event.key == pygame.K_SPACE:
                            self.lives = LIVES
                            self.reset_game()
                            self.state = "PLAYING"

            self.screen.fill(BLACK)

            if self.state == "START":
                self.draw_text("BREAKOUT GAME", self.font_large, WHITE, -50)
                self.draw_text("Press SPACE to Start", self.font_small, YELLOW, 50)

            elif self.state == "PLAYING":
                self.all_sprites.update()

                # 当たり判定
                if pygame.sprite.collide_rect(self.ball, self.paddle):
                    self.ball.speed_y *= -1
                
                hit_blocks = pygame.sprite.spritecollide(self.ball, self.blocks, True)
                if hit_blocks:
                    self.ball.speed_y *= -1

                # 【追加】クリア判定：ブロックグループが空になったかチェック
                if not self.blocks:
                    self.state = "CLEAR"

                # ミス判定
                if self.ball.rect.y > SCREEN_HEIGHT:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.state = "GAMEOVER"
                    else:
                        self.ball.reset()

                self.all_sprites.draw(self.screen)
                self.draw_text(f"LIVES: {self.lives}", self.font_small, WHITE, -280)

            elif self.state == "CLEAR":
                # 【追加】クリア画面の表示
                self.draw_text("CONGRATULATIONS!", self.font_large, YELLOW, -50)
                self.draw_text("ALL BLOCKS CLEARED", self.font_small, WHITE, 20)
                self.draw_text("Press SPACE to Play Again", self.font_small, WHITE, 80)

            elif self.state == "GAMEOVER":
                self.draw_text("GAME OVER", self.font_large, RED, -50)
                self.draw_text("Press SPACE to Retry", self.font_small, WHITE, 50)

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = BreakoutGame()
    game.run()