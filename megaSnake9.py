import pygame
import random
pygame.init()


WIDTH, HEIGHT, GRID_SIZE = 500, 500, 10
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MegaWąż9')
SCORE_FONT = pygame.font.SysFont('Consolas', 30)
CLOCK = pygame.time.Clock()
FPS, VELOCITY = 30, 3
SNAKE_START_LENGTH = 30
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
WHITE, LIGHT_GRAY, DARK_GREY, BLACK = (255, 255, 255), (150, 150, 150), (100, 100, 100), (0, 0, 0)


class mSnake9:
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.direction = ''
        self.on_the_move = False
        self.step = 1
        self.segments = []
        
        
        for i in range(SNAKE_START_LENGTH):
            self.segments.append((self.x, self.y))
            
    def add_segment(self):          
        (x, y) = self.segments[-1]
        for i in range(GRID_SIZE):
            new_segment = (x, y)
            # new_segment = (x+(i*GRID_SIZE)%WIDTH, y+(i*GRID_SIZE)%WIDTH)
            # new_segment = (self.segment[0], self.segment[1])
            self.segments.append(new_segment)
            # print(new_segment)
        

    def draw(self, WINDOW):      
        for index, segment in enumerate(self.segments):
            if index <= 2:
                pygame.draw.rect(WINDOW, RED, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(WINDOW, BLACK, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))        

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.direction != 'down':
            self.direction = 'up' 
        if keys[pygame.K_DOWN] and self.direction != 'up':
            self.direction = 'down'
        if keys[pygame.K_RIGHT] and self.direction != 'left':
            self.direction = 'right'
        if keys[pygame.K_LEFT] and self.direction != 'right':
            self.direction = 'left'
            
        if self.direction != '':
            self.on_the_move = True

        if self.direction == 'up':
            self.y -= (self.step * VELOCITY)
        if self.direction == 'down':
            self.y += (self.step * VELOCITY)
        if self.direction == 'right':
            self.x += (self.step * VELOCITY)
        if self.direction == 'left':
            self.x -= (self.step * VELOCITY)

        self.segments.insert(0, (self.x, self.y))   #todo needs a rework to fit the grid
        self.segments.pop()
        

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.direction = ''
        self.on_the_move = False
        self.segments.clear()
        for i in range(SNAKE_START_LENGTH):
            self.segments.append((self.x, self.y))
        

class Food:
    def __init__(self, color):
        self.food_position_x = random.randrange(GRID_SIZE, WIDTH - GRID_SIZE, GRID_SIZE)
        self.food_position_y = random.randrange(GRID_SIZE, HEIGHT - GRID_SIZE, GRID_SIZE)
        
    def draw(self, WINDOW, color):
        pygame.draw.rect(WINDOW, color, (self.food_position_x, self.food_position_y, GRID_SIZE, GRID_SIZE))


def collision_check(score, snake, food):
    snake_head_rect = pygame.Rect(snake.segments[0][0], snake.segments[0][1], GRID_SIZE, GRID_SIZE)
    food_rect = pygame.Rect(food.food_position_x, food.food_position_y, GRID_SIZE, GRID_SIZE)
    
    if snake_head_rect.colliderect(food_rect):
        score += 1
        food.food_position_x = random.randrange(GRID_SIZE, WIDTH - GRID_SIZE, GRID_SIZE)
        food.food_position_y = random.randrange(GRID_SIZE, HEIGHT - GRID_SIZE, GRID_SIZE)
        snake.add_segment()
        # for i in range(50):
        #     snake.segments.append(snake.segments[-1])
        
    if (snake.x < 0 or snake.x > WIDTH or snake.y < 0 or snake.y > HEIGHT) and snake.on_the_move == True:
        score = 0
        snake.reset()
        
    # if snake.direction != '' and len(snake.segments) > (SNAKE_START_LENGTH) and len(snake.segments) != len(set(snake.segments)):
    # if snake.direction != '' and len(snake.segments) != len(set(snake.segments)):
    #     score -= 1
    #     snake.reset()
    # else:
    #     pass
    
    for segment in snake.segments[1:]:
        if segment == snake.segments[0] and snake.on_the_move == True:
            score = 0
            snake.reset()
            break
        
        
    return score

def draw_grid(window):
    for x_axis in range(0, int(HEIGHT / GRID_SIZE)):
        for y_axis in range(0, int(WIDTH / GRID_SIZE)):
            if ((y_axis + x_axis)) % 2 == 0:
                grid_rect = pygame.Rect(x_axis * GRID_SIZE, y_axis * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(window, LIGHT_GRAY, grid_rect)
            else:
                grid_rect = pygame.Rect(x_axis * GRID_SIZE, y_axis * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(window, DARK_GREY, grid_rect)

def main():
    run = True
    clock = pygame.time.Clock()
    snake = mSnake9(WIDTH // 2, HEIGHT // 2)
    score = 0    
    food_normal = Food(GREEN)
    
    while run:   # main event loop
        CLOCK.tick(FPS)     # regulates speed of a while loop, have influence on speed of the snake
        # WINDOW.fill(LIGHT_GRAY) 
        draw_grid(WINDOW)
        score_text = SCORE_FONT.render(f'Score {score}', 1, BLACK)
        WINDOW.blit(score_text, (WIDTH*0.02, HEIGHT*0.01))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                print(pygame.key.name(event.key))
        
        
        snake.move()
        
        
        
        score = collision_check(score, snake, food_normal)
        
        food_normal.draw(WINDOW, GREEN)
        snake.draw(WINDOW)
        pygame.display.update()
        
    pygame.quit()
    exit()


main()