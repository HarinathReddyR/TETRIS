import random
from main import GRID_HEIGHT,GRID_WIDTH
COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
]


TETROMINOES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1],[1],[1],[1]],
    [[1,0],[1,1],[1,0]],
    [[1,0],[1,1],[0,1]],
    [[0,1],[1,1],[1,0]],
    [[1,1],[1,0],[1,0]]
    
]
class Tetromino:
    def __init__(self):
        self.shape = random.choice(TETROMINOES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    def get_faces(self,grid,f):
        if(f==1):
            tmp =[[i,len(self.shape[0])-1] for i in range(0,len(self.shape[0]))]
            for j in range(0,len(self.shape[0])):
                y = len(self.shape)-1
                while(y>=0 and self.shape[y][j]==0):
                    y-=1
                tmp[j][1]=y
            return tmp
        elif f==2:
            tmp =[[0,i] for i in range(0,len(self.shape))]
            for i in range(0,len(self.shape)):
                x=0
                while(x<GRID_WIDTH and self.shape[i][x]==0):
                    x+=1
                tmp[i][0]=x
            return tmp
        elif f==3:
            tmp =[[len(self.shape[0])-1,i] for i in range(0,len(self.shape))]
            for i in range(0,len(self.shape)):
                x=len(self.shape[0])-1
                while(x>=0 and self.shape[i][x]==0):
                    x-=1
                tmp[i][0]=x
            return tmp
    def erase(self,grid):
        for i in range(0,len(self.shape)):
            for j in range(0,len(self.shape[0])):
                if(self.shape[i][j]==1):
                    grid[i+self.y][j+self.x]=0

    def fill(self,grid):
        for i in range(0,len(self.shape)):
            for j in range(0,len(self.shape[0])):
                if(self.shape[i][j]==1):
                    grid[i+self.y][j+self.x] =self.color

    def can_move(self,grid,x,y,f):
        faces = self.get_faces(grid,f)
        for i in range(len(faces)):
            new_x = self.x + faces[i][0] + x
            new_y = self.y + faces[i][1] + y
            if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (new_y >= 0 and grid[new_y][new_x] != 0):
                return False  
        return True
    def move_down(self,grid):
        if self.can_move(grid,0,1,1)!=True:
            return
        if self.y+len(self.shape)==GRID_HEIGHT:
            return
        self.erase(grid)
        self.y += 1
        self.fill(grid)
    
    def move_left(self,grid):
        if self.can_move(grid,-1,0,2)==False:
            return
        if(self.x==0):
            return
        self.erase(grid)
        self.x-=1
        self.fill(grid)
    
    def move_right(self,grid):
        if self.can_move(grid,+1,0,3)==False:
            return
        if(self.x+len(self.shape[0])>=GRID_WIDTH):
            return
        self.erase(grid=grid)
        self.x+=1
        self.fill(grid)
    
    def rotate(self,grid):
        m = len(self.shape)
        n = len(self.shape[0])
        if(self.x+m>=GRID_WIDTH or self.y+n>=GRID_HEIGHT ):
            return
        temp = [[0]*m for i in range(n)]
        for i in range(n):
            for j in range(m):
                temp[i][j] = self.shape[m-j-1][i]
        can_fill=True
        self.erase(grid)
        for i in range(n):
            for j in range(m):
                if(grid[i+self.y][j+self.x]!=0):
                    can_fill=False
                    break
        if(can_fill):
            self.shape=temp
        self.fill(grid)
        return