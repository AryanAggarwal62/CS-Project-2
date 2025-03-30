"""
CSC111 Project: Pyramid-Style UI (Simplified)
============================================

A minimal Pygame interface that includes:
  - Text boxes for Platform and User ID.
  - Two sliders for weighting "Game Similarity" and "Achievement Similarity."
  - A Submit button to get matchmaking recommendations.

Assumptions:
  - A placeholder get_recommendations function which calls into your real
    graph logic (e.g. a function that takes platform, user_id, game_weight,
    achievement_weight).
  - You can visually arrange elements in a "pyramid" layout or any design
    you prefer. This code just places them in a simple vertical/horizontal arrangement.
"""

import pygame
import sys

def get_recommendations(platform: str, user_id: str,
                        game_weight: float,
                        achievement_weight: float) -> list[str]:
    """
    Return a list of recommended player IDs for the given parameters.

    platform: 'steam', 'xbox', or 'playstation'
    user_id:  a user identifier in that platform
    game_weight / achievement_weight: slider values indicating the
                                      relative importance of each similarity factor.

    TODO: finish this with graph
    """
    return []


class Slider:
    """
    A simple horizontal slider class for Pygame.
    Allows the user to drag a handle to select a float value between 0 and 1.
    """
    def __init__(self, x: int, y: int, width: int, height: int, initial_val: float = 0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_width = 20
        self.handle_height = height
        self.min_x = x
        self.max_x = x + width - self.handle_width
        self.handle_x = self.min_x + (self.max_x - self.min_x) * initial_val
        self.dragging = False

    def get_value(self) -> float:
        """Return the slider's value in [0, 1]."""
        return (self.handle_x - self.min_x) / (self.max_x - self.min_x)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Update handle position based on mouse events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_rect = pygame.Rect(self.handle_x, self.rect.y, self.handle_width, self.handle_height)
                if handle_rect.collidepoint(event.pos):
                    self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, _ = event.pos
                self.handle_x = max(self.min_x, min(self.max_x, mouse_x))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the slider track and handle on the given surface."""
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)

        handle_rect = pygame.Rect(self.handle_x, self.rect.y, self.handle_width, self.handle_height)
        pygame.draw.rect(surface, (50, 200, 50), handle_rect)


def run_pyramid_ui() -> None:
    """
    Run a Pygame UI that asks for:
      - Platform (input text)
      - User ID (input text)
      - 2 Sliders (Game Similarity, Achievement Similarity)
      - Submit button -> calls get_recommendations and displays results

    You can adapt the layout to a "pyramid" or any shape you like!
    """
    pygame.init()
    pygame.display.set_caption("CSC111: Pyramid UI for Player Matchmaking")

    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))

    base_font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 34)

    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (200, 200, 200)
    light_blue = (173, 216, 230)

    platform_input_box = pygame.Rect(50, 70, 140, 32)
    userid_input_box = pygame.Rect(50, 120, 140, 32)

    platform_text = ""
    userid_text = ""

    game_slider = Slider(50, 180, 200, 20, initial_val=0.5)
    ach_slider = Slider(50, 230, 200, 20, initial_val=0.5)

    button_rect = pygame.Rect(50, 280, 100, 32)
    button_color = gray
    button_text = "Submit"

    recommendations = []

    clock = pygame.time.Clock()
    running = True
    active_input = None

    while running:
        screen.fill(white)

        title_surf = title_font.render("Pyramid UI: Player Matchmaking", True, black)
        screen.blit(title_surf, (50, 20))
        pf_label_surf = base_font.render("Platform:", True, black)
        screen.blit(pf_label_surf, (platform_input_box.x, platform_input_box.y - 20))

        uid_label_surf = base_font.render("User ID:", True, black)
        screen.blit(uid_label_surf, (userid_input_box.x, userid_input_box.y - 20))

        gm_label = base_font.render(f"Game Similarity: {game_slider.get_value():.2f}", True, black)
        screen.blit(gm_label, (50, 160))

        ach_label = base_font.render(f"Achievement Similarity: {ach_slider.get_value():.2f}", True, black)
        screen.blit(ach_label, (50, 210))

        pygame.draw.rect(screen, gray, platform_input_box, 2)
        pygame.draw.rect(screen, gray, userid_input_box, 2)

        pf_surf = base_font.render(platform_text, True, black)
        screen.blit(pf_surf, (platform_input_box.x + 5, platform_input_box.y + 5))

        uid_surf = base_font.render(userid_text, True, black)
        screen.blit(uid_surf, (userid_input_box.x + 5, userid_input_box.y + 5))

        game_slider.draw(screen)
        ach_slider.draw(screen)

        pygame.draw.rect(screen, button_color, button_rect)
        btn_text_surf = base_font.render(button_text, True, black)
        btn_text_rect = btn_text_surf.get_rect(center=button_rect.center)
        screen.blit(btn_text_surf, btn_text_rect)

        y_offset = 80
        if recommendations:
            rec_header = base_font.render("Recommendations:", True, black)
            screen.blit(rec_header, (300, 70))
            y_offset = 100
            for rec in recommendations:
                rec_line = base_font.render(f"- {rec}", True, black)
                screen.blit(rec_line, (300, y_offset))
                y_offset += 25

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if platform_input_box.collidepoint(event.pos):
                    active_input = "platform"
                elif userid_input_box.collidepoint(event.pos):
                    active_input = "userid"
                else:
                    active_input = None

                if button_rect.collidepoint(event.pos):
                    button_color = light_blue
                else:
                    button_color = gray

            elif event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos):
                    game_val = game_slider.get_value()
                    ach_val = ach_slider.get_value()
                    recommendations = get_recommendations(platform_text, userid_text, game_val, ach_val)
                    button_color = gray

            elif event.type == pygame.KEYDOWN:
                if active_input == "platform":
                    if event.key == pygame.K_BACKSPACE:
                        platform_text = platform_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        platform_text += event.unicode
                elif active_input == "userid":
                    if event.key == pygame.K_BACKSPACE:
                        userid_text = userid_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        userid_text += event.unicode

            game_slider.handle_event(event)
            ach_slider.handle_event(event)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_pyramid_ui()
