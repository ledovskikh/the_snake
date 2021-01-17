import pygame
import random

pygame.init()

menu_img = pygame.image.load('menu.jpeg')
RED = (255, 0, 0)
LIGHT_BLUE = (227, 243, 255)
COL_BACKGROUND = (135, 206, 250)
COLOUR_OF_FRAME_MIN = (139, 0, 255)  # фиолетовый
COLOUR_OF_SNAKE = (6, 75, 27)
FRAME_COLOUR = (255, 204, 0)  # основной фон
SIZE_OF_BLOCK = 30
MARG = 1  # отступ
COUNT_OF_BLOCKS_X = 19
COUNT_OF_BLOCKS_Y = 15

size = [650, 650]  # размер игрового поля

pygame.display.set_caption('The Snake')  # делаем заголовок
screen = pygame.display.set_mode(size)

# cords of snake
x1 = random.randint(1, 10)
y1 = random.randint(1, 10)

# changes of cords
d_row = 0
d_col = 0
snake_body = []

timer = pygame.time.Clock()

# flags
game_run = True  # пока True: идёт игра
game_play = False  # пока True: открыто окно с самой игрой
game_over = False  # if True: игра заканчивается
eaten = False  # съета ли еда

# добавим еще 4 флага, чтобы понимать, в какую сторону змейка дижется, чтобы нельзя ыло повернуть
# в противоположную сторону

right = False
left = False
up = False
down = False


# функция для отрисовки змейки:

def draw_blocks_snake(colour, row, column):
    for row_ in range(row):
        if row != row_ + 1:
            continue

        for column_ in range(column):

            if column != column_ + 1:
                continue

            pygame.draw.rect(screen, colour,
                             [30 + column_ * SIZE_OF_BLOCK + MARG * (column_ + 1),
                              30 + row_ * SIZE_OF_BLOCK + MARG * (row_ + 1),
                              SIZE_OF_BLOCK,
                              SIZE_OF_BLOCK])


while game_run:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print('EXIT')
            pygame.quit()

    text_block = pygame.font.Font(None, 55)
    text_play = pygame.font.Font(None, 60)

    text1 = text_block.render('Сыграем?', True, (184, 35, 134))
    text2 = text_play.render('Play!', True, (255, 204, 0))

    screen.fill(COL_BACKGROUND)  # заливаем фон
    screen.blit(menu_img, (300, 380))  # вставляем картинку змейки

    #  нарисуем кнопку "play", выведем текст на экран:

    pygame.draw.circle(screen, (148, 0, 211), (300, 250), 100)
    screen.blit(text1, (30, 30))
    screen.blit(text2, (250, 240))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > 230 and \
                    event.pos[0] < 350 and \
                    event.pos[1] > 230 and \
                    event.pos[1] < 340:
                game_play = True
                game_run = False


# функция для рисования поля:

def draw_blocks(colour, row, column):
    for row in range(COUNT_OF_BLOCKS_Y):

        for column in range(COUNT_OF_BLOCKS_X):
            pygame.draw.rect(screen, colour,
                             [30 + column * SIZE_OF_BLOCK + MARG * (column + 1),
                              30 + row * SIZE_OF_BLOCK + MARG * (row + 1),
                              SIZE_OF_BLOCK,
                              SIZE_OF_BLOCK])


# функция для отрисовки еды
def food_draw(colour, food_x, food_y):
    for row_ in range(food_x):
        if food_x != row_ + 1:
            continue

        for column_ in range(food_y):

            if food_y != column_ + 1:
                continue

            pygame.draw.rect(screen, colour,
                             [30 + column_ * SIZE_OF_BLOCK + MARG * (column_ + 1),
                              30 + row_ * SIZE_OF_BLOCK + MARG * (row_ + 1),
                              SIZE_OF_BLOCK,
                              SIZE_OF_BLOCK])


class SnakeBlock():
    def __init__(self, x1, y1):
        self.x1 = x1
        self.y1 = y1


snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]

if game_play:
    food_x = random.randint(1, 15)
    food_y = random.randint(1, 19)

    while not game_over:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                print('EXIT')
                game_play = False
                game_run = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not down:
                    d_row = -1
                    d_col = 0
                    up = True
                    right = False
                    left = False

                elif event.key == pygame.K_DOWN and not up:
                    d_row = 1
                    d_col = 0
                    down = True
                    right = False
                    left = False

                elif event.key == pygame.K_LEFT and not right:
                    d_row = 0
                    d_col = -1
                    left = True
                    down = False
                    up = False

                elif event.key == pygame.K_RIGHT and not left:
                    d_row = 0
                    d_col = 1
                    right = True
                    up = False
                    down = False

        if y1 > 19 or y1 < 0 or x1 > 15 or x1 < 0:
            game_over = True

        x1 += d_row
        y1 += d_col
        snake_body = [[x1, y1]]

        # пусть игра заканчивается, когда змейка умирает:

        screen.fill(FRAME_COLOUR)
        # нарисовали холст

        pygame.draw.rect(screen, COLOUR_OF_FRAME_MIN, (20, 20, 610, 490))
        # нарисовали рамку для поля

        draw_blocks(LIGHT_BLUE, SIZE_OF_BLOCK, SIZE_OF_BLOCK)
        # нарисовали поле

        food_draw(RED, food_x, food_y)

        head = snake_blocks[-1]

        new_head = SnakeBlock(head.x1 + d_row, head.y1 + d_col)
        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        print(x1, y1)
        print(snake_blocks)
        print('down:', down, 'up:', up, 'left:', left, 'right:', right)

        if snake_blocks[-1] == (food_x, food_y):
            snake_blocks.append([food_x, food_y])
            eaten = True
        # draw_blocks_snake(COLOUR_OF_SNAKE, snake_body[0][0], snake_body[0][1])

        # for i in range(1, len(snake_body)):
        #     for j in range(1, len(snake_body)):
        #         draw_blocks_snake(COLOUR_OF_SNAKE, snake_body[i][j], snake_body[i][j + 1])

        if eaten:
            # если змейка съела еду, то создаем новую еду:

            food_x = random.randint(1, 15)
            food_y = random.randint(1, 19)
            print('!!!')

            eaten = False
        for block in snake_blocks:
            draw_blocks_snake(COLOUR_OF_SNAKE, block.x1, block.y1)

        pygame.display.flip()
        timer.tick(5)
