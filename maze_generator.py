import pygame
from random import randrange


w, h = 400, 400
buffer = 2
pygame.init()
screen = pygame.display.set_mode((w+buffer, h+buffer))

clock = pygame.time.Clock()

BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
PINK  = pygame.Color("magenta")
GREEN = pygame.Color("green")


class Cell():
    def __init__(self, is_start=False, is_end=False):
        self.UP = self.DOWN = self.RIGHT = self.LEFT = True
        self.visited = False
        self.start = is_start
        self.end = is_end


def draw_cells(cells:list, rows, cols, offset, in_progress=True):
    for j in range(cols):
        for i in range(rows):
            x = j*offset
            y = i*offset
            if in_progress and cells[i][j].visited:
                pygame.draw.rect(screen, PINK, pygame.Rect(
                    (x, y), (offset, offset)
                ))
            if cells[i][j].UP:
                pygame.draw.line(screen, WHITE, (x        , y       ) , (x+offset , y       ), buffer)
            if cells[i][j].DOWN:
                pygame.draw.line(screen, WHITE, (x        , y+offset) , (x+offset , y+offset), buffer)
            if cells[i][j].RIGHT:
                pygame.draw.line(screen, WHITE, (x+offset , y       ) , (x+offset , y+offset), buffer)
            if cells[i][j].LEFT:
                pygame.draw.line(screen, WHITE, (x        , y       ) , (x        , y+offset), buffer)


def draw_solution(solution, offset):
    for r,c in solution:
        pygame.draw.rect(screen, GREEN, pygame.Rect(
            (c*offset, r*offset), (offset, offset)
        ))

def main():

    cols = rows = 20
    offset = w//cols

    cells = []
    for j in range(cols):
        row = []
        for i in range(rows):
            row.append(Cell())
        cells.append(row)
    
    cells[0][0].start = True
    cells[-1][-1].end = True

    row_index = 0
    col_index = 0
    current = cells[row_index][col_index]

    stack = [ (current, row_index, col_index) ]
    current.visited = True
    solution = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        if len(stack) > 0:

            current, row_index, col_index = stack.pop()

            neighbors = []
            up    = cells[row_index-1][col_index] if row_index>0 else None
            down  = cells[row_index+1][col_index] if row_index<rows-1 else None
            right = cells[row_index][col_index+1] if col_index<cols-1 else None
            left  = cells[row_index][col_index-1] if col_index>0 else None
            if up is not None and not up.visited:
                neighbors.append(0) # up=0
            if down is not None and not down.visited:
                neighbors.append(1) # down=1 
            if right is not None and not right.visited:
                neighbors.append(2) # right=2
            if left is not None and not left.visited:
                neighbors.append(3) # left=3
            
            if len(neighbors) > 0:

                stack.append( (current, row_index, col_index) )

                next_id = neighbors[randrange(len(neighbors))]
                if next_id == 0:
                    current.UP = False
                    up.DOWN = False
                    current = up
                    row_index = row_index-1
                elif next_id == 1:
                    current.DOWN = False
                    down.UP = False
                    current = down
                    row_index = row_index+1
                elif next_id == 2:
                    current.RIGHT = False
                    right.LEFT = False
                    current = right
                    col_index = col_index+1
                elif next_id == 3:
                    current.LEFT = False
                    left.RIGHT = False
                    current = left
                    col_index = col_index-1

                current.visited = True
                stack.append( (current, row_index, col_index) )
                if current.end:
                    solution = [(r,c) for _,r,c in stack]

        else:
            draw_solution(solution, offset)

        draw_cells(cells, rows, cols, offset, len(stack) > 0)
        pygame.draw.rect(screen, GREEN, pygame.Rect(
            (col_index*offset+buffer, row_index*offset+buffer), (offset-buffer, offset-buffer)
        ))

        pygame.display.flip()
        clock.tick(max(rows,cols))


if __name__ == "__main__":
    main()
