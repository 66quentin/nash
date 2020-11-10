import numpy as np
import sys 

class nash:
    def __init__(self):
        self.gain_grid = self.create_gain_grid()
        self.row_num=len(self.gain_grid)
        self.col_num=len(self.gain_grid[0])
        self.rows = list(range(self.row_num))
        self.columns = list(range(self.col_num))
        self.show_grid()

    def create_gain_grid(self):
        file = open(sys.argv[1], "r")
        gain_grid = []
        for line in file:
            row_array = []
            for gains in line.split(" "):
                row_array.append([float(gain) for gain in gains.split(",")])
            gain_grid.append(row_array)
        file.close()
        return gain_grid;
        
    def show_grid(self):
        print("Welcome to the beat game.\nPlayer 1's actions: rows\nPlayer 2's actions: columns\n  ",end='')
        print(''.join("     "+str(i)+"    " for i in range(self.col_num)),end='')
        for i in range(self.row_num):
            for k in ["|_________","|         "]:
                print("\n  ",end='')
                print(''.join(k for j in range(self.row_num)),end='')
            
            print("\n",i," ",end='', sep='')
            for j in range(self.col_num):
                value=self.gain_grid[i][j]
                size=len(str(value[0])+str(value[1]))
                space=" "*(8-size)+"\0\0"
                print("|",space[1],value[0],"\\",value[1], space[0],end='', sep='')
        print("\n")

    def remove_dominated(self,player):
        num=[len(self.gain_grid),len(self.gain_grid[0])]
        max_values = []
        for l1 in range(num[(player+1)%2]):
            max_gain = np.array(self.gain_grid).max(player)[l1][player]
            lines_to_keep = set()
            for l2 in range(num[player]):
                val = self.gain_grid[l1][l2][player] if player else self.gain_grid[l2][l1][player]
                if val == max_gain:
                    lines_to_keep.add(l2)
            max_values.append(lines_to_keep)

        lines_to_keep = []
        while max_values:
            maximum_intersection = max_values[0].copy()
            for c in range(1, len(max_values)):
                if len(maximum_intersection & max_values[c]) != 0:
                    maximum_intersection = maximum_intersection & max_values[c]
            max_index = maximum_intersection.pop()
            lines_to_keep.append(max_index)
            max_values = [l for l in max_values if max_index not in l]
        if(player): #Player 2
            new_gain_grid = [[] for _ in range(num[0])]
            for c in sorted(lines_to_keep):
                for r in range(num[0]):
                    new_gain_grid[r].append(self.gain_grid[r][c])
        else:
            new_gain_grid = [self.gain_grid[i] for i in sorted(lines_to_keep)]
        self.gain_grid = new_gain_grid
        if(player): #Player 2
            self.columns = [self.columns[i] for i in sorted(lines_to_keep)]
        else:
            self.rows = [self.rows[i] for i in sorted(lines_to_keep)]
        return num[player] != len(lines_to_keep);

    def pure_strategy_sol(self):
        best_gains = {}
        for c in range(self.col_num):
            max_gain = np.array(self.gain_grid).max(0)[c][0]
            for r in range(self.row_num):
                if self.gain_grid[r][c][0] == max_gain:
                    best_gains[(r, c)] = (self.rows[r], self.columns[c])

        best_gain_labels = []
        for r in range(self.row_num):
            max_gain = np.array(self.gain_grid[r]).max(0)[1]
            for c in range(self.col_num):
                if self.gain_grid[r][c][1] == max_gain:
                    if (r, c) in best_gains:
                        best_gain_labels.append(best_gains[(r, c)])
        return best_gain_labels;

    def mixed_strategy_sol(self):
        while self.remove_dominated(0) | self.remove_dominated(1):
            pass
        p1_move_pct = {}
        p2_move_pct = {}
        side_size = len(self.gain_grid)
        if side_size == 1:return (-1, -1);

        p1_res = [[1] * side_size]
        for c in range(1, side_size):
            p1_res.append([self.gain_grid[r][c][1] - self.gain_grid[r][0][1] for r in range(side_size)])
        p1_sol = [1] + [0 * (side_size - 1)]
        p1_res = np.linalg.solve(np.array(p1_res), np.array(p1_sol))
        for r in range(len(self.rows)):
            p1_move_pct[self.rows[r]] = p1_res[r] * 100

        p2_res = [[1] * side_size]
        for r in range(1, side_size):
            p2_res.append([self.gain_grid[r][c][0] - self.gain_grid[0][c][0] for c in range(side_size)])
        p2_sol = [1] + [0 * (side_size - 1)]
        p2_res = np.linalg.solve(np.array(p2_res), np.array(p2_sol))
        for c in range(len(self.columns)):
            p2_move_pct[self.columns[c]] = p2_res[c] * 100
        return (p1_move_pct, p2_move_pct);

    def pure_strategies(self):
        equilibria = self.pure_strategy_sol()
        for sol in equilibria:
            print("Player 1: ", sol[0], ", Player 2: ", sol[1])
        if len(equilibria) == 0:
            print("There is no pure strategy")

    def mixed_strategies(self):
        equilibria = self.mixed_strategy_sol()
        if(equilibria==(-1,-1)):
        	print("No mixed strategy")
        else:
            for r in self.rows:
                print("Player 1: ", r,",", equilibria[0][r], "%")
            for c in self.columns:
                print("Player 2: ", c,",", equilibria[1][c], "%")
            
game = nash()
print("Pure strategy Nash equilibria:")
game.pure_strategies()
print("Mixed strategy Nash equilibria:")
game.mixed_strategies()
