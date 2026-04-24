import pygame, random, cv2, mediapipe as mp, sys, os

pygame.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

audio_ready = False
bgm_sound = None
bgm_channel = None

try:
    pygame.mixer.init()
    audio_ready = True
except Exception as e:
    print("AUDIO INIT ERROR:", e)

WIDTH, HEIGHT = 500, 700
LEVEL_TARGET_SCORE = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 26)
font_big = pygame.font.SysFont("Arial", 40)
font_level_up = pygame.font.SysFont("Arial", 48, bold=True)

# ================= SAFE LOAD (FIX CHẤM ĐỎ 100%) =================
def load(img, size):
    path = os.path.join(ASSETS_DIR, img)

    if os.path.isfile(path):
        try:
            return pygame.transform.scale(
                pygame.image.load(path).convert_alpha(),
                size
            )
        except Exception as e:
            print("LOAD ERROR:", path, e)

    print("MISSING:", path)
    s = pygame.Surface(size)
    s.fill((0, 255, 0))  # xanh = lỗi file
    return s


def load_sound(file):
    if not audio_ready:
        print("AUDIO DISABLED: cannot load sound", file)
        return None

    path = os.path.join(ASSETS_DIR, file)
    if os.path.isfile(path):
        try:
            return pygame.mixer.Sound(path)
        except Exception as e:
            print("SOUND ERROR:", path, e)
    return None


def play_bgm(file, volume=0.5):
    global bgm_sound, bgm_channel

    if not audio_ready:
        print("AUDIO DISABLED: cannot play music", file)
        return

    path = os.path.join(ASSETS_DIR, file)
    if not os.path.isfile(path):
        print("MISSING MUSIC:", path)
        return

    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
        print("BGM STARTED:", path)
    except Exception as e:
        print("MUSIC ERROR:", path, e)
        try:
            bgm_sound = pygame.mixer.Sound(path)
            bgm_sound.set_volume(volume)
            bgm_channel = bgm_sound.play(loops=-1)
            if bgm_channel:
                print("BGM FALLBACK STARTED:", path)
            else:
                print("BGM FALLBACK FAILED:", path)
        except Exception as fallback_error:
            print("BGM FALLBACK ERROR:", path, fallback_error)


# ================= ASSETS =================
car_img = load("car.png", (60, 100))
road_img = load("road.png", (WIDTH, HEIGHT))

obs_imgs = [
    load("obstacle1.png", (60, 80)),
    load("obstacle2.png", (60, 80)),
    load("obstacle3.png", (60, 80)),
]

crash_sound = load_sound("crash.wav")
boost_sound = load_sound("boost.wav")
play_bgm("music.wav")

# ================= CAMERA =================
cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(max_num_hands=1)

# ================= GAME VAR =================
lanes = [100, 220, 340]
lane_index = 1

car_x = lanes[lane_index]
target_x = lanes[lane_index]

car = pygame.Rect(car_x, 550, 60, 100)

obstacles = []

base_speed = 3
speed = base_speed
spawn_rate = 35

score = 0
lives = 3
road_y = 0

state = "menu"
difficulty = ""
total_score = 0


def set_difficulty(level_name):
    global base_speed, spawn_rate, difficulty, speed

    difficulty = level_name

    if level_name == "EASY":
        base_speed, spawn_rate = 3, 60
    elif level_name == "MEDIUM":
        base_speed, spawn_rate = 4, 40
    else:
        base_speed, spawn_rate = 5, 25

    speed = base_speed


def get_next_difficulty(level_name):
    order = ["EASY", "MEDIUM", "HARD"]

    if level_name not in order:
        return None

    index = order.index(level_name)
    if index + 1 < len(order):
        return order[index + 1]
    return None

# gesture
prev_y = None
gesture_cooldown = 0
move_delay = 0

boost_timer = 0
drift_timer = 0
level_up_timer = 0
level_up_text = ""

# ================= BUTTON =================
def draw_button(text, x, y, color):
    rect = pygame.Rect(x, y, 220, 70)
    pygame.draw.rect(screen, color, rect, border_radius=20)
    screen.blit(font.render(text, True, (0, 0, 0)), (x + 50, y + 20))
    return rect


# ================= MAIN LOOP =================
while True:
    screen.fill((0, 0, 0))

    # ================= MENU =================
    if state == "menu":
        screen.blit(font_big.render("HAND RACING", True, (255, 255, 255)), (110, 120))

        easy = draw_button("EASY", 140, 250, (0, 255, 100))
        med  = draw_button("MEDIUM", 140, 340, (255, 255, 0))
        hard = draw_button("HARD", 140, 430, (255, 80, 80))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                obstacles.clear()
                score = 0
                total_score = 0
                lives = 3
                boost_timer = 0
                drift_timer = 0
                level_up_timer = 0
                level_up_text = ""
                prev_y = None
                gesture_cooldown = 0
                move_delay = 0
                lane_index = 1
                car_x = lanes[lane_index]
                target_x = lanes[lane_index]

                if easy.collidepoint(e.pos):
                    set_difficulty("EASY")
                    state = "play"

                if med.collidepoint(e.pos):
                    set_difficulty("MEDIUM")
                    state = "play"

                if hard.collidepoint(e.pos):
                    set_difficulty("HARD")
                    state = "play"

    # ================= PLAY =================
    elif state == "play":

        # ================= CAMERA =================
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            cv2.imshow("Camera", frame)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = hands.process(rgb)

            move_delay += 1

            if res.multi_hand_landmarks and move_delay > 5:
                hand = res.multi_hand_landmarks[0]

                x = hand.landmark[8].x
                y = hand.landmark[8].y

                # lane control
                if x < 0.33:
                    lane_index = 0
                elif x < 0.66:
                    lane_index = 1
                else:
                    lane_index = 2

                target_x = lanes[lane_index]

                # gesture
                if prev_y is not None and gesture_cooldown == 0:
                    dy = y - prev_y

                    if dy < -0.08:
                        boost_timer = 120
                        speed = base_speed + 3
                        gesture_cooldown = 12
                        if boost_sound:
                            boost_sound.play()

                    elif dy > 0.08:
                        drift_timer = 20
                        gesture_cooldown = 12

                prev_y = y

        if cv2.waitKey(1) & 0xFF == ord('q'):
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

        # ================= SPEED =================
        if boost_timer > 0:
            boost_timer -= 1
        else:
            speed = base_speed

        if level_up_timer > 0:
            level_up_timer -= 1

        if gesture_cooldown > 0:
            gesture_cooldown -= 1

        # ================= ROAD =================
        road_y += speed
        if road_y >= HEIGHT:
            road_y = 0

        screen.blit(road_img, (0, road_y))
        screen.blit(road_img, (0, road_y - HEIGHT))

        # ================= CAR =================
        if drift_timer > 0:
            drift_timer -= 1
            car_x += (target_x - car_x) * 0.4
        else:
            car_x += (target_x - car_x) * 0.2

        car = pygame.Rect(int(car_x), 550, 60, 100)
        screen.blit(car_img, car)

        # ================= OBSTACLE (FIXED 100%) =================
        if random.randint(1, spawn_rate) == 1:
            obstacles.append({
                "rect": pygame.Rect(random.choice(lanes), -80, 60, 80),
                "img": random.choice(obs_imgs)
            })

        for o in obstacles:
            o["rect"].y += speed

            # DRAW (QUAN TRỌNG)
            screen.blit(o["img"], o["rect"])

            # COLLISION
            if o["rect"].colliderect(car):
                lives -= 1
                if crash_sound:
                    crash_sound.play()
                o["rect"].y = HEIGHT + 999

                if lives <= 0:
                    state = "gameover"

        obstacles = [o for o in obstacles if o["rect"].y < HEIGHT]

        # ================= UI =================
        score += 1
        total_score += 1

        if score >= LEVEL_TARGET_SCORE:
            next_difficulty = get_next_difficulty(difficulty)
            obstacles.clear()
            score = 0
            boost_timer = 0
            drift_timer = 0
            speed = base_speed

            if next_difficulty:
                set_difficulty(next_difficulty)
                level_up_text = f"LEVEL UP: {next_difficulty}"
                level_up_timer = 90
            else:
                state = "win"

        screen.blit(font.render(f"Level: {score}/{LEVEL_TARGET_SCORE}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Lives: {lives}", True, (255,100,100)), (10,40))
        screen.blit(font.render(f"{difficulty}", True, (255,255,255)), (10,70))
        screen.blit(font.render(f"Total: {total_score}", True, (255,255,255)), (10,100))

        if boost_timer > 0:
            screen.blit(font.render("BOOST!", True, (255,255,0)), (350,10))

        if level_up_timer > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, (0, 0))

            level_surface = font_level_up.render(level_up_text, True, (255, 255, 0))
            level_rect = level_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(level_surface, level_rect)

    # ================= GAME OVER =================
    elif state == "gameover":
        screen.blit(font_big.render("GAME OVER", True, (255,50,50)), (120,250))
        screen.blit(font.render("Click to menu", True, (255,255,255)), (150,320))

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                state = "menu"

    elif state == "win":
        screen.blit(font_big.render("YOU WIN!", True, (255, 255, 0)), (145, 250))
        screen.blit(font.render(f"Total score: {total_score}", True, (255,255,255)), (150, 320))
        screen.blit(font.render("Click to menu", True, (255,255,255)), (150, 360))

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                state = "menu"

    # ================= EXIT =================
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
