import pygame
import time
import random
import math

pygame.init()

color_1= (255,255,255)  #white
color_2= (255,255,102)  #yellow
color_3= (0,0,0)         #black
color_4= (128,0,128)    #purple
color_5= (0,200,0)       #green
color_6= (255,0,0)       #red
color_7= (0,0,255)

box_len = 900
box_height = 600

# Add at the top of your file (global scope)
snake_direction = "RIGHT"


# Load background image
background_img = pygame.image.load(r"snakegamebg1.png")  # Replace with your actual file name
background_img = pygame.transform.scale(background_img, (box_len, box_height))  # Resize to fit screen


add_caption = pygame.display.set_mode((box_len , box_height))
pygame.display.set_caption("SNAKE GAME")

timer= pygame.time.Clock()

snake_block = 15
snake_speed = 10

display_style = pygame.font.SysFont("arial",30,"bold","italic")
score_font = pygame.font.SysFont("arial",45,"bold","italic")

def final_score(score):
    value = score_font.render("Enjoy the Snake Game       YOUR SCORE IS : " + str(score),True,color_1)
    add_caption.blit(value, [0,0])
    

def make_snake(snake_block, list_snake):
    
    global snake_direction
    time = pygame.time.get_ticks() / 200  # time in seconds scaled

    eye_radius = 2
    offset = 3


    # === Draw BODY with sine-wave slither ===
    for i, segment in enumerate(list_snake[:-1]):
        x, y = segment

        wave_amplitude = 4
        wave_frequency = 0.4
        slither_offset = int(wave_amplitude * math.sin(pygame.time.get_ticks() * 0.005 + i * wave_frequency))

        if snake_direction in ["LEFT", "RIGHT"]:
            y += slither_offset
        else:  # UP or DOWN
            x += slither_offset

        # Gradient fade color (head = brightest)
        fade = 128 + int((127 * (len(list_snake) - i) / len(list_snake)))  # Ranges roughly from 255 (head) to ~128 (tail)
        body_color = (0,0,fade)

        pygame.draw.rect(add_caption, body_color, [x, y, snake_block, snake_block], border_radius=4)

    # === Draw HEAD ===
    x, y = list_snake[-1]

    pygame.draw.rect(add_caption, color_4, [x, y, snake_block, snake_block], border_radius=6)

    # === Draw EYES & TONGUE based on direction ===
    if snake_direction == "UP":
        eye1 = (x + offset, y + offset)
        eye2 = (x + snake_block - offset - 1, y + offset)
        tongue = [(x + snake_block // 2, y), (x + snake_block // 2 - 2, y - 6), (x + snake_block // 2 + 2, y - 6)]
    elif snake_direction == "DOWN":
        eye1 = (x + offset, y + snake_block - offset)
        eye2 = (x + snake_block - offset - 1, y + snake_block - offset)
        tongue = [(x + snake_block // 2, y + snake_block), (x + snake_block // 2 - 2, y + snake_block + 6), (x + snake_block // 2 + 2, y + snake_block + 6)]
    elif snake_direction == "LEFT":
        eye1 = (x + offset, y + offset)
        eye2 = (x + offset, y + snake_block - offset - 1)
        tongue = [(x, y + snake_block // 2), (x - 6, y + snake_block // 2 - 2), (x - 6, y + snake_block // 2 + 2)]
    else:  # RIGHT
        eye1 = (x + snake_block - offset, y + offset)
        eye2 = (x + snake_block - offset, y + snake_block - offset - 1)
        tongue = [(x + snake_block, y + snake_block // 2), (x + snake_block + 6, y + snake_block // 2 - 2), (x + snake_block + 6, y + snake_block // 2 + 2)]

    pygame.draw.circle(add_caption, color_3, eye1, eye_radius)
    pygame.draw.circle(add_caption, color_3, eye2, eye_radius)

    # Flicker tongue every ~200ms
    if pygame.time.get_ticks() // 400 % 2 == 0:
        pygame.draw.polygon(add_caption, (255, 0, 0),tongue)



def display_msg(msg, color):
    mssg=display_style.render(msg, True, color)
    add_caption.blit(mssg, [box_len/6, box_height/3])

def draw_bug_food(surface, x, y, size):
    head_radius = size // 4
    body_width = size
    body_height = size

    # Draw red oval body
    body_rect = pygame.Rect(x, y + head_radius, body_width, body_height - head_radius)
    pygame.draw.ellipse(surface, (255, 0, 0), body_rect)

    # Draw black head (circle)
    head_center = (x + size // 2, y + head_radius)
    pygame.draw.circle(surface, (0, 0, 0), head_center, head_radius)

    # Draw black dots (spots)
    spot_radius = size // 10
    spot_positions = [
        (x + size // 4, y + size // 2),
        (x + 3 * size // 4, y + size // 2),
        (x + size // 2, y + 3 * size // 4),
    ]
    for pos in spot_positions:
        pygame.draw.circle(surface, (0, 0, 0), pos, spot_radius)

def game_start():
    game_over= False
    game_close= False

    value_x1= box_len/2
    value_y1= box_height/2

    x1_change = 0
    y1_change = 0
    
    snake_direction="RIGHT"
    
    list_snake = []
    snake_len = 1

    foodx_pos = round(random.randrange(0, box_len-snake_block)/15.0)*15.0
    foody_pos = round(random.randrange(60, box_height-snake_block)/15.0)*15.0


    while not game_over:
        while game_close == True:
            add_caption.fill(color_6)
            display_msg("You lost! Want to play again Press C else Press Q", color_4)
            final_score(snake_len-1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                    snake_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                    snake_direction = "RIGHT"
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                    snake_direction = "UP"
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                    snake_direction = "DOWN"


        if value_x1>=box_len or value_x1<0 or value_y1>=box_height or value_y1<0:
            game_close = True
            
        value_x1 = value_x1+x1_change
        value_y1 = value_y1+y1_change
        add_caption.blit(background_img, (0, 0))  # Draw background image

        draw_bug_food(add_caption, foodx_pos, foody_pos, snake_block)

        snake_head = []
        snake_head.append(value_x1)
        snake_head.append(value_y1)
        list_snake.append(snake_head)
        if len(list_snake)> snake_len:
            del list_snake[0]

        for x in list_snake[:-1]:
            if x == snake_head:
                game_close = True

        
        make_snake(snake_block, list_snake )
        final_score(snake_len-1)


        pygame.display.update()

        if value_x1 == foodx_pos and value_y1 == foody_pos:
            foodx_pos = round(random.randrange(0, box_len-snake_block)/15.0)*15.0
            foody_pos = round(random.randrange(60, box_height-snake_block)/15.0)*15.0
            snake_len = snake_len+1

        timer.tick(snake_speed)
    
    pygame.quit()
    quit()

game_start()
