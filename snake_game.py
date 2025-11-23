import sys
import pygame
import random
import json
import os # <--- ÚJ: Mappák kezeléséhez

# 1. Pygame inicializálása
pygame.init()
pygame.mixer.init() # <--- ÚJ: Hangrendszer indítása

# --- Általános beállítások ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Snake Game")

# Színek definiálása (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
GREEN = (0, 200, 0)
RED = (255, 50, 50)
PURPLE = (170, 0, 255)

# Játék sebesség és időzítés
FPS = 15 
CLOCK = pygame.time.Clock()

# Betűtípusok beállítása
FONT_XL = pygame.font.Font(None, 80) 
FONT_L = pygame.font.Font(None, 40)
FONT_M = pygame.font.Font(None, 30)

# Rács és Kígyó beállítások
CELL_SIZE = 20 
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Fájlbeállítások
HIGHSCORE_FILE = "highscores.json" 

# --- ÚTVONAL KERESŐ FÜGGVÉNY (PyInstallerhez) ---
def resource_path(relative_path):
    """ Megkeresi az abszolút útvonalat az erőforráshoz,
        akkor is, ha .exe-be van csomagolva. """
    try:
        # PyInstaller létrehoz egy átmeneti mappát _MEIPASS néven
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- HANGOK BETÖLTÉSE ---
def load_sound(filename):
    try:
        # Itt használjuk az új resource_path függvényt!
        # A "sounds" a mappa neve, a filename a fájl neve
        path = resource_path(os.path.join("sounds", filename)) 
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"Nem sikerült betölteni a hangot: {filename} ({e})")
        return None

# Itt töltjük be a konkrét fájlokat
sound_start = load_sound("start.ogg")
sound_eat = load_sound("eat.ogg")
sound_gameover = load_sound("gameover.ogg")


# ------------------------------------
# --- SEGÉDFÜGGVÉNYEK (Toplista és Név) ---
# ------------------------------------

def load_highscores():
    """Betölti a toplistát a JSON fájlból."""
    try:
        with open(HIGHSCORE_FILE, 'r', encoding='utf-8') as f:
            scores = json.load(f)
            scores.sort(key=lambda x: x['score'], reverse=True)
            return scores
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_highscores(scores):
    """Elmenti a toplistát a JSON fájlba."""
    try:
        with open(HIGHSCORE_FILE, 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=4)
    except IOError:
        pass

def get_player_name():
    """Kezeli a játékosnév beírását és megjeleníti a TOP 3-at."""
    name = ""
    input_active = True
    
    while input_active:
        highscores = load_highscores() 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10:
                    name += event.unicode
        
        SCREEN.fill(BLACK)
        
        # TOP 3 LISTA MEGJELENÍTÉSE
        leaderboard_title = FONT_L.render("TOP 3 PONTSZÁM", True, RED)
        SCREEN.blit(leaderboard_title, (SCREEN_WIDTH // 2 - leaderboard_title.get_width() // 2, 50))
        
        y_offset = 100
        for i, entry in enumerate(highscores[:3]):
            rank = i + 1
            entry_text = FONT_M.render(f"{rank}. {entry['name']}: {entry['score']}", True, WHITE)
            SCREEN.blit(entry_text, (SCREEN_WIDTH // 2 - entry_text.get_width() // 2, y_offset + i * 30))
        
        # Névbekérés
        title_text = FONT_L.render("Add meg a nevedet:", True, WHITE)
        name_text = FONT_L.render(name + "_", True, GREEN)
        instruction_text = FONT_M.render("Nyomd meg az ENTER-t", True, WHITE)

        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        SCREEN.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 + 110))
        
        pygame.display.update()
        CLOCK.tick(30)
        
    return name

def display_leaderboard(current_score, player_name):
    """Megjeleníti a toplistát a játék után."""
    
    highscores = load_highscores()
    
    if current_score > 0:
        highscores.append({"name": player_name, "score": current_score})
        highscores.sort(key=lambda x: x['score'], reverse=True)
        save_highscores(highscores[:10]) 

    leaderboard_running = True
    while leaderboard_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                leaderboard_running = False
                
        SCREEN.fill(BLACK)
        
        title_text = FONT_XL.render("TOPLISTA", True, RED)
        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        
        score_text = FONT_L.render(f"Pontszám: {current_score}", True, GREEN)
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150))
        
        y_offset = 250
        for i, entry in enumerate(highscores[:10]):
            rank = i + 1
            color = GREEN if entry['name'] == player_name and entry['score'] == current_score else WHITE
            
            entry_text = FONT_L.render(f"{rank}. {entry['name']}: {entry['score']}", True, color)
            SCREEN.blit(entry_text, (SCREEN_WIDTH // 2 - entry_text.get_width() // 2, y_offset + i * 40))
        
        exit_text = FONT_M.render("Nyomd meg az ESCAPE-et a kilépéshez", True, WHITE)
        SCREEN.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT - 50))
        
        pygame.display.update()
        CLOCK.tick(15)

def draw_score(surface, score):
    score_text = FONT_L.render(f"Pontszám: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))


# ------------------------------------
# --- KÍGYÓ ÉS ÉTEL OSZTÁLYOK ---
# ------------------------------------

class Snake:
    def __init__(self):
        self.x = GRID_WIDTH // 2 
        self.y = GRID_HEIGHT // 2
        self.body = [(self.x, self.y)] 
        self.direction = (1, 0) 
        
    def move(self, grow=False):
        current_x, current_y = self.body[0]
        dx, dy = self.direction
        
        new_x = current_x + dx
        new_y = current_y + dy

        # KÉPERNYŐ ÁTLÉPÉSE (Wrap Around)
        if new_x < 0:
            new_x = GRID_WIDTH - 1
        elif new_x >= GRID_WIDTH:
            new_x = 0
            
        if new_y < 0:
            new_y = GRID_HEIGHT - 1
        elif new_y >= GRID_HEIGHT:
            new_y = 0

        self.body.insert(0, (new_x, new_y))
        
        if not grow:
            self.body.pop()

    def check_eat(self, food):
        return self.body[0] == food.position

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def draw(self, surface):
        for segment in self.body:
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GREEN, rect)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        x = random.randrange(0, GRID_WIDTH)
        y = random.randrange(0, GRID_HEIGHT)
        self.position = (x, y)

    def draw(self, surface):
        x = self.position[0] * CELL_SIZE
        y = self.position[1] * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, PURPLE, rect)

# ------------------------------------
# --- FŐ JÁTÉKVEZÉRLÉS ---
# ------------------------------------

def run_game():
    
    # 1. Név bekérése és kezdőképernyő
    player_name = get_player_name()
    
    # Kezdőképernyő a Space megnyomásáig
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                intro = False

        SCREEN.fill(BLACK)
        title_text = FONT_XL.render("SNAKE GAME", True, GREEN)
        name_text = FONT_L.render(f"Játékos: {player_name}", True, WHITE)
        start_text = FONT_L.render("Nyomd meg a SPACE gombot a kezdéshez!", True, WHITE)
        
        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
        SCREEN.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        SCREEN.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.update()
        CLOCK.tick(15)
        
    # Játék objektumok létrehozása
    snake = Snake() 
    food = Food()
    score = 0
    
    # START HANG LEJÁTSZÁSA
    if sound_start:
        sound_start.play()
    
    running = True
    game_over = False

    while running:
        
        # 2. Események kezelése
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_ESCAPE:
                    running = False 
                    
                if not game_over: 
                    # Kígyó irányítása WASD
                    if event.key == pygame.K_w and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_s and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_a and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_d and snake.direction != (-1, 0):
                        snake.direction = (1, 0)

        if not game_over:
            
            # LOGIKA: Ütközés és Növekedés
            grow = False
            if snake.check_eat(food):
                grow = True
                food.randomize_position()
                score += 10
                # EVÉS HANG LEJÁTSZÁSA
                if sound_eat:
                    sound_eat.play() 
            
            snake.move(grow=grow)
            
            # GAME OVER LOGIKA: Összeütközés önmagával
            if snake.check_self_collision():
                game_over = True
                # HALÁL HANG LEJÁTSZÁSA
                if sound_gameover:
                    sound_gameover.play()
                
        # 3. Rajzolás / Képernyő frissítése
        
        SCREEN.fill(BLACK) 
        food.draw(SCREEN) 
        snake.draw(SCREEN) 
        draw_score(SCREEN, score)

        if game_over:
            # GAME OVER: megjelenítjük a toplistát, majd kilép a program
            display_leaderboard(score, player_name)
            running = False
            
        pygame.display.update()
        CLOCK.tick(FPS)
        
# 4. Program indítása
if __name__ == '__main__':
    run_game()
    pygame.quit()