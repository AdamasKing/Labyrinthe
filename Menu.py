import pygame
import subprocess

pygame.init()

# Constantes

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu de jeu")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

BACKGROUND_MENU = pygame.image.load("arrière-du-menu.jpeg")
BACKGROUND_MENU = pygame.transform.scale(BACKGROUND_MENU, (WIDTH, HEIGHT))

font = pygame.font.Font(None, 36)

# dessin du bouton
def draw_button(screen, color, x, y, width, height, text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

#boucle principale

def main():
    button_rect = pygame.Rect(WIDTH // 2.55, 400, 200, 60)

    running = True
    while running:
        screen.blit(BACKGROUND_MENU, (0, 0))

        # texte afficher
        texte1 = font.render("Le Labyrinthe de Dédale", True, (255, 255, 255))
        screen.blit(texte1, (WIDTH // 2 - texte1.get_width() // 2, HEIGHT // 3))

        texte2 = font.render("Cliquer pour jouer", True, (255, 255, 255))
        screen.blit(texte2, (WIDTH // 2 - texte2.get_width() // 2, HEIGHT // 2))

        # obtenir la position de la souris
        mouse_pos = pygame.mouse.get_pos()

        # vérifier si la souris est sur le bouton
        if button_rect.collidepoint(mouse_pos):
            button_color = LIGHT_BLUE
        else:
            button_color = BLUE

        # dessiner le bouton
        draw_button(screen, button_color, button_rect.x, button_rect.y, button_rect.width, button_rect.height, "Cliquer pour jouer")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # vérifie le clic de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Vous avez cliqué sur le bouton")
                    subprocess.run(["python", "Labyrinthe de dédale.py"])
                    pygame.quit()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
