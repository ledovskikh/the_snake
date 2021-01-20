import pygame
import random

pygame.init()
speed_game = 4
score = 0
scores = []

menu_img = pygame.image.load('menu.jpeg')
pygame.mixer.music.load('music.mp3')

pygame.mixer.music.play()

RED = (255, 0, 0)
LIGHT_BLUE = (227, 243, 255)
COL_BACKGROUND = (63, 174, 196)
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
records = False

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


def game_r():
    global game_play, game_over, eaten, score, up, down, left, right, x1, y1, d_col, d_row, \
        snake_body, game_run, scores, snake_blocks, records
    while game_run:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                print('EXIT')
                pygame.quit()

        text_block = pygame.font.Font(None, 55)
        text_play = pygame.font.Font(None, 60)

        text1 = text_block.render('Сыграем?', True, (6, 43, 46))
        text2 = text_play.render('Play!', True, (120, 162, 183))
        text_rec = text_play.render('RECORDS', True, COLOUR_OF_FRAME_MIN)

        screen.fill(COL_BACKGROUND)  # заливаем фон
        screen.blit(menu_img, (300, 380))  # вставляем картинку змейки
        #  нарисуем кнопку "play", выведем текст на экран:

        pygame.draw.circle(screen, (6, 43, 46), (300, 250), 100)
        pygame.draw.rect(screen, (255, 204, 0), (50, 400, 230, 100))
        screen.blit(text1, (30, 30))
        screen.blit(text2, (250, 240))
        screen.blit(text_rec, (60, 430))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 230 < event.pos[0] < 350 and 230 < event.pos[1] < 340:
                    game_play = True
                    game_run = False
                    game_p()

                if 20 < event.pos[0] < 350 and 400 < event.pos[1] < 540:
                    print('!!!!')
                    game_run = False
                    records = True

        while records:
            screen.fill(COL_BACKGROUND)
            pygame.draw.rect(screen, (255, 204, 0), (50, 400, 130, 100))
            text_back = text_block.render('BACK', True, COLOUR_OF_FRAME_MIN)
            text_show_rec = text_block.render('TOP RECORDS', True, (230, 230, 250))
            y = 130
            scores = sorted(scores, reverse=True)
            for i in range(len(scores)):
                user = 'User'
                text_records = (pygame.font.Font(None, 40)).render(f"{user} {str(i + 1)}:"
                                                                   f" {scores[i]}",
                                                                   True, (29, 51,
                                                                          74))
                screen.blit(text_records, (230, y))
                y += 60
                print()

            screen.blit(text_back, (60, 430))
            screen.blit(text_show_rec, (180, 60))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 20 < event.pos[0] < 350 and 400 < event.pos[1] < 540:
                        print('!!!!')
                        game_run = True
                        records = False
            pygame.display.flip()

        pygame.display.flip()


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


snake_blocks = [SnakeBlock(x1, y1)]


def game_p():
    global game_play, game_over, eaten, score, up, down, left, right, x1, y1, d_col, d_row, \
        snake_body, game_run, scores, snake_blocks, records
    if game_play:
        food_x = random.randint(1, 15)
        food_y = random.randint(1, 19)
        draw_blocks_snake(RED, food_x, food_y)

        while not game_over:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    print('EXIT')
                    game_play = False
                    game_run = False
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] > 550 and \
                            event.pos[1] > 590:
                        print('EXIT')
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

            x1 += d_row
            y1 += d_col
            snake_body = [[x1, y1]]

            screen.fill(FRAME_COLOUR)
            # нарисовали холст

            pygame.draw.rect(screen, COLOUR_OF_FRAME_MIN, (20, 20, 610, 490))
            # нарисовали рамку для поля

            draw_blocks(LIGHT_BLUE, SIZE_OF_BLOCK, SIZE_OF_BLOCK)
            # нарисовали поле

            # food_draw(RED, food_x, food_y)
            draw_blocks_snake(RED, food_x, food_y)

            head = snake_blocks[-1]
            new_head = SnakeBlock(head.x1 + d_row, head.y1 + d_col)
            snake_blocks.append(new_head)
            snake_blocks.pop(0)

            if tuple(snake_body[0]) == (food_x, food_y):
                print('!яблоко!')
                score += 1
                eaten = True

            if eaten:
                # если змейка съела еду, то создаем новую еду:
                snake_blocks.append(SnakeBlock(food_x, food_y))
                food_x = random.randint(1, 15)
                food_y = random.randint(1, 19)
                draw_blocks_snake(RED, food_x, food_y)
                eaten = False

            for block in snake_blocks:
                draw_blocks_snake(COLOUR_OF_SNAKE, block.x1, block.y1)

            text_score = pygame.font.Font(None, 45)
            text_sc = text_score.render(f"Your score: {score}", True, (0, 0, 139))
            screen.blit(text_sc, (100, 550))

            pygame.draw.rect(screen, (13, 84, 79), (530, 530, 630, 550))

            text_quit = pygame.font.Font(None, 50)
            text_q = text_quit.render('QUIT', True, (40, 192, 222))
            screen.blit(text_q, (550, 590))

            if y1 > 19 or y1 < 0 or x1 > 15 or x1 < 0:

                pygame.draw.rect(screen, RED, (170, 150, 300, 300))
                go_out = pygame.font.Font(None, 50)
                text_go = go_out.render("Сыграем еще?", True, (0, 64, 107))
                screen.blit(text_go, (190, 170))
                pygame.draw.rect(screen, (0, 128, 0), (180, 250, 100, 100))
                pygame.draw.rect(screen, (0, 128, 0), (360, 250, 100, 100))
                tx_yes = pygame.font.Font(None, 40)
                text_yes = tx_yes.render("ДA", True, (0, 0, 0))
                text_no = tx_yes.render("НЕТ", True, (0, 0, 0))
                screen.blit(text_yes, (200, 270))
                screen.blit(text_no, (380, 270))

                for event in pygame.event.get():

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 250 > event.pos[0] > 150 < event.pos[1] < 380:
                            scores.append(score)
                            print(scores)
                            score = 0
                            up = False
                            down = False
                            right = False
                            left = False
                            d_row = 0
                            d_col = 0
                            x1 = random.randint(1, 10)
                            y1 = random.randint(1, 10)
                            snake_blocks = [SnakeBlock(x1, y1)]
                            snake_body = [[x1, y1]]
                            game_run = True
                            game_r()
                            game_play = False  # пока True: открыто окно с самой игрой
                            game_over = False
                            print('!!')
                        elif 340 < event.pos[0] < 450 and 230 < event.pos[1] < 350:
                            scores.append(score)
                            print(scores)
                            score = 0
                            game_over = True
                            pygame.quit()

            pygame.display.flip()
            timer.tick(speed_game)


game_r()
