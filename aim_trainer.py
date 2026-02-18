import pygame
import random
import math
import sys

# --- Configuration & Constants ---
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aim Trainer Reference Demo")

# Color definitions (RGB)
COLOR_BG = (30, 30, 30)        # Dark Grey Background
COLOR_TARGET = (0, 255, 255)   # Cyan Target
COLOR_CENTER = (255, 255, 255) # White Center
COLOR_TEXT = (255, 255, 255)   # White Text
COLOR_ACCENT = (255, 100, 100) # Red Accent

# Game settings
TARGET_RADIUS = 30
GAME_DURATION = 30  # Seconds
FPS = 60

# Fonts
try:
    font_main = pygame.font.SysFont("Arial", 30)
    font_large = pygame.font.SysFont("Arial", 60, bold=True)
except:
    # Fallback if Arial is not available
    font_main = pygame.font.Font(None, 36)
    font_large = pygame.font.Font(None, 72)

class Target:
    """
    Represents the circular target that the player needs to click.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = TARGET_RADIUS
        self.respawn()

    def respawn(self):
        """Moves the target to a random position within valid screen bounds."""
        margin = 50
        # Ensure target doesn't spawn off-screen or behind UI text
        self.x = random.randint(margin, SCREEN_WIDTH - margin)
        self.y = random.randint(margin + 60, SCREEN_HEIGHT - margin)

    def draw(self, surface):
        """Draws the target as concentric circles."""
        # Outer circle
        pygame.draw.circle(surface, COLOR_TARGET, (self.x, self.y), self.radius)
        # Inner circle
        pygame.draw.circle(surface, COLOR_CENTER, (self.x, self.y), self.radius * 0.8)
        # Bullseye
        pygame.draw.circle(surface, COLOR_TARGET, (self.x, self.y), self.radius * 0.4)

    def is_clicked(self, mouse_pos):
        """
        Checks if the mouse click occurred within the target's radius.
        Uses the distance formula: sqrt((x2-x1)^2 + (y2-y1)^2)
        """
        mx, my = mouse_pos
        distance = math.sqrt((mx - self.x)**2 + (my - self.y)**2)
        return distance <= self.radius

def draw_text_centered(surface, text, font, color, y_offset=0):
    """Utility to draw text in the center of the screen."""
    text_surf = font.render(text, True, color)
    rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset))
    surface.blit(text_surf, rect)

def main():
    """Main game loop and state management."""
    clock = pygame.time.Clock()
    
    # Game States: MENU, PLAYING, GAMEOVER
    game_state = "MENU"
    
    score = 0
    start_ticks = 0
    target = Target()
    
    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "MENU":
                    # Start the game
                    game_state = "PLAYING"
                    score = 0
                    start_ticks = pygame.time.get_ticks()
                    target.respawn()
                
                elif game_state == "PLAYING":
                    # Check for hits
                    if target.is_clicked(event.pos):
                        score += 1
                        target.respawn()
                
                elif game_state == "GAMEOVER":
                    # Return to menu
                    game_state = "MENU"

        # --- Update & Draw ---
        screen.fill(COLOR_BG)

        if game_state == "MENU":
            draw_text_centered(screen, "AIM TRAINER DEMO", font_large, COLOR_TARGET, -50)
            draw_text_centered(screen, "Click anywhere to Start", font_main, COLOR_TEXT, 50)

        elif game_state == "PLAYING":
            # Calculate remaining time
            seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
            time_left = GAME_DURATION - seconds_passed
            
            if time_left <= 0:
                time_left = 0
                game_state = "GAMEOVER"
            
            # Draw game elements
            target.draw(screen)
            
            # Draw UI (Score and Time)
            score_text = font_main.render(f"Score: {score}", True, COLOR_TEXT)
            time_text = font_main.render(f"Time: {time_left:.1f}", True, COLOR_TEXT)
            screen.blit(score_text, (20, 20))
            screen.blit(time_text, (SCREEN_WIDTH - 150, 20))

        elif game_state == "GAMEOVER":
            draw_text_centered(screen, "SESSION COMPLETE", font_large, COLOR_ACCENT, -80)
            draw_text_centered(screen, f"Final Score: {score}", font_large, COLOR_TEXT, 0)
            
            # Calculate simple stats
            if GAME_DURATION > 0:
                kps = score / GAME_DURATION
                draw_text_centered(screen, f"Speed: {kps:.2f} hits/sec", font_main, COLOR_TEXT, 60)
            
            draw_text_centered(screen, "Click to Menu", font_main, (150, 150, 150), 120)

        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
