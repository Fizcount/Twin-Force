import pygame
import sys
from PIL import Image
import time
import random
import pygame.freetype  # Import pygame freetype untuk font lebih fleksibel
import warna

# Inisialisasi Pygame dan Mixer
pygame.init()
pygame.mixer.init()

# Variabel global untuk status time limit
time_limit_enabled = True  # Mulai dengan time limit diaktifkan


def toggle_time_limit():
    global time_limit_enabled
    time_limit_enabled = not time_limit_enabled

def play_main_menu_bgm():
    pygame.mixer.music.load("main_menu_bgm.mp3")  # Ganti dengan path ke BGM permainan
    pygame.mixer.music.play(-1, 0.0)  # Memutar BGM permainan, -1 untuk loop tak terbatas

# Fungsi untuk mengubah musik latar belakang saat masuk permainan
def play_game_bgm():
    pygame.mixer.music.load("game_bgm.mp3")  # Ganti dengan path ke BGM permainan
    pygame.mixer.music.play(-1, 0.0)  # Memutar BGM permainan, -1 untuk loop tak terbatas

# Fungsi untuk menghentikan musik saat game over atau kembali ke menu utama
def stop_bgm():
    pygame.mixer.music.stop()  # Hentikan musik saat game over atau kembali ke menu

    # Fungsi untuk memutar musik Game Over
def play_game_over_bgm():
    pygame.mixer.music.load("game_over_bgm.mp3")  # Ganti dengan path musik Game Over
    pygame.mixer.music.play(-1, 0.0)  # Memutar musik Game Over, -1 untuk loop tak terbatas

def BOM_RATE():
    return random.randint(100,200)

def ENEMY_RATE():
    return random.randint(10,20)

# Konstanta
WIDTH, HEIGHT = 700, 600  # Ukuran kanvas
FPS = 90
BULLET_SPEED = 35  # Kecepatan peluru
FIRE_RATE = 0.5 # Interval waktu dalam detik
ENEMY_SPEED = 2  # Kecepatan musuh
BOM_SPEED = 5 # Kecepatan bom
ENEMY_SPAWN_RATE = ENEMY_RATE() # Frekuensi munculnya musuh (setiap 30 frame)
BOM_SPAWN_RATE = BOM_RATE() # Frekuensi munculnya bom (setiap 30 frame)
ENEMY_BULLET_SPEED = 15 # Kecepatan peluru musuh
ENEMY_FIRE_RATE = 0.8  # Interval waktu tembakan musuh
BOSS_SPEED = 1
BOSS_BULLET_SPEED = 15
BOSS_FIRE_RATE = 4

# File untuk menyimpan high score
HIGH_SCORE_FILE = "high_score.txt"
HIGH_SCORE_FILE_TIME = "high_score_time.txt"

# Membaca high score dari file
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0  # Jika file tidak ditemukan atau isinya tidak valid, set high score ke 0

def load_high_score_time():
    try:
        with open(HIGH_SCORE_FILE_TIME, "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0  # Jika file tidak ditemukan atau isinya tidak valid, set high score ke 0

# Menyimpan high score ke file
def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

def save_high_score_time(score):
    with open(HIGH_SCORE_FILE_TIME, "w") as file:
        file.write(str(score))
        

# Membuat layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Twin Force")

# Memuat gambar ikon
icon_image = pygame.image.load("icon.png")  # Ganti dengan path ke gambar ikon Anda

# Menetapkan ikon pada jendela
pygame.display.set_icon(icon_image)


# Memuat gambar GIF latar belakang
def load_gif(filename):
    pil_image = Image.open(filename)
    frames = []
    try:
        while True:
            frame = pil_image.convert("RGBA")
            frame = frame.transpose(Image.FLIP_TOP_BOTTOM)  # Membalik gambar jika perlu
            frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
            frames.append(frame)
            pil_image.seek(len(frames))  # Pindah ke frame berikutnya
    except EOFError:
        pass  # Selesai membaca semua frame
    return frames

background_frames = load_gif("background.gif")  # Ganti dengan path gambar GIF latar belakang Anda
background_index = 0

# Memuat gambar pesawat dan mengubah ukurannya
original_spaceship_image = pygame.image.load("spaceship.png")  # Ganti dengan path gambar pesawat Anda
spaceship_image = pygame.transform.scale(original_spaceship_image, (50, 50))  # Mengubah ukuran menjadi 50x50 piksel
spaceship_rect1 = spaceship_image.get_rect(center=(WIDTH // 2 - 25, HEIGHT // 2))  # Pesawat pertama di tengah kiri
spaceship_image_mirror = pygame.transform.flip(spaceship_image, False, False)  # Flip vertikal pesawat kedua
spaceship_rect2 = spaceship_image_mirror.get_rect(center=(WIDTH // 2 + 25, HEIGHT //2))  # Pesawat kedua di tengah kanan

# Memuat gambar peluru
bullet_image = pygame.image.load("peluru.png")  # Ganti dengan path gambar peluru Anda
bullet_image = pygame.transform.scale(bullet_image, (40, 45))  # Mengubah ukuran peluru jika perlu

# Memuat gambar musuh
enemy_image = pygame.image.load("enemy.png")  # Ganti dengan path gambar musuh Anda
enemy_image = pygame.transform.scale(enemy_image, (50, 50))  # Mengubah ukuran musuh jika perlu

# Memuat gambar ledakan
explosion_frames = load_gif("explosion.gif")  # Ganti dengan path gambar GIF ledakan Anda

# Memuat suara
spaceship_damage_sound = pygame.mixer.Sound("spaceship_damage.wav")  # Ganti dengan path ke file suara kerusakan pesawat Anda
shoot_sound = pygame.mixer.Sound("shoot.wav")  # Ganti dengan path ke file suara peluru Anda
explosion_sound = pygame.mixer.Sound("explosion.wav")  # Ganti dengan path ke file suara ledakan Anda
enemy_shoot_sound = pygame.mixer.Sound("enemy_shoot.wav")  # Ganti dengan path ke file suara peluru musuh Anda
health_up_sound = pygame.mixer.Sound("health_up.wav")  #


# Mengatur volume efek suara (nilai antara 0.0 hingga 1.0)
shoot_sound.set_volume(0.5)  # Menurunkan volume suara tembakan 
explosion_sound.set_volume(0.5)  # Mengatur volume suara ledakan 
enemy_shoot_sound.set_volume(0.5) #mengatur volume suara tembakan enemy
spaceship_damage_sound.set_volume(0.5) #mengatur volume spaceship tertembak

# Variabel untuk animasi
angle = 0  # Sudut rotasi pesawat
angle2 = 0
move_speed = 5  # Kecepatan gerak pesawat
tilt_angle = -15  # Sudut miring maksimum


# Kelas untuk peluru
class Bullet:
    def __init__(self, x, y, speed=BULLET_SPEED):
        self.image = bullet_image  # Menggunakan gambar peluru
        self.rect = self.image.get_rect(center=(x, y))  # Menggunakan posisi untuk mengatur rect
        self.speed = speed  # Kecepatan peluru

    def update(self):
        self.rect.y -= self.speed  # Menggerakkan peluru ke atas (untuk peluru pemain)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Menggambar peluru menggunakan gambar

# Kelas untuk peluru musuh
class EnemyBullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("enemy_bullet.png")  # Ganti dengan gambar peluru musuh Anda
        self.image = pygame.transform.scale(self.image, (30, 35))  # Mengubah ukuran peluru musuh
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = ENEMY_BULLET_SPEED

    def update(self):
        self.rect.y += self.speed  # Menggerakkan peluru musuh ke bawah

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Menggambar peluru musuh
        
class Bom:
    def __init__(self):
        self.image = pygame.image.load("bom.png")  # Ganti dengan path gambar bom Anda
        self.image = pygame.transform.scale(self.image, (50, 50))  # Mengubah ukuran bom jika perlu
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))  # Mulai dari posisi acak di atas layar
        self.hp = 1  # HP bom (jika perlu)

    def update(self):
        self.rect.y += BOM_SPEED  # Menggerakkan bom ke bawah

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Menggambar bom


# Kelas untuk musuh
class Enemy:
    def __init__(self):
        self.image = enemy_image
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
        self.hp = 1
        self.last_fire_time = time.time()

    def update(self):
        self.rect.y += ENEMY_SPEED
        if time.time() - self.last_fire_time >= ENEMY_FIRE_RATE:
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            enemy_bullets.append(enemy_bullet)  # Menambahkan peluru musuh ke dalam daftar
            enemy_shoot_sound.play()  # Memainkan suara tembakan musuh
            self.last_fire_time = time.time()  # Reset waktu terakhir menembak

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    

class Boss:
    def __init__(self):
        self.image = pygame.image.load("boss.png")  # Ganti dengan gambar boss Anda
        self.image = pygame.transform.scale(self.image, (100, 100))  # Mengubah ukuran boss jika perlu
        self.rect = self.image.get_rect(center=(WIDTH // 2, 50))  # Mulai dari tengah atas layar
        self.hp = 10  # HP boss
        self.last_fire_time = time.time()  # Waktu terakhir menembak
        self.direction = 1  # Arah pergerakan (1 = kanan, -1 = kiri)

    def update(self):
        global BOSS_SPEED
        # Boss bergerak ke kiri dan kanan
        self.rect.x += BOSS_SPEED * self.direction  # Ganti ENEMY_SPEED dengan BOSS_SPEED

        # Jika boss mencapai batas kiri atau kanan, ubah arah
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1  # Ubah arah
            self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))  # Pastikan boss tetap dalam batas layar

        # Menembak peluru ke arah pesawat
        if time.time() - self.last_fire_time >= BOSS_FIRE_RATE:
            boss_bullet1 = BossBullet(self.rect.centerx - 20, self.rect.bottom)  # Peluru dari sisi kiri
            boss_bullet2 = BossBullet(self.rect.centerx + 20, self.rect.bottom)  # Peluru dari sisi kanan
            enemy_bullets.append(boss_bullet1)
            enemy_bullets.append(boss_bullet2)
            enemy_shoot_sound.play()  # Memainkan suara tembakan boss
            self.last_fire_time = time.time()  # Reset waktu terakhir menembak

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Menggambar boss

class BossBullet:
    def __init__(self, x, y):
        global BOSS_BULLET_SPEED
        self.image = pygame.image.load("boss_bullet.png")  # Ganti dengan gambar peluru boss Anda
        self.image = pygame.transform.scale(self.image, (50, 55))  # Mengubah ukuran peluru boss
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BOSS_BULLET_SPEED  # Kecepatan peluru boss

    def update(self):
        # Menggerakkan peluru boss ke bawah
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Menggambar peluru boss

# Kelas untuk ledakan
class Explosion:
    def __init__(self, x, y, animation_speed=0.8, scale= 1.0):
        self.frames = explosion_frames  # Menggunakan gambar ledakan
        self.current_frame = 2  # Frame saat ini
        self.rect = self.frames[self.current_frame].get_rect(center=(x, y))  # Mengatur posisi
        self.animation_speed = animation_speed  # Menggunakan parameter kecepatan
        self.frame_count = 0  # Menghitung frame untuk animasi
        self.scale = scale  # Menyimpan skala untuk ukuran

        # Mengubah ukuran frame ledakan
        self.frames = [pygame.transform.scale(frame, (int(frame.get_width() * scale), int(frame.get_height() * scale))) for frame in self.frames]

    def update(self):
        self.frame_count += self.animation_speed
        if self.frame_count >= len(self.frames):
            return True  # Mengindikasikan bahwa animasi telah selesai
        return False  # Animasi masih berjalan

    def draw(self, surface):
        current_frame = int(self.frame_count)

        # Memastikan current_frame tidak melebihi jumlah frame
        if current_frame < len(self.frames):
            surface.blit(self.frames[current_frame], self.rect.topleft)  # Menggambar frame saat ini

# Daftar peluru, musuh, dan ledakan
bullets = []
enemies = []
boms = []
explosions = []
enemy_bullets = []
last_fire_time = 0  # Waktu terakhir peluru ditembakkan
frame_count = 0  # Menghitung frame untuk spawn musuh
frame_count_bom = 0
spaceship_hp = 5  # Menambahkan HP untuk pesawat
score = 0  # Menambahkan variabel untuk menyimpan skor

# Main Menu Background with G

def main_menu():
    global screen, score,time_limit_enabled
    # Load a custom font with a larger size
    font = pygame.font.Font("font1.ttf", 60)  # Replace with your font file path
    high_score = load_high_score()  # Load thehigh_score_time() high score
    high_score_time = load_high_score_time()

    start_text = font.render("Start Game", True,warna.SILVER)
    quit_text = font.render("Quit", True, warna.MAROON)
    high_score_text = font.render(f"High Score: {high_score}", True, warna.ORANYE)
    high_score_time_text = font.render(f"High Score time: {high_score_time}", True, warna.ORANYE)

    # Create rectangles for the text to place them on screen
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 150))
    high_score_time_rect = high_score_time_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 90))
    
        # Tombol untuk memilih mode dengan time limit aktif
    start_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 50)
    time_limit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
 
    stop_bgm()  # Hentikan musik BGM permainan
    play_main_menu_bgm()  # Mainkan musik main menu

    # Load background frames
    background_frames = load_gif("background_mm.gif")  # Replace with your background gif path
    background_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):  # If "Start" clicked
                    main()  # Start the game
                elif quit_rect.collidepoint(event.pos):  # If "Quit" clicked
                    pygame.quit()
                    sys.exit()
                elif time_limit_button.collidepoint(event.pos):
                    toggle_time_limit()  # Toggle time limit


        # Draw the background GIF
        background = background_frames[background_index]
        background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale to fit screen
        screen.blit(background_scaled, (0, 0))  # Draw the background
        
        # Update the background GIF frame index
        background_index += 1
        if background_index >= len(background_frames):
            background_index = 0  # Loop back to the first frame

        # Draw the text and buttons on top of the background
        draw_text_with_outline(screen, start_text, start_rect, outline_color=(255, 255, 255), outline_thickness=0)
        draw_text_with_outline(screen, quit_text, quit_rect, outline_color=(255,255,255), outline_thickness=0)
        draw_text_with_outline(screen, high_score_text, high_score_rect, outline_color=(255,255,255), outline_thickness=0)
        draw_text_with_outline(screen, high_score_time_text, high_score_time_rect, outline_color=(255,255,255), outline_thickness=0)
        
        # Membuat tombol untuk mode Time Limit toggle
        time_limit_button_width = 550
        time_limit_button_height = 100
        time_limit_button = pygame.Rect(WIDTH - time_limit_button_width - 70, 450, time_limit_button_width, time_limit_button_height)
        
        # Menampilkan tombol Time Limit toggle (aktif / non-aktif)
        pygame.draw.rect(screen, (255, 0, 0) if time_limit_enabled else (0, 0, 255), time_limit_button)

        # Memperbarui teks time limit berdasarkan status (ON/OFF)
        time_limit_text = font.render("Time Limit: " + ("ON" if time_limit_enabled else "OFF"), True, (255, 255, 255))
        screen.blit(time_limit_text, (time_limit_button.x + (time_limit_button.width // 500 - time_limit_text.get_width() // 500), time_limit_button.y + (time_limit_button.height // 2 - time_limit_text.get_height() // 2)))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def draw_text_with_outline(surface, text, rect, outline_color, outline_thickness):
    """Draw text with an outline effect"""
    # Draw the outline first (multiple times with slight offsets)
    for dx in [-outline_thickness, 0, outline_thickness]:
        for dy in [-outline_thickness, 0, outline_thickness]:
            surface.blit(text, rect.move(dx, dy))
    # Draw the main text on top
    surface.blit(text, rect)


# Fungsi Game Over Screen dengan musik
def game_over_screen(score):
    global screen
    font = pygame.font.Font("font1.ttf", 48)  # Gunakan font sesuai preferensi Anda
    game_over_text = font.render("Game Over", True, warna.MERAH)
    score_text = font.render(f"Score: {score}", True, warna.PUTIH)
    high_score = load_high_score()
    high_score_time = load_high_score_time()

    if time_limit_enabled:
        if score > high_score_time:
            save_high_score_time(score)
            high_score_time = score

    elif score > high_score:
        save_high_score(score)
        high_score = score

    high_score_text = font.render(f"High Score: {high_score}", True, warna.ORANYE)
    restart_text = font.render("Restart", True, warna.CYAN)
    quit_text = font.render("Quit", True, warna.MAROON)
    back_to_menu_text = font.render("Back to Main Menu", True, warna.MAROON)

    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
    back_to_menu_rect = back_to_menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 170))

    # Memutar musik game over saat masuk ke game over screen
    stop_bgm()  # Hentikan musik BGM permainan
    play_game_over_bgm()  # Mainkan musik Game Over
    
    background_frames = load_gif("background_over.gif")  # Replace with your background gif path
    background_index = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"  # Signal to restart the game
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif back_to_menu_rect.collidepoint(event.pos):
                    stop_bgm()  # Stop Game Over music
                    return "menu"  # Go back to main menu

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "restart"  # Signal to restart the game    
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # Update the background GIF frame index
        background = background_frames[background_index]
        background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale to fit screen
        screen.blit(background_scaled, (0, 0))  # Draw the background
        
        # Update the background GIF frame index
        background_index += 1
        if background_index >= len(background_frames):
            background_index = 0  # Loop back to the first frame

        draw_text_with_outline(screen, game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)), (0, 0, 0), 0)
        draw_text_with_outline(screen, score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)), (0, 0, 0), 0)
        draw_text_with_outline(screen, high_score_text, high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)), (0, 0, 0), 0)
        draw_text_with_outline(screen, restart_text, restart_rect, (0, 0, 0), 0)
        draw_text_with_outline(screen, quit_text, quit_rect, (0, 0, 0), 0)
        draw_text_with_outline(screen, back_to_menu_text, back_to_menu_rect, (0, 0, 0), 0)

        pygame.display.flip()

def main():
    global background_index, angle, angle2, last_fire_time, frame_count, spaceship_hp, score, frame_count_bom,ENEMY_SPAWN_RATE,BOM_SPAWN_RATE
    clock = pygame.time.Clock()

    # Initialize/reset game state
    bullets.clear()  # Clear any existing bullets
    enemies.clear()  # Clear any existing enemies
    explosions.clear()  # Clear any existing explosions
    enemy_bullets.clear()  # Clear any existing enemy bullets
    boms.clear() # Clear any existing bom
    boss = None
    # Set the position of the spaceships to the center of the screen
    spaceship_rect1.center = (WIDTH // 2 - 25, HEIGHT // 2)  # Set the first spaceship position
    spaceship_rect2.center = (WIDTH // 2 + 25, HEIGHT // 2)  # Set the second spaceship position
    if time_limit_enabled:
        time_limit = 21  # 3 menit dalam detik
        start_time = time.time()  # Waktu mulai permainan
        time_left = time_limit  # Waktu yang tersisa
    else:
        time_left = None  # Tidak ada batas waktu jika time limit tidak aktif

    max_bullets = 10 # Maximum number of bullets
    current_bullets = max_bullets  # Current number of bullets
    last_bullet_refill_time = time.time()  # Time when the last bullet was added    

    # Mulai musik permainan
    play_game_bgm()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Bullet replenishment logic
        if current_bullets < max_bullets and current_time - last_bullet_refill_time >= 2:
            current_bullets += 1  # Refill one bullet
            last_bullet_refill_time = current_time  # Update the last refill time

        # Menangani penekanan tombol
        keys = pygame.key.get_pressed()
        current_time = time.time()

        # Menghitung waktu yang telah berlalu
        if time_limit_enabled:
            elapsed_time = current_time - start_time
            time_left = max(time_limit - elapsed_time, 0)  # Hitung waktu yang tersisa
            if time_left == 0:  # Jika waktu habis, permainan berakhir
                if score > load_high_score_time():
                    save_high_score_time(score)  # Save high score if the player wins
                result = game_over_screen(score)  # Show game over screen
                if result == "restart":
                    score = 0  # Reset score
                    spaceship_hp = 5  # Reset HP
                    stop_bgm()  # Stop the game BGM when game over
                    main()  # Restart the game
                elif result == "menu":
                    main_menu()  # Go back to the main menu
                    return  # Exit main function when game over
                return  # Exit main function after game over

        # Firing logic
        # Firing logic
        if keys[pygame.K_SPACE]:  # If the space key is pressed
            if current_bullets > 0 and current_time - last_fire_time >= FIRE_RATE :
                bullet = Bullet(spaceship_rect1.centerx, spaceship_rect1.top)  # Bullet from the first ship
                bullets.append(bullet)
                bullet = Bullet(spaceship_rect2.centerx, spaceship_rect2.top)  # Bullet from the second ship
                bullets.append(bullet)
                last_fire_time = current_time
                shoot_sound.play()  # Play shoot sound
                current_bullets -= 1  # Decrease the bullet count by the number of bullets fired
            if current_bullets <= 0 :
                spaceship_damage_sound.play()
                spaceship_hp = 0

        # Menggerakkan pesawat
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:  # Serong kiri atas
            spaceship_rect1.x -= move_speed
            spaceship_rect1.y -= move_speed
            spaceship_rect2.x += move_speed
            spaceship_rect2.y -= move_speed
            angle = -tilt_angle  # Miring ke kiri untuk pesawat pertama
            angle2 = tilt_angle  # Miring ke kanan untuk pesawat kedua
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:  # Serong kanan atas
            spaceship_rect1.x += move_speed
            spaceship_rect1.y -= move_speed
            spaceship_rect2.x -= move_speed
            spaceship_rect2.y -= move_speed
            angle = tilt_angle  # Miring ke kanan untuk pesawat pertama
            angle2 = -tilt_angle  # Miring ke kiri untuk pesawat kedua
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:  # Serong kiri bawah
            spaceship_rect1.x -= move_speed
            spaceship_rect1.y += move_speed
            spaceship_rect2.x += move_speed
            spaceship_rect2.y += move_speed
            angle = tilt_angle / 2  # Miring ke belakang untuk pesawat pertama
            angle2 = -tilt_angle / 2  # Miring ke depan untuk pesawat kedua
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:  # Serong kanan bawah
            spaceship_rect1.x += move_speed
            spaceship_rect1.y += move_speed
            spaceship_rect2.x -= move_speed
            spaceship_rect2.y += move_speed
            angle = tilt_angle / 2  # Miring ke belakang untuk pesawat pertama
            angle2 = -tilt_angle / 2  # Miring ke depan untuk pesawat kedua
        elif keys[pygame.K_LEFT]:  # Kiri
            spaceship_rect1.x -= move_speed
            spaceship_rect2.x += move_speed
            angle = -tilt_angle  # Miring ke kiri untuk pesawat pertama
            angle2 = tilt_angle  # Miring ke kanan untuk pesawat kedua
        elif keys[pygame.K_RIGHT]:  # Kanan
            spaceship_rect1.x += move_speed
            spaceship_rect2.x -= move_speed
            angle = tilt_angle  # Miring ke kanan untuk pesawat pertama
            angle2 = -tilt_angle  # Miring ke kiri untuk pesawat kedua
        elif keys[pygame.K_UP]:  # Atas
            spaceship_rect1.y -= move_speed
            spaceship_rect2.y -= move_speed
            angle = -tilt_angle / 2  # Miring ke depan untuk pesawat pertama
            angle2 = tilt_angle / 2  # Miring ke belakang untuk pesawat kedua
        elif keys[pygame.K_DOWN]:  # Bawah
            spaceship_rect1.y += move_speed
            spaceship_rect2.y += move_speed
            angle = tilt_angle / 2  # Miring ke belakang untuk pesawat pertama
            angle2 = -tilt_angle / 2  # Miring ke depan untuk pesawat kedua
        else:
            angle = 0
            angle2 = 0     


        # Mengatur batas layar
        spaceship_rect1.clamp_ip(screen.get_rect())  # Mengatur batas pesawat pertama agar tidak keluar dari layar
        spaceship_rect2.clamp_ip(screen.get_rect())  # Mengatur batas pesawat kedua agar tidak keluar dari layar

        # Menggambar ulang layar
        background = background_frames[background_index]
        background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Mengubah ukuran latar belakang agar sesuai dengan layar

        # Menggambar latar belakang
        screen.blit(background_scaled, (0, 0))  # Menggambar latar belakang

        # Memutar pesawat pertama dan kedua berdasarkan sudut
        rotated_spaceship1 = pygame.transform.rotate(spaceship_image, angle)
        rotated_rect1 = rotated_spaceship1.get_rect(center=spaceship_rect1.center)

        rotated_spaceship2 = pygame.transform.rotate(spaceship_image_mirror, angle2)
        rotated_rect2 = rotated_spaceship2.get_rect(center=spaceship_rect2.center)

        # Menggambar pesawat
        screen.blit(rotated_spaceship1, rotated_rect1.topleft)
        screen.blit(rotated_spaceship2, rotated_rect2.topleft)

        # Memperbarui posisi peluru dan menggambarnya
        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        # Memperbarui posisi musuh dan menggambarnya
        for enemy in enemies[:]:
            enemy.update()
            enemy.draw(screen)
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
            if spaceship_rect1.colliderect(enemy.rect) or spaceship_rect2.colliderect(enemy.rect):
                spaceship_hp -= 1
                spaceship_damage_sound.play()  # Memainkan suara kerusakan
                enemy.hp -= 1
                if enemy.hp <= 0:
                    explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                    explosion_sound.play()
                    enemies.remove(enemy)

            for bullet in bullets[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.hp -= 1
                    bullets.remove(bullet)
                    if enemy.hp <= 0:
                        explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                        explosion_sound.play()
                        score += 10
                        if enemy in enemies:  # Check if enemy is still in the list
                            enemies.remove(enemy)
                        if time_limit_enabled:#  Menambah skor saat musuh dihancurkan
                           time_limit += 3  # Menambahkan 5 detik saat musuh dihancur
                           break
                        
                if boss is not None and bullet.rect.colliderect(boss.rect):  # Jika peluru mengenai boss
                    boss.hp -= 1  # Kurangi HP boss
                    bullets.remove(bullet)  # Hapus peluru
                    if boss.hp <= 0:  # Jika HP boss habis
                        explosions.append(Explosion(boss.rect.centerx, boss.rect.centery))
                        score += 100
                        explosion_sound.play()
                        boss = None  # Reset boss    
                        break

            # Memperbarui dan menggambar peluru musuh
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.update()
            enemy_bullet.draw(screen)
            if enemy_bullet.rect.top > HEIGHT:
                enemy_bullets.remove(enemy_bullet)
            if spaceship_rect1.colliderect(enemy_bullet.rect) or spaceship_rect2.colliderect(enemy_bullet.rect):
                spaceship_hp -= 1
                spaceship_damage_sound.play()  # Memainkan suara kerusakan
                enemy_bullets.remove(enemy_bullet)

            # Memperbarui dan menggambar ledakan
        for explosion in explosions[:]:
            if explosion.update():
                explosions.remove(explosion)
            explosion.draw(screen)

        # Menambahkan musuh baru secara acak
        frame_count += 0.2
        if frame_count >= ENEMY_SPAWN_RATE:
            enemies.append(Enemy())
            ENEMY_SPAWN_RATE = ENEMY_RATE()  # Ganti spawn rate dengan nilai acak baru
            frame_count = 0

        #MENAMBAH BOM ACAK
        frame_count_bom += 0.2
        if frame_count_bom >= BOM_SPAWN_RATE:
            boms.append(Bom())
            BOM_SPAWN_RATE = BOM_RATE()
            frame_count_bom = 0

        # Memperbarui dan menggambar bom
        for bom in boms[:]:
            bom.update()  # Memperbarui posisi bom
            bom.draw(screen)  # Menggambar bom di layar
            if bom.rect.top > HEIGHT:  # Menghapus bom jika sudah keluar dari layar
                boms.remove(bom)
            if spaceship_rect1.colliderect(bom.rect) or spaceship_rect2.colliderect(bom.rect):
                spaceship_hp += 3
                health_up_sound.play()  # Memainkan suara kerusakan
                boms.remove(bom)

        for bom in boms[:]:
            for bullet in bullets[:]:
                if bullet.rect.colliderect(bom.rect):  # Jika peluru mengenai bom
                    bom.hp -= 1  # Mengurangi HP bom
                    bullets.remove(bullet)  # Menghapus peluru
                    if bom.hp <= 0:
                        spaceship_hp -= 1
                        explosions.append(Explosion(bom.rect.centerx, bom.rect.centery))
                        boms.remove(bom)  # Menghapus bom jika HP-nya habis
                    break  # Keluar dari loop setelah menemukan tabrakan  

        # Dalam loop utama
         # Spawn boss jika skor adalah kelipatan 100 dan boss belum ada
        if score % 100 == 0 and boss is None and score > 0:
            boss = Boss()  # Spawn boss jika skor adalah kelipatan 100

        # Update dan gambar boss jika ada
        if boss is not None:
            boss.update()
            if boss.rect.top < 50:  # Jika boss belum mencapai posisi tertentu di layar
                boss.rect.y += BOSS_SPEED  # Gerakkan boss ke bawah
            else:
                boss.rect.y = 50  # Set boss di posisi tetap setelah mencapai 50px dari atas
            boss.draw(screen)   

            # Menggambar bar HP boss
            bar_width = 100  # Lebar bar HP
            bar_height = 10  # Tinggi bar HP
            max_hp = 10 # Maksimal HP boss
            hp_ratio = boss.hp / max_hp  # Rasio HP saat ini terhadap maksimum

            if boss.hp <= 0:  # Jika boss mati
                explosions.append(Explosion(boss.rect.centerx, boss.rect.centery))
                score += 20
                explosion_sound.play()
                boss = None  # Reset boss
            else:  # Hanya menggambar bar HP jika boss masih hidup
                if spaceship_rect1.colliderect(boss.rect) or spaceship_rect2.colliderect(boss.rect):
                    spaceship_hp -= 1
                    spaceship_damage_sound.play()  # Memainkan suara kerusakan
                    boss.hp -= 1  # Kurangi HP boss

                # Gambar latar belakang bar HP
                pygame.draw.rect(screen, (255, 0, 0), (boss.rect.centerx - bar_width // 2, boss.rect.bottom + 5, bar_width, bar_height))  # Latar belakang merah

                # Gambar bar HP yang sebenarnya
                pygame.draw.rect(screen, (0, 255, 0), (boss.rect.centerx - bar_width // 2, boss.rect.bottom + 5, bar_width * hp_ratio, bar_height))  # Bar HP hijau

        # Menampilkan HP pesawat
        font = pygame.font.Font("font.ttf", 48) 
        hp_text = font.render(f"HP: {spaceship_hp}", True, warna.HIJAU)
        screen.blit(hp_text, (WIDTH - 140, 10))

        # Menampilkan skor
        score_text = font.render(f"Score: {score}", True, warna.ORANYE)
        screen.blit(score_text, (10, 10))
        
        bullet_text = font.render(f"Bullets: {current_bullets}/{max_bullets}", True, warna.ORANYE)
        screen.blit(bullet_text, (10, 50))  # Display bullets below the score

        if time_limit_enabled:
            time_text = font.render(f"Time: {int(time_left)}", True, (255, 255, 255))
            screen.blit(time_text, (WIDTH // 2 - 100, 10))
        
        #cek kondisi pesawat
        if spaceship_hp <= 0 or (time_limit_enabled and time_left == 0) or spaceship_hp >= 10:
            result = game_over_screen(score)
            spaceship_hp =+ 5
            if result == "menu":
                score = 0 
                main_menu()  # Go back to main menu
                return
            elif result == "restart":
                score = 0  # Reset score
                spaceship_hp = 5  # Reset HP
                stop_bgm()  # Stop current BGM
                main()  # Restart the game

        # Mengupdate indeks frame latar belakang
        background_index += 1
        if background_index >= len(background_frames):
            background_index = 0  # Kembali ke frame pertama jika sudah sampai akhir

        # Update tampilan game lainnya
        pygame.display.flip()
        clock.tick(FPS)


# Menjalankan fungsi utama
if __name__ == "__main__":
    main_menu()  # Menampilkan menu utama sebelum memulai permainan
