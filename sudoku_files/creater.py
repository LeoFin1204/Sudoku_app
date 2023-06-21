import copy
import random
import solver
from constants import TABLE_SIZE, TABLE_SIDE, BLOCK_SIDE

MAX_NUM_1LEV = 36
MAX_NUM_2LEV = 42
MAX_NUM_3LEV = 48
MIN_NUM_1LEV = 31
MIN_NUM_2LEV = 37
MIN_NUM_3LEV = 43

class SolvedTable:
    
    _table = [[1,2,3,4,5,6,7,8,9],
              [4,5,6,7,8,9,1,2,3],
              [7,8,9,1,2,3,4,5,6],
              [2,3,4,5,6,7,8,9,1],
              [5,6,7,8,9,1,2,3,4],
              [8,9,1,2,3,4,5,6,7],
              [3,4,5,6,7,8,9,1,2],
              [6,7,8,9,1,2,3,4,5],
              [9,1,2,3,4,5,6,7,8]]

    def swap_str(self, str1, str2):
        """Swap 2 strings"""

        self._table[str1], self._table[str2] = self._table[str2], self._table[str1]

    def swap_col(self, col1, col2):
        """Swap 2 columns"""

        for i in range(9):
            self._table[i][col1], self._table[i][col2] = self._table[i][col2], self._table[i][col1]

    def swap_str_block(self, bl1, bl2):
        """Swap 2 blocks of strings"""

        self.swap_str(BLOCK_SIDE * bl1, BLOCK_SIDE * bl2)
        self.swap_str(BLOCK_SIDE * bl1 + 1, BLOCK_SIDE * bl2 + 1)
        self.swap_str(BLOCK_SIDE * bl1 + 2, BLOCK_SIDE * bl2 + 2)

    def swap_col_block(self, bl1, bl2):
        """Swap 2 blocks of columns"""

        self.swap_col(BLOCK_SIDE * bl1,BLOCK_SIDE * bl2)
        self.swap_col(BLOCK_SIDE * bl1 + 1, BLOCK_SIDE * bl2 + 1)
        self.swap_col(BLOCK_SIDE * bl1 + 2, BLOCK_SIDE * bl2 + 2)

    def transpose(self):
        """Transpose table"""

        for i in range(TABLE_SIDE):
            for j in range(i):
                self._table[i][j], self._table[j][i] = self._table[j][i], self._table[i][j]

    def solved_table(self):
        ans = []
        for i in range(9):
            ans += self._table[i]
        return ans

class Difficulty:
    """Difficulty of creating sudoku"""

    min_num_of_full_cells = 0
    max_num_of_full_cells = 0

    def __init__(self, dif=0):
        if dif == 1:
            self.min_num_of_full_cells = MIN_NUM_1LEV
            self.max_num_of_full_cells = MAX_NUM_1LEV
        elif dif == 2:
            self.min_num_of_full_cells = MIN_NUM_2LEV
            self.max_num_of_full_cells = MAX_NUM_2LEV
        elif dif == 3:
            self.min_num_of_full_cells = MIN_NUM_3LEV
            self.max_num_of_full_cells = MAX_NUM_3LEV
        else:
            self.min_num_of_full_cells = 0
            self.max_num_of_full_cells = 0

    def dif_range(self):
        """Return range of possible number empty cells"""

        return self.min_num_of_full_cells, self.max_num_of_full_cells

class Creator:

    difficulty = Difficulty()

    def __init__(self, dif):
        self.difficulty = Difficulty(dif)

    def _choose_2():
        """Choose 2 string or colomn from one block"""

        num1 = random.choice([x for x in range(TABLE_SIDE)])
        num1_block = [num1//BLOCK_SIDE * BLOCK_SIDE,
                      num1//BLOCK_SIDE * BLOCK_SIDE + 1,
                      num1//BLOCK_SIDE * BLOCK_SIDE + 2]
        num1_block.remove(num1)
        num2 = random.choice(num1_block)

        return num1, num2

    def _choose_2_block():
        """Choose 2 blocks of strings or columns"""

        blocks = [x for x in range(BLOCK_SIDE)]
        block1 = random.choice(blocks)
        blocks.remove(block1)
        block2 = random.choice(blocks)

        return block1, block2
        
    def _shaffle(self):
        """Shaffle full table for deleting cells"""
        
        table = SolvedTable()

        num_of_shaffles = 5000
        
        for i in range(num_of_shaffles):

            shaffle_types = (
                ["2_string"] * 5 +
                ["2_colomn"] * 5 +
                ["string_block"] * 2 +
                ["colomn_block"] * 2
                )
            
            current_shaffle_comand = random.choice(shaffle_types)
            
            if current_shaffle_comand == "2_string":
                str1, str2 = Creator._choose_2()
                table.swap_str(str1, str2)
            elif current_shaffle_comand == "2_colomn":
                col1, col2 = Creator._choose_2()
                table.swap_col(col1, col2)
            elif current_shaffle_comand == "string_block":
                bl1, bl2 = Creator._choose_2_block()
                table.swap_str_block(bl1, bl2)
            elif current_shaffle_comand == "colomn_block":
                bl1, bl2 = Creator._choose_2_block()
                table.swap_col_block(bl1, bl2)
                
        table.transpose()

        return table.solved_table()

    def _delete_cells(self, table):
        """Delete some cells and get finished sudoku table"""

        reserved_table = copy.deepcopy(table)
        not_checked = [cell for cell in range(TABLE_SIZE)]
        deleted_cells_counter = 0

        min_n, max_n = self.difficulty.dif_range()
        max_deleted_cells = random.randint(min_n, max_n)

        while (deleted_cells_counter <= max_deleted_cells) and (not_checked):
            random_cell = random.choice(not_checked)
            table[random_cell] = 0
            not_checked.remove(random_cell)

            solving_table = solver.Solver(table)
            if isinstance(solving_table.solve(), str):
                table[random_cell] = reserved_table[random_cell]

        return table

        

    def create_sudoku(self):
        """Return unsolved sudoku table"""
        
        return self._delete_cells(self._shaffle())
