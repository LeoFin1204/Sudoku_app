import copy
from constants import TABLE_SIZE, TABLE_SIDE, BLOCK_SIDE

class Solver:

    _table_of_variants = [[1,2,3,4,5,6,7,8,9] for i in range(TABLE_SIZE)]

    _solutions_num = 0

    _table = [0] * TABLE_SIZE

    _solved_table = []

    _inserted = [False] * TABLE_SIZE

    def __init__(self, inp_table):
        
        self._table_of_variants = [[1,2,3,4,5,6,7,8,9] for i in range(TABLE_SIZE)]
        self._solutions_num = 0
        self._table = [0] * TABLE_SIZE
        self._solved_table = []
        self._inserted = [False] * TABLE_SIZE
        
        for num_of_cell in range(TABLE_SIZE):
            if inp_table[num_of_cell] != 0:
                self._insert(num_of_cell, inp_table[num_of_cell])

    @staticmethod
    def _block_num(num_of_cell):
        """Return nember of 3*3 block in which cell with 'num_of_cell' is"""

        return (num_of_cell % TABLE_SIDE) // BLOCK_SIDE + (num_of_cell // TABLE_SIDE) // BLOCK_SIDE * BLOCK_SIDE

    @staticmethod
    def _str_of_cell(num_of_cell):
        """Return list of cell's numbers in one sudoku string with 'num_of_cell'"""
        
        return [TABLE_SIDE * (num_of_cell // TABLE_SIDE) + i for i in range(TABLE_SIDE)]

    @staticmethod
    def _col_of_cell(num_of_cell):
        """Return list of cell's numbers in one sudoku colomn with 'num_of_cell'"""
        
        return [num_of_cell % TABLE_SIDE + TABLE_SIDE * i for i in range(TABLE_SIDE)]

    @staticmethod
    def _block_of_cell(num_of_cell):
        """Return list of cell's numbers in one sudoku 3*3 block with 'num_of_cell'"""
        
        ans = []
        bl = Solver._block_num(num_of_cell)
        for i in range(BLOCK_SIDE):
            for j in range(BLOCK_SIDE):
                ans += [bl // BLOCK_SIDE * BLOCK_SIDE * TABLE_SIDE + BLOCK_SIDE * (bl % BLOCK_SIDE) + TABLE_SIDE * i + j]
        return ans

    def _insert(self, num_of_cell, num):
        """Insert in sudoku cell 'num_of_cell' number 'num'"""
        
        self._table[num_of_cell] = num
        variant_changes_zone = set(Solver._str_of_cell(num_of_cell) +
                                   Solver._col_of_cell(num_of_cell) +
                                   Solver._block_of_cell(num_of_cell))

        for cell in variant_changes_zone:
            try:
                if cell == num_of_cell:
                    self._table_of_variants[cell] = [num]
                    self._inserted[cell] = True
                else:
                    self._table_of_variants[cell].remove(num)
                if (len(self._table_of_variants[cell]) == 1) and not (self._inserted[cell]):
                    self._insert(cell, self._table_of_variants[cell][0])
            except ValueError:
                pass

    def _cell_with_min_vars(self):
        """Find number of cell with minimal variants of inserting in this cell"""
        min_vars = 10
        cell_with_min_vars = -1
        for i in range(TABLE_SIZE):
            if ((min_vars > len(self._table_of_variants[i])) and (self._table_of_variants[i]) and not (self._inserted[i])):
                min_vars = len(self._table_of_variants[i])
                cell_with_min_vars = i
        return cell_with_min_vars

    def _check_sols_and_find(self):
        """Check number of solutions of current sudoku.
            If there is only one solution it returns thos solution, else return verdict""" 

        if ([] in self._table_of_variants):
            return 'no more solution'

        if (self._solutions_num > 1):
            return 'so many solutions'

        if not (0 in self._table):
            self._solutions_num += 1
            self._solved_table = self._table
            return 'solution find'

        cell_with_min_vars = self._cell_with_min_vars()

        reserve_var_table = copy.deepcopy(self._table_of_variants)
        reserve_inserted = copy.deepcopy(self._inserted)
        reserve_table = copy.deepcopy(self._table)

        for num in self._table_of_variants[cell_with_min_vars]:
            self._insert(cell_with_min_vars, num)
            if self._check_sols_and_find() == 'so many solutions':
                self._table[cell_with_min_vars] = 0
                return 'so many solutions'
            self._table = reserve_table
            self._table_of_variants = reserve_var_table
            self._inserted = reserve_inserted

        return 'enumeration complete'

    def solve(self):
        """Try to solve current sudoku"""
        
        self._check_sols_and_find()
        if self._solutions_num == 0:
            return 'no solution'
        elif self._solutions_num == 1:
            return self._solved_table
        else:
            return 'so many solutions'

