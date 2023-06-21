import os
import sys

#os.chdir(sys._MEIPASS)

file = open('datas/saved_sudoku.txt', 'r')

all_sudoku = []

for sudoku_str in file.readlines():
    all_sudoku += [[int(i) for i in sudoku_str[:-1]]]

file.close()

current_sudoku = -1

_num_of_saved_sudoku = len(all_sudoku)

def save(table):
    """Save the table in 'saved_sudoku.txt'"""
    
    global all_sudoku, _num_of_saved_sudoku
    all_sudoku += [table]
    file = open('datas/saved_sudoku.txt', 'a')
    sudoku_str = ''
    for num in table:
        sudoku_str += str(num)
    file.write(sudoku_str + '\n')
    file.close()
    _num_of_saved_sudoku += 1

def sudoku_from_saved():
    """Return sudoku from 'saved_sudoku.txt' under the number 'current_sudoku'"""
    
    global _num_of_saved_sudoku, current_sudoku
    current_sudoku %= _num_of_saved_sudoku
    return all_sudoku[current_sudoku]
