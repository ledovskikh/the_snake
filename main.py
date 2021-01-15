import pygame

LIGHT_BLUE = (227, 243, 255)
COLOUR_OF_FRAME_MIN = (139, 0, 255)  # фиолетовый
COLOUR_OF_SNAKE = (11, 218, 81)
FRAME_COLOUR = (255, 204, 0)  # основной фон
SIZE_OF_BLOCK = 30
MARG = 1  # отступ
COUNT_OF_BLOCKS_X = 19
COUNT_OF_BLOCKS_Y = 15

size = [650, 650]  # размер игрового поля

pygame.display.set_caption('The Snake')  # делаем заголовок
screen = pygame.display.set_mode(size)


# создадим класс, для удобства хранения и обращения к координатам змейки


class The_Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y


snake_block = [The_Snake(1, 2), The_Snake(3, 4)]


# функция для рисования поля:

def draw_blocks(colour, row, column):
    for row in range(COUNT_OF_BLOCKS_Y):

        for column in range(COUNT_OF_BLOCKS_X):
            pygame.draw.rect(screen, colour,
                             [30 + column * SIZE_OF_BLOCK + MARG * (column + 1),
                              30 + row * SIZE_OF_BLOCK + MARG * (row + 1),
                              SIZE_OF_BLOCK,
                              SIZE_OF_BLOCK])


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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('EXIT')
            pygame.quit()

    screen.fill(FRAME_COLOUR)
    # нарисовали холст

    pygame.draw.rect(screen, COLOUR_OF_FRAME_MIN, (20, 20, 610, 490,))
    # нарисовали рамку для поля

    draw_blocks(LIGHT_BLUE, SIZE_OF_BLOCK, SIZE_OF_BLOCK)
    # нарисовали поле

    pygame.display.flip()
