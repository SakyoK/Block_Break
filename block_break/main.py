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

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.all_sprites.update()

            # Collision Ball-Paddle
            if pygame.sprite.collide_rect(self.ball, self.paddle):
                self.ball.speed_y *= -1

            # Collision Ball-Blocks
            hit_blocks = pygame.sprite.spritecollide(self.ball, self.blocks, True)
            if hit_blocks:
                self.ball.speed_y *= -1

            # Game Over Check
            if self.ball.rect.y > SCREEN_HEIGHT:
                self.ball.reset()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = BreakoutGame()
    game.run()