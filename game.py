import pgzrun
from pygame import Rect
import math
import random

# --- Configurações Globais ---
WIDTH, HEIGHT = 800, 400
TITLE = "Roguelike Adventure"
CELL_SIZE = 16
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

game_state = "menu"
music_enabled, sounds_enabled = True, True
resume_button_visible = False

# --- Classes de Interface ---
class Button:
    """Representa um botão interativo no menu do jogo."""
    def __init__(self, text, center_pos):
        self.text = text
        self.rect = Rect(center_pos[0] - 100, center_pos[1] - 25, 200, 50)
        self.hover = False

    def draw(self):
        color = (150, 150, 150) if self.hover else (100, 100, 100)
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(self.text, center=self.rect.center, fontsize=30, color="white")

    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

# --- Classes de Entidade ---
class Hero:
    """Classe do personagem principal controlado pelo jogador."""
    def __init__(self):
        self.grid_x, self.grid_y = 2, 2
        self.target_x, self.target_y = self.grid_x, self.grid_y
        self.actor = Actor("hero_idle1", (self.grid_x * CELL_SIZE, self.grid_y * CELL_SIZE))
        self.is_moving = False
        self.health = 5
        self.invulnerable, self.invulnerable_timer = False, 0
        self.attack_power = 1
        self.is_attacking = False
        self.attack_frame = 0
        self.attack_timer = 0
        self.attack_speed = 0.05
        self.anim_timer = 0
        self.anim_frame = 0

    def attack(self):
        """Ataca todos os inimigos em uma área maior ao redor do herói (2 tiles de distância)."""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_frame = 0
            for enemy in enemies:
                dx = abs(self.grid_x - enemy.grid_x)
                dy = abs(self.grid_y - enemy.grid_y)
                if dx <= 2 and dy <= 2:  # Área de ataque aumentada
                    enemy.health -= self.attack_power

    def draw(self):
        """Desenha o herói e a animação de ataque, se aplicável."""
        if not self.invulnerable or int(self.invulnerable_timer * 10) % 2 == 0:
            self.actor.draw()
            if self.is_attacking and 0 <= self.attack_frame <= 7:
                attack_img = f"attack/ani_attack_{self.attack_frame + 1:02}"
                attack_actor = Actor(attack_img, self.actor.pos)
                attack_actor.draw()

    def update(self):
        """Atualiza animação, movimentação e estado do herói."""
        import pgzero.builtins
        # Animação idle/movimento
        self.anim_timer += 1/60
        if self.anim_timer > 0.3:
            self.anim_timer = 0
            self.anim_frame = 1 - self.anim_frame
        if not self.is_moving and not self.is_attacking:
            img = f"hero_idle{self.anim_frame+1}"
            self.actor.image = img
        elif self.is_moving and not self.is_attacking:
            img = f"hero_move{self.anim_frame+1}"
            self.actor.image = img
        # Movimento contínuo
        dx = int(pgzero.builtins.keyboard.right) - int(pgzero.builtins.keyboard.left)
        dy = int(pgzero.builtins.keyboard.down) - int(pgzero.builtins.keyboard.up)
        if not self.is_moving and not self.is_attacking:
            if dx != 0 or dy != 0:
                new_x, new_y = self.grid_x + dx, self.grid_y + dy
                if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and world_grid[new_y][new_x] == 0:
                    self.target_x, self.target_y = new_x, new_y
                    self.is_moving = True
                    if sounds_enabled:
                        sounds.step.play()
        if self.is_moving:
            curr_x, curr_y = self.actor.pos
            target_pos = (self.target_x * CELL_SIZE, self.target_y * CELL_SIZE)
            dx, dy = target_pos[0] - curr_x, target_pos[1] - curr_y
            dist = (dx**2 + dy**2) ** 0.5
            if dist > 2:
                self.actor.pos = (curr_x + dx / dist * 2, curr_y + dy / dist * 2)
            else:
                self.actor.pos = target_pos
                self.grid_x, self.grid_y, self.is_moving = self.target_x, self.target_y, False
        if self.is_attacking:
            self.attack_timer += 1 / 60
            if self.attack_timer >= self.attack_speed:
                self.attack_timer = 0
                self.attack_frame += 1
                if self.attack_frame > 7:
                    self.is_attacking = False
        if self.invulnerable:
            self.invulnerable_timer += 1 / 60
            if self.invulnerable_timer >= 0.5:
                self.invulnerable, self.invulnerable_timer = False, 0

class Enemy:
    """Classe dos inimigos que patrulham pontos fixos no mapa."""
    def __init__(self, x, y, patrol_points):
        self.grid_x, self.grid_y = x, y
        self.actor = Actor("enemy_idle1", (self.grid_x * CELL_SIZE, self.grid_y * CELL_SIZE))
        # Patrulha maior: pontos mais distantes
        self.patrol_points = patrol_points
        self.target_x, self.target_y = self.grid_x, self.grid_y
        self.is_moving, self.current_point = False, 0
        self.health = 3
        self.anim_timer = 0
        self.anim_frame = 0
        self.speed = 0.2  # Muito mais lento

    def update(self):
        """Atualiza animação e movimentação do inimigo."""
        self.anim_timer += 1/60
        if self.anim_timer > 0.3:
            self.anim_timer = 0
            self.anim_frame = 1 - self.anim_frame
        if not self.is_moving:
            img = f"enemy_idle{self.anim_frame+1}"
            self.actor.image = img
        else:
            img = f"enemy_move{self.anim_frame+1}"
            self.actor.image = img
        # Patrulha
        if not self.is_moving:
            target = self.patrol_points[self.current_point]
            if (self.grid_x, self.grid_y) != target:
                self.target_x, self.target_y = target
                self.is_moving = True
            else:
                self.current_point = (self.current_point + 1) % len(self.patrol_points)
        if self.is_moving:
            curr_x, curr_y = self.actor.pos
            target_pos = (self.target_x * CELL_SIZE, self.target_y * CELL_SIZE)
            dx, dy = target_pos[0] - curr_x, target_pos[1] - curr_y
            dist = (dx**2 + dy**2) ** 0.5
            if dist > 1.5:
                self.actor.pos = (curr_x + dx / dist * self.speed, curr_y + dy / dist * self.speed)
            else:
                self.actor.pos = target_pos
                self.grid_x, self.grid_y, self.is_moving = self.target_x, self.target_y, False

    def draw(self):
        """Desenha o inimigo na tela."""
        self.actor.draw()

# --- Classe do Menu ---
class GameMenu:
    """Gerencia o menu principal e suas interações."""
    def __init__(self):
        self.buttons = {
            'resume': Button("Resume Game", (WIDTH // 2, HEIGHT // 2 - 90)),
            'start': Button("Start Game", (WIDTH // 2, HEIGHT // 2 - 30)),
            'sound': Button(f"Sound: {'ON' if sounds_enabled else 'OFF'}", (WIDTH // 2, HEIGHT // 2 + 30)),
            'music': Button(f"Music: {'ON' if music_enabled else 'OFF'}", (WIDTH // 2, HEIGHT // 2 + 90)),
            'exit': Button("Exit", (WIDTH // 2, HEIGHT // 2 + 150))
        }

    def draw(self):
        """Desenha o menu e seus botões."""
        screen.draw.text(TITLE, center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color="white")
        for name, button in self.buttons.items():
            if name == 'resume' and not resume_button_visible:
                continue
            button.draw()

    def handle_click(self, pos):
        """Gerencia cliques nos botões do menu."""
        global game_state, music_enabled, sounds_enabled, resume_button_visible
        for name, button in self.buttons.items():
            if button.rect.collidepoint(pos):
                if name == 'resume' and resume_button_visible:
                    game_state = "playing"
                elif name == 'start':
                    game_state = "playing"
                    if music_enabled:
                        music.play("background")
                elif name == 'sound':
                    sounds_enabled = not sounds_enabled
                    button.text = f"Sound: {'ON' if sounds_enabled else 'OFF'}"
                elif name == 'music':
                    music_enabled = not music_enabled
                    button.text = f"Music: {'ON' if music_enabled else 'OFF'}"
                elif name == 'exit':
                    exit()

    def handle_mouse_move(self, pos):
        """Atualiza o estado de hover dos botões do menu."""
        for name, button in self.buttons.items():
            if name == 'resume' and not resume_button_visible:
                continue
            button.check_hover(pos)

# --- Funções de Controle do Jogo ---
def reset_game():
    """Reinicia o herói e os inimigos para o início do jogo."""
    global hero, enemies
    hero = Hero()
    enemies = [
        Enemy(7, 7, [(7, 7), (15, 7), (15, 15), (7, 15)]),
        Enemy(3, 3, [(3, 3), (3, 12), (12, 12), (12, 3)]),
        Enemy(10, 5, [(10, 5), (18, 5), (18, 10), (10, 10)]),  # Novo inimigo
        Enemy(5, 15, [(5, 15), (5, 18), (8, 18), (8, 15)])     # Novo inimigo
    ]

# --- Geração do Mapa ---
world_grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
for _ in range(10):
    x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
    world_grid[y][x] = 1

reset_game()
menu = GameMenu()

# --- Loop Principal do Jogo ---
def update():
    """Atualiza o estado do jogo, entidades e música a cada frame."""
    global game_state
    # Música do menu e do jogo (apenas background.mp3)
    if music_enabled and not music.is_playing("background"):
        music.play("background")
    elif not music_enabled and music.is_playing("background"):
        music.stop()
    if game_state == "playing":
        hero.update()
        for enemy in enemies[:]:
            enemy.update()
            if enemy.health <= 0:
                enemies.remove(enemy)
        if not enemies:
            game_state = "gameover"
        else:
            for enemy in enemies:
                if hero.actor.colliderect(enemy.actor) and not hero.invulnerable:
                    hero.health -= 1
                    hero.invulnerable = True
                    if hero.health <= 0:
                        game_state = "menu"
                        reset_game()

# --- Função de Desenho ---
def draw():
    """Desenha o estado atual do jogo na tela."""
    screen.clear()
    if game_state in ["menu", "paused"]:
        menu.draw()
    elif game_state == "gameover":
        screen.draw.text("Fim de Jogo! Você venceu!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="yellow")
        screen.draw.text("Pressione ESC para sair", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=40, color="white")
    else:
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                screen.blit("floor", (x * CELL_SIZE, y * CELL_SIZE))
                if world_grid[y][x] == 1:
                    screen.blit("wall", (x * CELL_SIZE, y * CELL_SIZE))
        hero.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text(f"Health: {hero.health}", (10, 10), color="white")
        screen.draw.text("Pause = P", (WIDTH -100, 10), color="white")

# --- Eventos de Entrada ---
def on_mouse_down(pos):
    """Gerencia cliques do mouse no menu."""
    if game_state in ["menu", "paused"]:
        menu.handle_click(pos)

def on_mouse_move(pos):
    """Gerencia movimento do mouse para hover no menu."""
    if game_state in ["menu", "paused"]:
        menu.handle_mouse_move(pos)

def on_key_down(key):
    """Gerencia teclas pressionadas para pausa, ataque e sair do jogo."""
    global game_state, resume_button_visible
    if key == keys.P and game_state == "playing":
        game_state = "paused"
        resume_button_visible = True
    elif key == keys.SPACE and game_state == "playing":
        hero.attack()
    elif key == keys.ESCAPE and game_state == "gameover":
        exit()

pgzrun.go()