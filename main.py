import pygame
import time
import Tetromino as t

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
GRID_SIZE = 35
GRID_WIDTH = (SCREEN_WIDTH -200)// GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10
# variables
lines=0
score = 0
paused = False
startGame=False
# Colors
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
]

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")



def draw_next_tetromino(surface,next_tetromino):
    next_rect = pygame.Rect(GRID_WIDTH * GRID_SIZE + 10, 50, 180, 180)
    pygame.draw.rect(surface, WHITE, next_rect, 2)  

    font = pygame.font.Font(None, 36)
    next_text = font.render("Next", True, WHITE)
    surface.blit(next_text, (GRID_WIDTH * GRID_SIZE + 60, 10))

    shape = next_tetromino.shape
    shape_width = len(shape[0]) * GRID_SIZE
    shape_height = len(shape) * GRID_SIZE
    start_x = next_rect.x + (next_rect.width - shape_width) // 2
    start_y = next_rect.y + (next_rect.height - shape_height) // 2

    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(start_x + x * GRID_SIZE, start_y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, next_tetromino.color, rect) 
                pygame.draw.rect(surface, WHITE, rect, 2)

def score_area(surface,score,next_tetromino):
    pygame.draw.rect(surface, BLACK, (GRID_WIDTH * GRID_SIZE, 0, SCREEN_WIDTH - GRID_WIDTH * GRID_SIZE, SCREEN_HEIGHT))
    draw_next_tetromino(surface, next_tetromino)

    font = pygame.font.Font(None, 36)

    score_text = font.render("Score", True, WHITE)
    surface.blit(score_text, (GRID_WIDTH * GRID_SIZE + 60, 250))

    score_value_text = font.render(str(score), True, WHITE)
    surface.blit(score_value_text, (GRID_WIDTH * GRID_SIZE + 90, 290))

    pygame.draw.line(surface, WHITE, (GRID_WIDTH * GRID_SIZE + 10, 330), (SCREEN_WIDTH - 10, 330), 2)

    lines_text = font.render("Lines", True, WHITE)
    surface.blit(lines_text, (GRID_WIDTH * GRID_SIZE + 60, 350))
    lines_value_text = font.render(str(lines), True, WHITE)
    surface.blit(lines_value_text, (GRID_WIDTH * GRID_SIZE + 90, 390))
    pause_button = pygame.Rect(GRID_WIDTH * GRID_SIZE + 50, 430, 100, 50)
    pygame.draw.rect(surface, GREY, pause_button)
    pause_text = font.render("Pause", True, WHITE)
    surface.blit(pause_text, (pause_button.x + 10, pause_button.y + 10))

    # Restart Button
    restart_button = pygame.Rect(GRID_WIDTH * GRID_SIZE + 50, 490, 100, 50)
    pygame.draw.rect(surface, GREY, restart_button)
    restart_text = font.render("Restart", True, WHITE)
    surface.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))
    return pause_button,restart_button

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(surface, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(surface, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
    pygame.draw.rect(surface, WHITE, (0, 0, GRID_WIDTH * GRID_SIZE, SCREEN_HEIGHT), 5)

def balance(grid):
    #todo
    return
def remove_filled(grid):
    global score,lines
    fill_row_nos = [i for i in range(0,GRID_HEIGHT) if all(grid[i][j]!=0 for j in range(0,GRID_WIDTH))]
    tmp=0
    for i in fill_row_nos:
        del grid[i]
        balance(grid)
        grid.insert(0,[0 for j in range(GRID_WIDTH)])
        tmp+=10
    lines+=len(fill_row_nos)
    score+=len(fill_row_nos)*tmp
def end(tmp,grid):
    for i in range(len(tmp.shape)):
        for j in range(len(tmp.shape[0])):
            if(grid[tmp.y+i][tmp.x+j]!=0):
                return True
    return False
def draw_start_button(surface):
    font = pygame.font.Font(None, 74)
    text = font.render("Play Game", True, WHITE) 
    button_width = 300
    button_height = 100

    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = (SCREEN_HEIGHT - button_height) // 2
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    pygame.draw.rect(surface, WHITE, button_rect, 5)  

    text_rect = text.get_rect(center=button_rect.center)
    surface.blit(text, text_rect)

    return button_rect 

def draw_pause_overlay(surface):
    frame_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    frame_surface.blit(surface, (0, 0))
    for dx in range(-5, 6, 2): 
        for dy in range(-5, 6, 2): 
            if dx != 0 or dy != 0:  
                frame_surface.blit(surface, (dx, dy))
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  
    frame_surface.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 72)
    text_surface = font.render("Game Paused", True, WHITE)

    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    frame_surface.blit(text_surface, text_rect)

    resume_font = pygame.font.Font(None, 50)
    resume_text = resume_font.render("Resume", True, WHITE)

    resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    pygame.draw.rect(frame_surface, GREY, resume_rect.inflate(20, 10)) 
    surface.blit(frame_surface, (0, 0)) 
    surface.blit(resume_text, resume_rect)

    return resume_rect

def main():
    global score,lines,startGame,paused

    clock = pygame.time.Clock()
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    drop_time = 0  
    drop_interval = 1000
    current_tetromino = t.Tetromino()
    next_tetromino = t.Tetromino()

    resume_button = None
    playGame_button =None 
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and not startGame:
                if playGame_button.collidepoint(event.pos):
                    startGame = True
            elif event.type == pygame.MOUSEBUTTONDOWN and startGame:
                if pause_button.collidepoint(event.pos):
                    if paused:
                        drop_time=current_time
                    paused = not paused
                if restart_button.collidepoint(event.pos):
                    score = 0
                    lines = 0
                    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                    current_tetromino = t.Tetromino()
                    next_tetromino = t.Tetromino()
                    paused = False
                if paused :
                    if resume_button and resume_button.collidepoint(event.pos):
                        paused = False 
        if event.type == pygame.KEYDOWN and not paused:
            if event.key == pygame.K_LEFT:
                    current_tetromino.move_left(grid=grid)
            elif event.key == pygame.K_RIGHT:
                    current_tetromino.move_right(grid=grid)
            elif event.key == pygame.K_DOWN:
                    current_tetromino.move_down(grid)
            elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                current_tetromino.rotate(grid)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                return
        if startGame and not paused:
            for i in range(0,len(current_tetromino.shape)):
                for j in range(0,len(current_tetromino.shape[0])):
                    if current_tetromino.shape[i][j]==1:
                        grid[current_tetromino.y+i][current_tetromino.x+j]=current_tetromino.color
            
            screen.fill(BLACK)
            draw_grid(screen, grid)
            pause_button, restart_button=score_area(screen,score,next_tetromino)
            current_time = pygame.time.get_ticks()  
            if current_time - drop_time > drop_interval and not paused:
                if(current_tetromino.can_move(grid,0,1,1)):
                    current_tetromino.move_down(grid)
                else:
                    remove_filled(grid)
                    current_tetromino = next_tetromino
                    next_tetromino = t.Tetromino()
                    if end(current_tetromino,grid):
                        pygame.quit()
                        return
                drop_time = current_time
        elif startGame and paused:
            resume_button= draw_pause_overlay(screen)
        else:
            playGame_button = draw_start_button(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    pygame.init()
    main()
