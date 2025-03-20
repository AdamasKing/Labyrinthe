import pygame
import random
import subprocess

# Initialisation de Pygame
pygame.init()

# ----- Constantes -----
CELL_SIZE = 30              # Taille d'une cellule (en pixels)
COLS = 30                   # Nombre de colonnes
ROWS = 20                   # Nombre de lignes
WIDTH = COLS * CELL_SIZE    # Largeur de la fenêtre
HEIGHT = ROWS * CELL_SIZE   # Hauteur de la fenêtre

# Couleurs (R, G, B)
COLOR_EMPTY = (255, 255, 255)  # Blanc (espace libre)
COLOR_WALL  = (50, 50, 50)     # Gris foncé (mur)
COLOR_PLAYER = (255, 0, 0)     # Rouge (joueur)
COLOR_GRID  = (200, 200, 200)  # Gris clair pour dessiner les lignes de la grille
COLOR_VICTORY = (0, 255, 0)    # vert pour la case de victoire
BACKGROUND_MENU_PAUSE = pygame.image.load("Background menu.jpg")  # Arrière-plan du menu pause
BACKGROUND_MENU_PAUSE = pygame.transform.scale(BACKGROUND_MENU_PAUSE, (WIDTH, HEIGHT))  # Redimensionne l'arrière-plan du menu pause

# ----- Création de la fenêtre -----
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labyrinthe Dynamique")

# ----- Création de la grille (labyrinthe) -----
# 0 = espace libre, 1 = mur
grid = []
for row in range(ROWS):
    row_data = []
    for col in range(COLS):
        # Probabilité d'avoir un mur (ici 30% de murs)
        cell = 1 if random.random() < 0.3 else 0
        row_data.append(cell)
    grid.append(row_data)

#position de la case de victoire (colonne, ligne)
victory_pos = [random.randint(26, COLS - 1), random.randint(16, ROWS - 1)]
grid[victory_pos[1]][victory_pos[0]] = 0


# Position initiale du joueur (colonne, ligne)
player_pos = [0, 0]
grid[player_pos[1]][player_pos[0]] = 0  # S'assurer que la case du joueur est vide

# ----- Timer pour la mise à jour du labyrinthe -----
# On définit un événement personnalisé qui se déclenchera toutes les 2000 ms (2 secondes)
UPDATE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(UPDATE_EVENT, 3000)

current_screen = "game"  # Fenêtre du jeu, première fenêtre

# ----- Boucle principale -----
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)  # Limitation à 60 images par seconde

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ----- Gestion du jeu -----
        if current_screen == "game":
            # Mise à jour dynamique du labyrinthe toutes les 2 secondes
            if event.type == UPDATE_EVENT:
                # On modifie aléatoirement x cellules de la grille
                for _ in range(250):
                    rand_row = random.randint(0, ROWS - 1)
                    rand_col = random.randint(0, COLS - 1)
                    # Ne pas changer la case occupée par le joueur
                    if [rand_col, rand_row] == player_pos or [rand_col, rand_row] == victory_pos:
                        continue

                    # Inverser l'état : si c'est un mur, on le vide et vice-versa
                    grid[rand_row][rand_col] = 0 if grid[rand_row][rand_col] == 1 else 1
                directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                libre = False
                for d in directions:
                    if 0 <= player_pos[0] + d[0] < ROWS and 0 <= player_pos[1] + d[1] < COLS:
                        if grid[player_pos[1]+d[1]][player_pos[0]+d[0]] == 0:
                            libre = True
                if not libre:
                    random_directions = random.choice(directions)
                    while not (0 <= player_pos[0] + random_directions[0] < ROWS and 0 <= player_pos[1] + random_directions[1] < COLS):
                        random_directions = random.choice(directions)
                    grid[player_pos[1]+random_directions[1]][player_pos[0]+random_directions[0]] = 0

            # Gestion des déplacements du joueur avec les flèches du clavier
            elif event.type == pygame.KEYDOWN:
                new_pos = player_pos.copy()
                if event.key == pygame.K_LEFT:
                    new_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    new_pos[0] += 1
                elif event.key == pygame.K_UP:
                    new_pos[1] -= 1
                elif event.key == pygame.K_DOWN:
                    new_pos[1] += 1

                # Touche Echap
                if event.key == pygame.K_ESCAPE:
                    current_screen = "menu pause"

                # Vérifier que la nouvelle position est dans les limites de la grille
                if 0 <= new_pos[0] < COLS and 0 <= new_pos[1] < ROWS:
                    # Le joueur ne peut se déplacer que sur des cases vides
                    if grid[new_pos[1]][new_pos[0]] == 0:
                        player_pos = new_pos

                # Vérifie si la position du joueur est égal à celle de la case victoire
                def check_victory(player_pos, victory_pos):
                    return player_pos == victory_pos
                
                # Si oui, affiche une fenêtre de victoire
                if check_victory(player_pos, victory_pos):
                    subprocess.run(["python", "Menu.py"])

        # ----- Gestion du menu pause -----
        elif current_screen == "menu pause":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Touche "Entrée" pour recommencer
                    current_screen = "game"
                    player_pos = [0, 0]  # Reset la position du joueur
                    victory_pos = [random.randint(26, COLS - 1), random.randint(16, ROWS - 1)]
                    grid[victory_pos[1]][victory_pos[0]] = 0

    # ----- Affichage -----
    if current_screen == "game":
        screen.fill(COLOR_EMPTY)

        # Dessin de la grille
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                # Dessiner la case selon qu'elle est vide ou un mur
                if grid[row][col] == 1:
                    pygame.draw.rect(screen, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(screen, COLOR_EMPTY, rect)
                # Dessiner les contours de la grille
                pygame.draw.rect(screen, COLOR_GRID, rect, 1)

        # Dessiner le joueur
        player_rect = pygame.Rect(player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, COLOR_PLAYER, player_rect)

        # Dessiner la case victoire
        victory_rect = pygame.Rect(victory_pos[0] * CELL_SIZE, victory_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, COLOR_VICTORY, victory_rect)

    elif current_screen == "menu pause":
        screen.blit(BACKGROUND_MENU_PAUSE, (0, 0))  # Affichage de l'image du menu pause

        # Afficher texte
        font = pygame.font.Font(None, 36)
        text = font.render("EN PAUSE", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

        text2 = font.render("Press Enter to start again", True, (255, 255, 255))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()