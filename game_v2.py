import pygame
import sys

# === SETUP ===
pygame.init()
WIDTH, HEIGHT = 720, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime Attacks Goblin")

clock = pygame.time.Clock()
FPS = 10

background = pygame.image.load("background.jpg").convert()
bg_scaled_height = HEIGHT
bg_scaled_width = int(background.get_width() * (HEIGHT / background.get_height()))
background = pygame.transform.scale(background, (bg_scaled_width, bg_scaled_height))
bg_x1 = 0
bg_x2 = background.get_width()
bg_speed = 3

# === CONSTANTS ===
SPRITE_SIZE = 16
SPRITE_SPACING = 2
SCALED_SIZE = 64

# === LOAD SPRITE SHEETS ===
slime_sheet = pygame.image.load("slime_sheet_v2.png").convert_alpha()
goblin_sheet = pygame.image.load("goblin_sheet_2.png").convert_alpha()

# === AUDIO ===
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
#pygame.mixer.music.get_volume(0.3)
#attack_sound=pygame.mixer.Sound("attack.wav")


# === FRAME EXTRACTION FUNCTION ===
def get_animation_frames(sheet, row, frame_count):
    frames = []
    for i in range(frame_count):
        x = i * (SPRITE_SIZE + SPRITE_SPACING)
        y = row * (SPRITE_SIZE + SPRITE_SPACING)
        frame = sheet.subsurface(pygame.Rect(x, y, SPRITE_SIZE, SPRITE_SIZE))
        frame = pygame.transform.scale(frame, (SCALED_SIZE, SCALED_SIZE))
        frames.append(frame)
    return frames

# === SLIME ANIMATIONS ===
slime_run_right = get_animation_frames(slime_sheet, row=5, frame_count=6)
slime_run_left = [pygame.transform.flip(f, True, False) for f in slime_run_right]
slime_attack_right = get_animation_frames(slime_sheet, row=3, frame_count=6)
slime_attack_left = [pygame.transform.flip(f, True, False) for f in slime_attack_right]

# === GOBLIN ANIMATIONS ===
goblin_run_left = get_animation_frames(goblin_sheet, row=5, frame_count=6)
goblin_die_anim = get_animation_frames(goblin_sheet, row=4, frame_count=6)

# === SLIME STATE ===

slime_jump = False 
gravity=1
slime_jump_velocity=0
ground_y=HEIGHT-SCALED_SIZE-20
slime_x, slime_y = 100, HEIGHT // 2
slime_velocity = 5
slime_direction = "right"
slime_frame_index = 0
slime_action = "run"
attack_timer = 0

# === GOBLIN STATE ===

goblin={
        "x":500,
        "y":HEIGHT // 2, 
        "health":3,
        "alive": True, 
        "frame": 0, 
        "death_index":0}

# === FONTS ===

font=pygame.font.SysFont(None, 36)
big_font=pygame.font.SysFont("Arial", 64, bold=True)

you_win=False 
you_win_timer=30

# === MAIN LOOP ===
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # === ATTACK WHEN DRAGGING MOUSE WITH LEFT BUTTON PRESSED ===
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and attack_timer == 0 and not you_win:
            slime_action = "attack"
            attack_timer = 3
            #attack_sound.play()
            distance = abs(slime_x - goblin["x"])
            if distance < 80 and goblin["alive"]:
                goblin["health"] -= 1
                if goblin["health"] <= 0:
                    goblin["alive"] = False

    keys = pygame.key.get_pressed()
    if attack_timer == 0 and not you_win:
        if keys[pygame.K_LEFT]:
            slime_x -= slime_velocity
            slime_direction = "left"
            slime_action = "run"
        elif keys[pygame.K_RIGHT]:
            slime_x += slime_velocity
            slime_direction = "right"
            slime_action = "run"
            
            
            
            
    # === SLIME JUMP UPDATE ===
    if keys[pygame.K_SPACE] and not slime_jump and not you_win: 
        slime_jump=True
        slime_jump_velocity=-15
    
    if slime_jump: 
        slime_y+=slime_jump_velocity
        slime_jump_velocity+=gravity
        if slime_y>=ground_y: 
            slime_y=ground_y
            slime_jump=False 
            
    
    
    # === SLIME FRAME UPDATE ===
    slime_frame_index += 1
    if slime_action == "attack":
        slime_frames = slime_attack_right if slime_direction == "right" else slime_attack_left
    else:
        slime_frames = slime_run_right if slime_direction == "right" else slime_run_left

    if slime_frame_index >= len(slime_frames):
        slime_frame_index = 0
        if slime_action == "attack":
            slime_action = "run"
            attack_timer = 0

    if attack_timer > 0:
        attack_timer -= 1

    # === GOBLIN FRAME UPDATE ===
    if goblin["alive"]:
        goblin["frame"] = (goblin["frame"]  + 1) % len(goblin_run_left)
    elif goblin["death_index"] < len(goblin_die_anim) - 1:
        goblin["death_index"]  += 1

    # === BACKGROUND SCROLL ===
    bg_x1 -= bg_speed
    bg_x2 -= bg_speed
    if bg_x1 <= -background.get_width():
        bg_x1 = bg_x2 + background.get_width()
    if bg_x2 <= -background.get_width():
        bg_x2 = bg_x1 + background.get_width()

    # === DRAW EVERYTHING ===
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))

    screen.blit(slime_frames[slime_frame_index], (slime_x, slime_y))

    if goblin["alive"]:
        screen.blit(goblin_run_left[goblin["frame"]], (goblin["x"], goblin["y"]))
    else:
        screen.blit(goblin_die_anim[goblin["death_index"]], (goblin["x"], goblin["y"]))

    # === DISPLAY GOBLIN HEALTH ===
    font = pygame.font.SysFont(None, 30)
    #health_text = font.render(f"Goblin HP: {goblin["health"}, True, (255, 50, 50))
    #screen.blit(health_text, (goblin["x"], goblin["y"] - 30))

    pygame.display.update()

pygame.quit()
sys.exit()
