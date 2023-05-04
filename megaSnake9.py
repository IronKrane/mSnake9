import pygame
import random
pygame.init()


WIDTH, HEIGHT = 500, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MegaWąż9')
SCORE_FONT = pygame.font.SysFont('Consolas', 30)
FPS, VEL = 30, 3
SNAKE_SIZE, SNAKE_START_LENGTH = 10, 30
WHITE, BLUE, GREEN, GREY, BLACK, RED = (255, 255, 255), (0, 125, 255), (0, 255, 0), (100, 100, 100), (0, 0, 0), (255, 0, 0)
CLOCK = pygame.time.Clock()


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
        for i in range(SNAKE_SIZE):
            new_segment = (x, y)
            self.segments.append(new_segment)
            # print(new_segment)
        

    def draw(self, WINDOW):      
        for index, segment in enumerate(self.segments):
            if index <= 2:
                pygame.draw.rect(WINDOW, RED, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
            else:
                pygame.draw.rect(WINDOW, BLACK, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))        

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
            self.y -= (self.step * VEL)
        if self.direction == 'down':
            self.y += (self.step * VEL)
        if self.direction == 'right':
            self.x += (self.step * VEL)
        if self.direction == 'left':
            self.x -= (self.step * VEL)

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
        self.food_position_x = random.randrange(SNAKE_SIZE, WIDTH - SNAKE_SIZE, SNAKE_SIZE)
        self.food_position_y = random.randrange(SNAKE_SIZE, HEIGHT - SNAKE_SIZE, SNAKE_SIZE)
        
    def draw(self, WINDOW, color):
        pygame.draw.rect(WINDOW, color, (self.food_position_x, self.food_position_y, SNAKE_SIZE, SNAKE_SIZE))


def collision_check(score, snake, food):
    snake_head_rect = pygame.Rect(snake.segments[0][0], snake.segments[0][1], SNAKE_SIZE, SNAKE_SIZE)
    food_rect = pygame.Rect(food.food_position_x, food.food_position_y, SNAKE_SIZE, SNAKE_SIZE)
    
    if snake_head_rect.colliderect(food_rect):
        score += 1
        food.food_position_x = random.randrange(SNAKE_SIZE, WIDTH - SNAKE_SIZE, SNAKE_SIZE)
        food.food_position_y = random.randrange(SNAKE_SIZE, HEIGHT - SNAKE_SIZE, SNAKE_SIZE)
        snake.add_segment()
        # for i in range(50):
        #     snake.segments.append(snake.segments[-1])
        
    if (snake.x < 0 or snake.x > WIDTH or snake.y < 0 or snake.y > HEIGHT) and snake.on_the_move == True:
        score -= 1
        snake.reset()
        
    # if snake.direction != '' and len(snake.segments) > (SNAKE_START_LENGTH) and len(snake.segments) != len(set(snake.segments)):
    # if snake.direction != '' and len(snake.segments) != len(set(snake.segments)):
    #     score -= 1
    #     snake.reset()
    # else:
    #     pass
    
    for segment in snake.segments[1:]:
        if segment == snake.segments[0] and snake.on_the_move == True:
            score -= 1
            snake.reset()
            break
        
        
    return score

def main():
    run = True
    clock = pygame.time.Clock()
    snake = mSnake9(WIDTH // 2, HEIGHT // 2)
    score = 10    
    food_normal = Food(GREEN)
    
    while run:   # main event loop
        CLOCK.tick(FPS)     # regulates speed of a while loop, MAX speed, not min speed
        WINDOW.fill(GREY) 
        score_text = SCORE_FONT.render(f'{score}', 1, BLACK)
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

if __name__ == '__main__': 
    main()