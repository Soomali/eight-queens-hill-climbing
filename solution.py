import random
#table is an 8x8 array where 1 representing
#a queen    
import threading
from multiprocessing import Process

TABLE_SIZE = 8


class SolutionChecker():
    
    def __init__(self,board):
        self.table = board.board

    def intersects_other(self,x,y):
        if self.__intersects_row(x,y):
            return True
        if self.__intersects_column(x,y):
            return True
        start_x,start_y = self.__calculate_upper_start(x,y)
        lower_start_x,lower_start_y = self.__calculate_lower_start(x,y)

        return self.__intersects_upper_diagonally(start_x,start_y,x,y) or self.__intersects_lower_diagonally(lower_start_x,lower_start_y,x,y)

    def __intersects_row(self,x,y):
        for i in range(TABLE_SIZE):
            if(y != i and self.table[x][i] == 1):
                return True
        return False
    
    def __intersects_column(self,x,y):
        for i in range(TABLE_SIZE):
            if(x != i and self.table[i][y] == 1):
                return True
        return False
        
    def __calculate_upper_start(self,x,y):
        start_x = x
        start_y = y
        while start_x > 0 and start_y < TABLE_SIZE - 1:
            start_x -= 1
            start_y += 1
        return start_x,start_y 


    def __calculate_lower_start(self,x,y):
        start_x = x 
        start_y = y 
        while start_x < TABLE_SIZE - 1 and start_y < TABLE_SIZE - 1:
            start_x += 1
            start_y += 1
        return start_x,start_y 


    def __intersects_lower_diagonally(self,start_x,start_y,x,y):
        while start_x < TABLE_SIZE and start_y >= 0:
            if start_x == x and start_y == y:
                start_x -= 1
                start_y -= 1
                continue
            if self.table[start_x][start_y] == 1:
                return True 
            start_x -= 1
            start_y -= 1
        return False

    def __intersects_upper_diagonally(self,start_x,start_y,x,y):
        while start_x < TABLE_SIZE and start_y >= 0:
            if start_x == x and start_y == y:
                start_x += 1
                start_y -= 1
                continue
            if self.table[start_x][start_y] == 1:
                return True 
            start_x += 1
            start_y -= 1
        return False


    def check_solution(self):
        total_intersections = 0
        for i in range(TABLE_SIZE):
            for j in range(TABLE_SIZE):
                if self.table[i][j] == 1:
                    intersects_other =  self.intersects_other(i,j)
                    if intersects_other:
                        total_intersections += 1 
        
        return total_intersections


class Board():
    def __init__(self,board):
        self.board = board 
        self.solution_checker = SolutionChecker(self)
    def get_queen_poisitons(self):
        lst = []
        for i in range(TABLE_SIZE):
            for j in range(TABLE_SIZE):
                if self.board[i][j] == 1:
                    lst.append((i,j))
        return lst 
    def get_intersecting_queen_positions(self):
        pst = self.get_queen_poisitons()
        lst = []
        for i in pst:
            if self.solution_checker.intersects_other(i[0],i[1]):
                lst.append(i)
        return lst

def generate_random_board():
    q_size = TABLE_SIZE
    
    board = [[0 for _ in range(q_size)] for __ in range(q_size)]

    while q_size > 0:
        x = random.randint(0,TABLE_SIZE - 1)
        y = random.randint(0,TABLE_SIZE - 1)
        if board[x][y] == 0:
            board[x][y] = 1
            q_size -= 1

    return Board(board)    




class HillClimber():

    def __init__(self,step_size = 10000,max_steps_on_same_solution = 5000):
        self.board = generate_random_board()
        self.step_size = step_size
        self.max_steps_on_same_solution = max_steps_on_same_solution
        self.replace_count = 0
    def climb(self):
        solution = SolutionChecker(self.board).check_solution()
        if solution == 0:
            return 0
        print(f'initial size: {solution}')
        for i in range(self.step_size):
            solution = self.__take_step(solution)
        return solution
    
    def climb_until_solution(self,):
        
        solution = SolutionChecker(self.board).check_solution()
        i = 0
        j = 0
        while solution != 0:
            solution,is_changed = self.__take_step(solution,i)
            i+=1
            if is_changed:
                i = 0
            if i == self.max_steps_on_same_solution * (8 - solution):
                self.board = generate_random_board()
                print(f'Changing board,solution was {solution}')
                solution = SolutionChecker(self.board).check_solution()
                i = 0
                j+= 1
            
        return i,j

    def __take_step(self,solution,steps_at_same_solution):
        step = self.__step(steps_at_same_solution)
        step_progress = SolutionChecker(step).check_solution()
        if solution > step_progress or (steps_at_same_solution >= self.max_steps_on_same_solution / 2 and solution == step_progress):
            solution = step_progress
            
            self.board = step
            return solution,True
        return solution,False
    
    def __step(self,solution):
        copy = Board(self.board.board.copy())
        self.__replace_random(copy)
        return copy

    def __replace_random(self, copy:Board):
        x,y = random.choice(copy.get_intersecting_queen_positions())

        x_replacement = random.randint(0,TABLE_SIZE - 1)
        y_replacement = random.randint(0,TABLE_SIZE - 1)

        while copy.board[x_replacement][y_replacement] != 0: 
            x_replacement = random.randint(0,TABLE_SIZE - 1)
            y_replacement = random.randint(0,TABLE_SIZE - 1)
        
        copy.board[x][y],copy.board[x_replacement][y_replacement] = copy.board[x_replacement][y_replacement],copy.board[x][y]



def run_climber():
    max_step_size = random.randint(1000,6000)
    print(f'max_step_size:{max_step_size}')
    climber = HillClimber(step_size=100000,max_steps_on_same_solution=max_step_size)
    result = climber.climb_until_solution()
    print(f'took {result[0]} steps and {result[1]} restarts to find solution. max step size was {max_step_size}')
    print(f'{climber.board}')

if __name__ == '__main__':
    processes = [Process(target=run_climber) for i in range(10)]
    for i in processes:
        i.start()

    for i in processes:
        if i.is_alive():
            i.join()