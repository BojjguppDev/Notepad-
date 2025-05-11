import pygame
import sys
from tkinter import Tk, filedialog

pygame.init()

# Display setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Notepad-")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Fonts
font = pygame.font.Font(None, 32)
menu_font = pygame.font.Font(None, 28)

# Text settings
text = ""
lines = []
line_height = font.get_height()
max_lines = (HEIGHT - 40) // line_height

clock = pygame.time.Clock()

# Cursor
cursor_visible = True
cursor_timer = 0
cursor_interval = 500

# Menu
menu_height = 30
menu_open = False
menu_rect = pygame.Rect(0, 0, 60, menu_height)
open_rect = pygame.Rect(0, menu_height, 100, 30)
save_rect = pygame.Rect(0, menu_height + 30, 100, 30)

def render_text(surface, lines, x, y, show_cursor=False):
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BLACK)
        surface.blit(text_surface, (x, y + i * line_height))

    if show_cursor:
        cursor_x = font.size(lines[-1])[0] + x if lines else x
        cursor_y = y + (len(lines) - 1) * line_height
        pygame.draw.line(surface, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + line_height), 2)

def draw_menu(surface):
    pygame.draw.rect(surface, GRAY, (0, 0, WIDTH, menu_height))
    file_text = menu_font.render("File", True, BLACK)
    surface.blit(file_text, (10, 5))

    if menu_open:
        pygame.draw.rect(surface, DARK_GRAY, open_rect)
        open_text = menu_font.render("Open", True, WHITE)
        surface.blit(open_text, (10, menu_height + 5))

        pygame.draw.rect(surface, DARK_GRAY, save_rect)
        save_text = menu_font.render("Save", True, WHITE)
        surface.blit(save_text, (10, menu_height + 35))

def save_to_file(filename="note.txt"):
    try:
        with open(filename, "w") as f:
            for line in lines:
                f.write(line + "\n")
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

def open_file():
    global lines, text
    try:
        Tk().withdraw()  # hide main tkinter window
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "r") as f:
                content = f.read()
            lines = content.splitlines()
            text = ""
            print(f"Opened: {filepath}")
    except Exception as e:
        print(f"Error opening file: {e}")

running = True
while running:
    screen.fill(WHITE)
    now = pygame.time.get_ticks()

    if now - cursor_timer >= cursor_interval:
        cursor_visible = not cursor_visible
        cursor_timer = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_rect.collidepoint(event.pos):
                menu_open = not menu_open
            elif menu_open and open_rect.collidepoint(event.pos):
                open_file()
                menu_open = False
            elif menu_open and save_rect.collidepoint(event.pos):
                lines.append(text)
                save_to_file()
                text = ""
                menu_open = False
            else:
                menu_open = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            elif event.key == pygame.K_RETURN:
                lines.append(text)
                text = ""
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                lines.append(text)
                save_to_file()
                text = ""
            elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                open_file()
            else:
                text += event.unicode

    draw_menu(screen)
    current_display = lines[-(max_lines - 1):] + [text]
    render_text(screen, current_display, 10, menu_height + 10, show_cursor=cursor_visible)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
