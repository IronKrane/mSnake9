import pygame
import random
pygame.init()


WIDTH, HEIGHT, GRID_SIZE = 600, 600, 20
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MegaWąż9')
SCORE_FONT = pygame.font.SysFont('Consolas', 30)
CLOCK = pygame.time.Clock()
FPS, VELOCITY = 60, 1
SNAKE_START_LENGTH = 5
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (150, 150, 255)
WHITE, LIGHT_GRAY, DARK_GREY, BLACK = (255, 255, 255), (250, 250, 250), (200, 200, 200), (0, 0, 0)

class mSnake9:
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.direction = ''
        self.on_the_move = False
        self.step = GRID_SIZE
        self.segments = []
        self.growth = 5
        
        for i in range(SNAKE_START_LENGTH):
            self.segments.append((self.x, self.y))
            
    def add_segment(self):          
        (x, y) = self.segments[-1]
        for i in range(self.growth):
            new_segment = (x, y)
            self.segments.append(new_segment)

    def draw(self, WINDOW):      
        for index, segment in enumerate(self.segments):
            if index < 1:
                head_rect = (segment[0], segment[1], GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(WINDOW, RED, head_rect)
                pygame.draw.rect(WINDOW, BLACK, head_rect, 1) # single pixel border for better visibility
            else:
                body_rect = (segment[0], segment[1], GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(WINDOW, BLUE, body_rect)        
                pygame.draw.rect(WINDOW, BLACK, body_rect, 1) # single pixel border for better visibility

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

        self.segments.insert(0, (self.x, self.y))
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
        food_rect = (self.food_position_x, self.food_position_y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(WINDOW, color, food_rect)
        pygame.draw.rect(WINDOW, BLACK, food_rect, 1) # single pixel border for better visibility

def collision_check(score, snake, food):
    snake_head_rect = pygame.Rect(snake.segments[0][0], snake.segments[0][1], GRID_SIZE, GRID_SIZE)
    food_rect = pygame.Rect(food.food_position_x, food.food_position_y, GRID_SIZE, GRID_SIZE)
    
    if snake_head_rect.colliderect(food_rect):                          # collision check between snake head and food
        score += 1
        food.food_position_x = random.randrange(GRID_SIZE, WIDTH - GRID_SIZE, GRID_SIZE)
        food.food_position_y = random.randrange(GRID_SIZE, HEIGHT - GRID_SIZE, GRID_SIZE)
        snake.add_segment()
        
    if (snake.x < 0 or snake.x > WIDTH or snake.y < 0 or snake.y > HEIGHT) and snake.on_the_move == True:
        score = 0                                                       # collision check with a boundary of the window
        snake.reset()
        
    for segment in snake.segments[1:]:                                  # loop thru every segment in the list except first one
        if segment == snake.segments[0] and snake.on_the_move == True:  # and check if it is a duplicate with a first one
            score = 0                                                   # if true then we have a collision with a tail
            snake.reset()                                               # snake must be moving otherwise we get collision at the starting position
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
    last = pygame.time.get_ticks()
    
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
        
        
        # snake.move()
        # pygame.time.delay(100)
        cooldown = 100                  #todo needs refining, right now game is either unresponsive or too fast
        now = pygame.time.get_ticks()   #* I think check for key input should be here for responsiveness and passed down into move function
        if now - last >= cooldown:
            last = now
            snake.move()
        
        score = collision_check(score, snake, food_normal)
        
        food_normal.draw(WINDOW, GREEN)
        snake.draw(WINDOW)
        pygame.display.update()
        
    pygame.quit()
    exit()

main()