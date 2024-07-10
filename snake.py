import pygame
import time
import random

pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen dimensions
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')

clock = pygame.time.Clock()

snake_block = 20  # Double the original size
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)

# Load images
snake_head_img = pygame.image.load('snake_head.png')
snake_body_img = pygame.image.load('snake_body.png')
apple_img = pygame.image.load('apple.png')
background_img = pygame.image.load('background.png')
snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))
snake_body_img = pygame.transform.scale(snake_body_img, (snake_block, snake_block))
apple_img = pygame.transform.scale(apple_img, (snake_block, snake_block))
background_img = pygame.transform.scale(background_img, (dis_width, dis_height))

def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)

def our_snake(snake_block, snake_list, direction_list):
    for i in range(len(snake_list)):
        x, y = snake_list[i]
        if i == len(snake_list) - 1:  # Head of the snake
            head_img = rotate_image(snake_head_img, direction_list[i])
            dis.blit(head_img, (x, y))
        else:
            body_img = snake_body_img
            if direction_list[i] == 90 or direction_list[i] == 270:
                body_img = rotate_image(snake_body_img, 90)
            dis.blit(body_img, (x, y))

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2))
    dis.blit(mesg, mesg_rect.topleft)

def gameLoop():  
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0
    direction = 0  # initial direction (0 degrees means facing right)

    snake_List = []
    direction_list = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    while not game_over:

        while game_close == True:
            dis.blit(background_img, (0, 0))
            message("You Lost! Press Q to Quit or C to Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 270:  # Prevent immediate 180 turn
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 90  # rotate left
                elif event.key == pygame.K_RIGHT and direction != 90:  # Prevent immediate 180 turn
                    x1_change = snake_block
                    y1_change = 0
                    direction = 270  # rotate right
                elif event.key == pygame.K_UP and direction != 180:  # Prevent immediate 180 turn
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 0  # rotate up
                elif event.key == pygame.K_DOWN and direction != 0:  # Prevent immediate 180 turn
                    y1_change = snake_block
                    x1_change = 0
                    direction = 180  # rotate down

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        
        # Draw the background image
        dis.blit(background_img, (0, 0))
        
        dis.blit(apple_img, (foodx, foody))
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        direction_list.append(direction)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
            del direction_list[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List, direction_list)

        pygame.display.update()

        # Improve collision detection
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
