import pygame
import sys
import solver
import creater
import saver
import copy
from constants import TABLE_SIZE, TABLE_SIDE, BLOCK_SIDE

pygame.init()

FONE_COLOR = (255, 240, 217)
BLACK = (0, 0, 0)
SELECTED_CELL_COLOR = (255, 200, 195)
GOOD_MASSAGE_COLOR = (105, 135, 199)
BAD_MASSAGE_COLOR = (230, 161, 192)
NUMBER_COLOR = (134, 121, 175)
MOUSE_ON_COLOR = (204, 150, 200)
FIX_CELL_COLOR = (200, 255, 200)

FONT = pygame.font.Font(None, 70)

FPS = 50

SCREEN = pygame.display.set_mode((830, 760)) 

BUTTON_1_RECT = pygame.Rect((700,40,90,90))
BUTTON_2_RECT = pygame.Rect((700,150,90,90))
BUTTON_3_RECT = pygame.Rect((700,260,90,90))
BUTTON_4_RECT = pygame.Rect((700,370,90,90))
BUTTON_5_RECT = pygame.Rect((700,480,90,90))
BUTTON_EXIT_RECT = pygame.Rect((700,640,90,90))
SUDOKU_FIELD = pygame.Rect((20, 20, 629, 629))

CLOCK = pygame.time.Clock()
SOLVER_PICT = pygame.image.load('images/Solver.bmp')
SOLVE_PICT = pygame.image.load('images/Solve.bmp')
CREATOR_PICT = pygame.image.load('images/Creater.bmp')
CREATE_PICT = pygame.image.load('images/Create.bmp')
SOLVINGMODE_PICT = pygame.image.load('images/Classic.bmp')
SAVE_PICT = pygame.image.load('images/Save.bmp')
ERASE_PICT = pygame.image.load('images/Erase.bmp')
PREVIOUS_PICT = pygame.image.load('images/Previous.bmp')
NEXT_PICT= pygame.image.load('images/Next.bmp')
BACK_PICT = pygame.image.load('images/Back.bmp')
DIFFICULTY_1_PICT = pygame.image.load('images/1.bmp')
DIFFICULTY_2_PICT = pygame.image.load('images/2.bmp')
DIFFICULTY_3_PICT = pygame.image.load('images/3.bmp')
EXIT_PICT = pygame.image.load('images/Exit.bmp')
FRAME = pygame.image.load('images/frame.png')
ICON = pygame.image.load('images/icon.png')

NUM_KEY_SET = [pygame.K_BACKSPACE,
               pygame.K_1, pygame.K_2, pygame.K_3,
               pygame.K_4, pygame.K_5, pygame.K_6,
               pygame.K_7, pygame.K_8, pygame.K_9]

class Button:
    _rect = None
    _bottomright = None
    _picture = None

    def __init__(self, bottomright):
        self._bottomright = bottomright

    def action(self):
        """Actions which happen after click"""
        pass

class SolverButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = SOLVER_PICT.get_rect(bottomright = self._bottomright)
        self._picture = SOLVER_PICT

    def action(self):
        global lobby
        lobby = SolverLobby()

class CreatorButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = CREATOR_PICT.get_rect(bottomright = self._bottomright)
        self._picture = CREATOR_PICT

    def action(self):
        global lobby
        lobby = CreatorLobby()

class SolvingModeButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = SOLVINGMODE_PICT.get_rect(bottomright = self._bottomright)
        self._picture = SOLVINGMODE_PICT

    def action(self):
        global lobby
        lobby = SolvingModeLobby()

class SolveButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = SOLVE_PICT.get_rect(bottomright = self._bottomright)
        self._picture = SOLVE_PICT

    def action(self):
        global sudoku, massage, massage_color, wrong_filled_cells, fix_cells
        
        if wrong_filled_cells:
            massage = 'wrong input'
            massage_color = BAD_MASSAGE_COLOR
            return
        elif sudoku.count(0) >= (TABLE_SIZE - 16):
            massage = 'few numbers'
            massage_color = BAD_MASSAGE_COLOR
            return
        
        solution = solver.Solver(sudoku)
        output = solution.solve()
        
        if isinstance(output, str):
            massage = output
            massage_color = BAD_MASSAGE_COLOR
        else:
            sudoku = output
            fix_cells = []
            massage = 'successfuly solved'
            massage_color = GOOD_MASSAGE_COLOR
            

class CreateButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = CREATE_PICT.get_rect(bottomright = self._bottomright)
        self._picture = CREATE_PICT

    def action(self):
        global lobby
        lobby = SelectingDifficulty()

class SaveButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = SAVE_PICT.get_rect(bottomright = self._bottomright)
        self._picture = SAVE_PICT

    def action(self):
        global sudoku, massage, massage_color
        saver.save(sudoku)
        massage = 'sudoku saved'
        massage_color = GOOD_MASSAGE_COLOR

class EraseButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = ERASE_PICT.get_rect(bottomright = self._bottomright)
        self._picture = ERASE_PICT

    def action(self):
        global sudoku, massage, wrong_filled_cells, fix_cells
        wrong_filled_cells = []
        sudoku = [0] * TABLE_SIZE
        massage = ''
        fix_cells = []

class PreviousButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = PREVIOUS_PICT.get_rect(bottomright = self._bottomright)
        self._picture = PREVIOUS_PICT

    def action(self):
        global sudoku, massage, massage_color
        saver.current_sudoku -= 1
        sudoku = saver.sudoku_from_saved()
        set_cells(sudoku)
        massage = 'level ' + str(saver.current_sudoku + 1)
        massage_color = GOOD_MASSAGE_COLOR

class NextButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = NEXT_PICT.get_rect(bottomright = self._bottomright)
        self._picture = NEXT_PICT

    def action(self):
        global sudoku, massage, massage_color
        saver.current_sudoku += 1
        sudoku = saver.sudoku_from_saved()
        set_cells(sudoku)
        massage = 'level ' + str(saver.current_sudoku + 1)
        massage_color = GOOD_MASSAGE_COLOR

class BackButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = BACK_PICT.get_rect(bottomright = self._bottomright)
        self._picture = BACK_PICT

    def action(self):
        global lobby, massage
        lobby = StartLobby()
        massage = ''

class DifficultyButton(Button):

    def __init__(self, bottomright, dif):
        super().__init__(bottomright)
        if dif == 1:
            self._rect = DIFFICULTY_1_PICT.get_rect(bottomright = self._bottomright)
            self._picture = DIFFICULTY_1_PICT
        elif dif == 2:
            self._rect = DIFFICULTY_2_PICT.get_rect(bottomright = self._bottomright)
            self._picture = DIFFICULTY_2_PICT
        else:
            self._rect = DIFFICULTY_3_PICT.get_rect(bottomright = self._bottomright)
            self._picture = DIFFICULTY_3_PICT
        self._difficulty = dif

    def action(self):
        global sudoku, massage, massage_color, lobby
        creator = creater.Creator(self._difficulty)
        sudoku = creator.create_sudoku()
        set_cells(sudoku)
        massage = 'new sudoku created'
        massage_color = GOOD_MASSAGE_COLOR
        lobby = StartLobby()

class ExitButton(Button):

    def __init__(self, bottomright):
        super().__init__(bottomright)
        self._rect = EXIT_PICT.get_rect(bottomright = self._bottomright)
        self._picture = EXIT_PICT

    def action(self):
        pygame.quit()
        sys.exit()

class Lobby:

    button_1 = Button((790, 130))
    button_2 = Button((790, 240))
    button_3 = Button((790, 350))
    button_4 = Button((790, 460))
    button_5 = Button((790, 570))
    button_exit = ExitButton((790, 720))

    def draw(self):
        """Draw all buttons of the lobby"""

        pass

class StartLobby(Lobby):

    def __init__(self):
        self.button_1 = SolverButton((790, 130))
        self.button_2 = CreatorButton((790, 240))
        self.button_3 = SolvingModeButton((790, 350))
        self.button_4 = SaveButton((790, 460))
        self.button_5 = EraseButton((790, 570))

    def draw(self):
        global SCREEN
        SCREEN.blit(self.button_1._picture, self.button_1._rect)
        SCREEN.blit(self.button_2._picture, self.button_2._rect)
        SCREEN.blit(self.button_3._picture, self.button_3._rect)
        SCREEN.blit(self.button_4._picture, self.button_4._rect)
        SCREEN.blit(self.button_5._picture, self.button_5._rect)
        SCREEN.blit(self.button_exit._picture, self.button_exit._rect)

class SolverLobby(Lobby):

    def __init__(self):
        self.button_1 = SolveButton((790, 130))
        self.button_2 = EraseButton((790, 240))
        self.button_3 = BackButton((790, 350))

    def draw(self):
        global SCREEN
        SCREEN.blit(self.button_1._picture, self.button_1._rect)
        SCREEN.blit(self.button_2._picture, self.button_2._rect)
        SCREEN.blit(self.button_3._picture, self.button_3._rect)
        SCREEN.blit(self.button_exit._picture, self.button_exit._rect)

class CreatorLobby(Lobby):

    def __init__(self):
        self.button_1 = CreateButton((790, 130))
        self.button_2 = SaveButton((790, 240))
        self.button_3 = SolveButton((790, 350))
        self.button_4 = BackButton((790, 460))

    def draw(self):
        global SCREEN
        SCREEN.blit(self.button_1._picture, self.button_1._rect)
        SCREEN.blit(self.button_2._picture, self.button_2._rect)
        SCREEN.blit(self.button_3._picture, self.button_3._rect)
        SCREEN.blit(self.button_4._picture, self.button_4._rect)
        SCREEN.blit(self.button_exit._picture, self.button_exit._rect)

class SolvingModeLobby(Lobby):

    def __init__(self):
        self.button_1 = NextButton((790, 130))
        self.button_2 = PreviousButton((790, 240))
        self.button_3 = EraseButton((790, 350))
        self.button_4 = BackButton((790, 460))

    def draw(self):
        global SCREEN
        SCREEN.blit(self.button_1._picture, self.button_1._rect)
        SCREEN.blit(self.button_2._picture, self.button_2._rect)
        SCREEN.blit(self.button_3._picture, self.button_3._rect)
        SCREEN.blit(self.button_4._picture, self.button_4._rect)
        SCREEN.blit(self.button_exit._picture, self.button_exit._rect)

class SelectingDifficulty(Lobby):

    def __init__(self):
        self.button_1 = DifficultyButton((790, 130), 1)
        self.button_2 = DifficultyButton((790, 240), 2)
        self.button_3 = DifficultyButton((790, 350), 3)

    def draw(self):
        global SCREEN
        SCREEN.blit(self.button_1._picture, self.button_1._rect)
        SCREEN.blit(self.button_2._picture, self.button_2._rect)
        SCREEN.blit(self.button_3._picture, self.button_3._rect)
        SCREEN.blit(self.button_exit._picture, self.button_exit._rect)


def set_cells(table):
    """Set not empty table cells fixed"""

    global fix_cells
    fix_cells = []
    for cell in range(TABLE_SIZE):
        if table[cell]:
            fix_cells += [cell]


def draw_grid():
    """Draw grid for sudoku and numbers in table"""
    
    global sudoku
    for i in range(1, TABLE_SIDE):
        width = 5 if i % 3 == 0 else 1
        pygame.draw.line(SCREEN, GOOD_MASSAGE_COLOR, [40 + 70*i, 40], [40 + 70*i, 670], width)
        pygame.draw.line(SCREEN, GOOD_MASSAGE_COLOR, [40, 40 + 70*i], [670, 40 + 70*i], width)

    for i in range(TABLE_SIDE):
        for j in range(TABLE_SIDE):
            if sudoku[i + j * TABLE_SIDE] != 0:
                txt = FONT.render(str(sudoku[i + j * TABLE_SIDE]), 1, NUMBER_COLOR)
                SCREEN.blit(txt, (60 + 70*i, 50 + 70*j))

def draw_massage():
    """Write current massage"""
    
    global massage, massage_color
    txt = FONT.render(massage, 1, massage_color)
    SCREEN.blit(txt, (60, 680))

def draw_special_cells():
    """Draw 1) Selected cell; 2) Cell where our mouse is; 3) Wrong filled cells"""
    
    global wrong_filled_cells, mouse, fix_cells

    # selected cell
    pygame.draw.rect(SCREEN, SELECTED_CELL_COLOR, selection)

    # wrong filled cells
    for cell in wrong_filled_cells:
        l, k = cell // TABLE_SIDE, cell % TABLE_SIDE
        pygame.draw.rect(SCREEN, BAD_MASSAGE_COLOR, (40 + 70*k, 40 + 70*l, 70, 70))

    # mouse-on cell
    if (mouse[0] in range(40, 670)) and (mouse[1] in range(40, 670)):
        k, l = (mouse[0] - 40) // 70, (mouse[1] - 40) // 70
        pygame.draw.rect(SCREEN, MOUSE_ON_COLOR, (40+70*k, 40+70*l, 70,70))

    # fix cells
    for cell in fix_cells:
        l, k = cell // TABLE_SIDE, cell % TABLE_SIDE
        pygame.draw.rect(SCREEN, FIX_CELL_COLOR, (40 + 70*k, 40 + 70*l, 70, 70))
    

def draw_interface():
    """Draw all what has to be on screen"""
    
    SCREEN.fill(FONE_COLOR)
    frame_rect = FRAME.get_rect(bottomright = (830, 0))
    SCREEN.blit(FRAME, frame_rect)
    draw_special_cells()
    draw_grid()
    draw_massage()
    lobby.draw()

def check_cell(inp_cell):
    """Check cells for sudoku rules"""
    
    global sudoku, wrong_filled_cells

    cell_str = [9 * (inp_cell // TABLE_SIDE) + i for i in range(TABLE_SIDE)]
    cell_col = [inp_cell % TABLE_SIDE + TABLE_SIDE * i for i in range(TABLE_SIDE)]
    bl = (inp_cell % TABLE_SIDE) // BLOCK_SIDE + (inp_cell // TABLE_SIDE) // BLOCK_SIDE * BLOCK_SIDE
    cell_block = []
    for i in range(BLOCK_SIDE):
        for j in range(BLOCK_SIDE):
            cell_block += [bl // BLOCK_SIDE * TABLE_SIDE * BLOCK_SIDE + 3 * (bl % BLOCK_SIDE) + TABLE_SIDE * i + j]
    influence_zone = set(cell_str + cell_col + cell_block)

    for cell in influence_zone:
        if ((sudoku[cell] == sudoku[inp_cell]) and
            (sudoku[inp_cell] != 0) and
            (cell != inp_cell)):
            wrong_filled_cells += [inp_cell, cell]
            wrong_filled_cells = list(set(wrong_filled_cells))
            return

    try:
        wrong_filled_cells.remove(inp_cell)
    except BaseException:
        pass
    

selection = (-1,-1,-1,-1)
sudoku = [0] * TABLE_SIZE
mode = 'lobby'
wrong_filled_cells = []
massage = 'Welcome!'
massage_color = GOOD_MASSAGE_COLOR
num_of_selected_cell = 0
selected_cell = 39
lobby = StartLobby()
fix_cells = []

pygame.display.set_icon(ICON)
pygame.display.set_caption('Sudoku (by F.L.)')
pygame.display.update()

while True:

    CLOCK.tick(FPS)

    pygame.display.set_caption('Sudoku (by F.L.)')

    mouse = pygame.mouse.get_pos()

    draw_interface()
    frame_rect = FRAME.get_rect(bottomright = (830, 760))
    SCREEN.blit(FRAME, frame_rect)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif (event.type == pygame.MOUSEBUTTONDOWN and
              SUDOKU_FIELD.collidepoint(mouse)):
            k, l = (mouse[0] - 40) // 70, (mouse[1] - 40) // 70
            selection = (40+70*k, 40+70*l, 70, 70)
            selected_cell = l * TABLE_SIDE + k

        elif event.type == pygame.MOUSEBUTTONUP:

            if BUTTON_1_RECT.collidepoint(mouse):
                lobby.button_1.action()
            elif BUTTON_2_RECT.collidepoint(mouse):
                lobby.button_2.action()
            elif BUTTON_3_RECT.collidepoint(mouse):
                lobby.button_3.action()
            elif BUTTON_4_RECT.collidepoint(mouse):
                lobby.button_4.action()
            elif BUTTON_5_RECT.collidepoint(mouse):
                lobby.button_5.action()
            elif BUTTON_EXIT_RECT.collidepoint(mouse):
                lobby.button_exit.action()


        elif event.type == pygame.KEYDOWN:
            try:
                key = NUM_KEY_SET.index(event.key)
                if not (selected_cell in fix_cells):
                    sudoku[selected_cell] = key
                    for cell in wrong_filled_cells + [selected_cell]:
                        check_cell(cell)
            except ValueError:
                pass
                
    pygame.display.update()
