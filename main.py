import pygame
import random
import time
# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра: Лови объекты!")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Фон и текстуры объектов
background_color = WHITE
object_texture = pygame.image.load("obj.png")
object_texture = pygame.transform.scale(object_texture, (50, 50))

bg_texture = pygame.image.load("bg.png")
bg_texture = pygame.transform.scale(bg_texture, (WIDTH, HEIGHT))

# Параметры объектов
objects = []  # Список объектов
for _ in range(5):  # Добавляем стартовые объекты
    obj = {
        "x": random.randint(50, WIDTH - 50),
        "y": random.randint(50, HEIGHT - 150),
        "dx": random.choice([-4, -3, -2, 2, 3, 4]),
        "dy": random.choice([-4, -3, -2, 2, 3, 4])
    }
    objects.append(obj)

# Счет игрока
score = 0

rage = False
max_im = 8
percentage_spawn = 0.02

# Шрифт
font = pygame.font.SysFont("Arial", 24)

# Основной цикл игры
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for obj in objects[:]:
                obj_rect = pygame.Rect(obj["x"], obj["y"], 50, 50)
                if obj_rect.collidepoint(mouse_x, mouse_y):
                    objects.remove(obj)
                    score += 1
    # Добавление нового объекта
    if len(objects) < max_im and random.random() < percentage_spawn:
        new_obj = {
            "x": random.randint(50, WIDTH - 50),
            "y": random.randint(50, HEIGHT - 150),
            "dx": random.choice([-4, -3, -2, 2, 3, 4]),
            "dy": random.choice([-4, -3, -2, 2, 3, 4])
        }
        objects.append(new_obj)
    # Обновление объектов
    for obj in objects:
        obj["x"] += obj["dx"]
        obj["y"] += obj["dy"]

        # Проверка столкновений со стенами
        if obj["x"] <= 0 or obj["x"] + 50 >= WIDTH:
            obj["dx"] = -obj["dx"]
        if obj["y"] <= 0 or obj["y"] + 50 >= HEIGHT - 50:
            obj["dy"] = -obj["dy"]

    # Рендеринг
    screen.fill(background_color)
    screen.blit(bg_texture, (0,0))

    if rage:
        victory_text = font.render("Степан, ты не прав. И остаешься на продленку!", True, GREEN)
        screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width()//2, HEIGHT - 40))
        font_max = pygame.font.Font("Horroroidboldital.ttf", 256)
        victory_text = font_max.render("And now?!", True, (168, 32, 32))
        screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width()//2, HEIGHT //2 - victory_text.get_height()//2))

    title_text = font.render("Лопни всех Степашек", True, GREEN)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width()//2, 20))
    # Отображение объектов
    for obj in objects:
        screen.blit(object_texture, (obj["x"], obj["y"]))

    # Отображение панели с счетом
    score_text = font.render(f"Счет: {score}", True, BLACK)
    screen.blit(score_text, (10, HEIGHT - 40))

    # Проверка на победу
    if not objects:  # Если все объекты удалены

        rage = True
        max_im = 50
        percentage_spawn = 0.2


        

    pygame.display.flip()

    # Ограничение FPS
    pygame.time.Clock().tick(60)

# Завершение Pygame
pygame.quit()