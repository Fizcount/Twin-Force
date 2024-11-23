import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 700, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Membuat layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Pesawat Luar Angkasa")

# Fungsi untuk menampilkan menu utama
def main_menu():
    font = pygame.font.SysFont("Helvetica", 40)
    title_text = font.render("Game Pesawat Luar Angkasa", True, WHITE)
    start_text = font.render("Press ENTER to Start", True, WHITE)
    quit_text = font.render("Press ESC to Quit", True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Menangani input keyboard
        keys = pygame.key.get_pressed()

        # Jika tombol ENTER ditekan, mulai game
        if keys[pygame.K_RETURN]:
            return True  # Mengindikasikan untuk mulai game

        # Jika tombol ESC ditekan, keluar dari game
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # Menggambar layar menu
        screen.fill(BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()  # Update layar
        pygame.time.Clock().tick(FPS)  # Mengatur kecepatan frame

# Fungsi utama untuk game
def main_game():
    # Game logic di sini (seperti yang telah kamu buat di sebelumnya)
    # Ini adalah bagian yang akan dijalankan setelah pemain memilih untuk mulai game
    print("Game dimulai!")  # Contoh placeholder
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Implementasi game lainnya (seperti pergerakan pesawat, tembakan, musuh, dll.)

        pygame.display.update()

# Menjalankan game
if __name__ == "__main__":
    if main_menu():  # Jika menu dipilih untuk memulai game
        main_game()  # Pindah ke main game
        
