#   ----------------------------    #
#          WORDLE - Python          #
#   ----------------------------    #

import random
import pygame, sys
import re

pygame.init()

class Button:
    def __init__(self, text, width, height, pos, win, font):
        self.win = win
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos,(width, height))
        self.top_color = (86, 87, 88)   #"#475F77"

        # text
        self.text_surface = self.font.render(text,True,"#FFFFFF")
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)

    def setColor(self, value):
        GREEN = (83, 141, 78)
        YELLOW = (181, 159, 59)
        BACKGROUND = (18, 18, 19)
        DARKGREY = (86, 87, 88)

        if value == 2:
            #Letter is in word and in correct position
            self.top_color = GREEN
        elif value == 1:
            #Letter is in word and in wrong position
            self.top_color = YELLOW
        elif value == 0:
            #Letter is not in word
            self.top_color = BACKGROUND
        else:
            #Letter hasn't been guessed yet
            self.top_color = DARKGREY

        self.draw()

    
    def draw(self):
        pygame.draw.rect(self.win, self.top_color, self.top_rect, border_radius = 6)
        self.win.blit(self.text_surface, self.text_rect)
    
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        self.pressed = False
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = "#D74B4B"
        else:
            self.top_color = "#475F77"
    
    def check_pressed(self):
        return self.pressed == True

class Node:
    GREEN = (83, 141, 78)
    YELLOW = (181, 159, 59)
    BACKGROUND = (18, 18, 19, 0.5)
    DARKGREY = (86, 87, 88, 0.5)
    GREY = (128, 128, 128)
    WHITE = (255, 255, 255)

    def __init__(self, row, col, width, height, win):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * height
        self.value = ""
        self.color = self.BACKGROUND
        self.width = width
        self.height = height
        self.win = win

    def get_pos(self):
        return self.col, self.row

    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

    def set_guess(self, value):
        if value == 2:
            self.color = self.GREEN
        elif value == 1:
            self.color = self.YELLOW
        else:
            self.color = self.DARKGREY

    def get_guess(self):
        return self.color
    
    def is_empty(self):
        if self.value == "":
            return True
    
    def reset(self):
        self.value = ""
        self.color = self.BACKGROUND

    def draw(self):
        line = 2
        #draw node color for guess
        pygame.draw.rect(self.win, self.GREY, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.win, self.get_guess(), (self.x, self.y, self.width-4, self.height-4))

        # top line
        #pygame.draw.rect(self.win, self.WHITE, [0,self.x+self.width,self.height+self.y,line])

        #posTxt = small_fnt.render(str(self.get_pos()), 0, self.BLACK)
        valueTxt = fnt.render(str(self.get_value()), 0, self.WHITE)

        #draw coords
        #self.win.blit(posTxt, (self.x, self.y))
        #draw value
        self.win.blit(valueTxt, (self.x + (self.width / 2)-15, self.y + (self.height / 2)-15))

    def __lt__(self,other):
        return False


class Board():
    def __init__(self, win, w, h, rows, cols) -> None:
        self.win = win
        self.w = w
        self.h = h
        self.gap = w // cols
        self.gaph = h // rows
        self.rows = rows
        self.cols = cols
        self.board = self.make_board()

    def make_board(self):
        grid = []

        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                node = Node(j, i, self.gap,self.gaph, self.win)
                grid[i].append(node)
        
        return grid

    def reset(self):
        for row in self.board:
            for node in row:
                node.reset()

    def set_letter(self, letter, row, col):
        self.board[row][col].set_value(letter)
    
    def del_letter(self, row, col):
        self.board[row][col].reset()
    
    def set_color(self, row, col, value):
        self.board[row][col].set_guess(value)

    def draw(self):
        BLACK = (0,0,0, 0.5)

        line = 8

        for row in self.board:
            for node in row:
                node.draw()

        for i in range(self.rows):
            pygame.draw.line(self.win, BLACK, (0, i * self.gaph), (self.h, i * self.gaph), line)
            for j in range(self.cols):
                pygame.draw.line(self.win, BLACK, (j * self.gap, 0), (j * self.gap, self.h), line)

        # top line
        pygame.draw.rect(self.win, BLACK, [0,0,self.w,line])
        # bottom line
        pygame.draw.rect(self.win, BLACK, [0,self.h,self.w,line])
        # left line
        pygame.draw.rect(self.win, BLACK, [0,0,line, self.h])
        # right line
        pygame.draw.rect(self.win, BLACK, [self.w-line,0,line, self.h+line])
        pygame.display.update()

def isValidWord(word):
    if word.isalpha():
        return True
    return False

def GetCorrectGuesses(board, active_row, word, guess, guessed):
    for i in range(len(word)):

        if word[i] == guess[i]:
            word = word.replace(guess[i], " ", 1)
            board.set_color(active_row,i,2)
            if guess[i] in guessed.keys():
                if guessed[guess[i]] < 2:
                    guessed[guess[i]] = 2
            else:
                guessed[guess[i]] = 2

        elif word.find(guess[i]) > -1:
            word = word.replace(guess[i], " ", 1)
            board.set_color(active_row,i,1)
            if guess[i] in guessed.keys():
                if guessed[guess[i]] < 1:
                    guessed[guess[i]] = 1
            else:
                guessed[guess[i]] = 1

        else:
            board.set_color(active_row,i,0)
            if not guess[i] in guessed.keys():
                guessed[guess[i]] = 0

    return guessed

def updateGuessColor(guessed):
    for key, value in guessed.items():
        if key == 'A':
            AButton.setColor(value)
        if key == 'B':
            BButton.setColor(value)
        if key == 'C':
            CButton.setColor(value)
        if key == 'D':
            DButton.setColor(value)
        if key == 'E':
            EButton.setColor(value)
        if key == 'F':
            FButton.setColor(value)
        if key == 'G':
            GButton.setColor(value)
        if key == 'H':
            HButton.setColor(value)
        if key == 'I':
            IButton.setColor(value)
        if key == 'J':
            JButton.setColor(value)
        if key == 'K':
            KButton.setColor(value)
        if key == 'L':
            LButton.setColor(value)
        if key == 'M':
            MButton.setColor(value)
        if key == 'N':
            NButton.setColor(value)
        if key == 'O':
            OButton.setColor(value)
        if key == 'P':
            PButton.setColor(value)
        if key == 'Q':
            QButton.setColor(value)
        if key == 'R':
            RButton.setColor(value)
        if key == 'S':
            SButton.setColor(value)
        if key == 'T':
            TButton.setColor(value)
        if key == 'U':
            UButton.setColor(value)
        if key == 'V':
            VButton.setColor(value)
        if key == 'W':
            WButton.setColor(value)
        if key == 'X':
            XButton.setColor(value)
        if key == 'Y':
            YButton.setColor(value)
        if key == 'Z':
            ZButton.setColor(value)
            

def drawGuessedLetters():
    QButton.setColor(-1)
    WButton.setColor(-1)
    EButton.setColor(-1)
    RButton.setColor(-1)
    TButton.setColor(-1)
    YButton.setColor(-1)
    UButton.setColor(-1)
    IButton.setColor(-1)
    OButton.setColor(-1)
    PButton.setColor(-1)
    AButton.setColor(-1)
    SButton.setColor(-1)
    DButton.setColor(-1)
    FButton.setColor(-1)
    GButton.setColor(-1)
    HButton.setColor(-1)
    JButton.setColor(-1)
    KButton.setColor(-1)
    LButton.setColor(-1)
    ZButton.setColor(-1)
    XButton.setColor(-1)
    CButton.setColor(-1)
    VButton.setColor(-1)
    BButton.setColor(-1)
    NButton.setColor(-1)
    MButton.setColor(-1)

def checkWin(word, guess):
    if word == guess:
        return True
    return False

def generateWord():
    lines = open('wordle_dict.txt').read().splitlines()
    word = random.choice(lines)
    word = word.upper()
    return word


if __name__ == "__main__":
    win = pygame.display.set_mode((500, 800))
    pygame.display.set_caption("WORLDE: by Joshua Kindelberger")

    rows = 6
    cols = 5
    w = 500
    h = 500
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    GREEN = (83, 141, 78)
    RED = (201, 67, 52)
    fnt = pygame.font.SysFont("cambria", 40)
    small_fnt = pygame.font.SysFont("cambria", 10)
    fnt2 = pygame.font.SysFont("cambria", 20)
    word = generateWord()
    guess = ""
    input_active = True
    active_row = 0
    active_col = 0
    guessed = {}
    regex = "^[A-Za-z]+$"
    
    board = Board(win, w, h, rows, cols)

    board.draw()

    #Initiate First Row of Letters
    QButton = Button("Q", 30, 30, (55, 550), win, fnt2)
    QButton.draw()
    WButton = Button("W", 30, 30, (95, 550), win, fnt2)
    WButton.draw()
    EButton = Button("E", 30, 30, (135, 550), win, fnt2)
    EButton.draw()
    RButton = Button("R", 30, 30, (175, 550), win, fnt2)
    RButton.draw()
    TButton = Button("T", 30, 30, (215, 550), win, fnt2)
    TButton.draw()
    YButton = Button("Y", 30, 30, (255, 550), win, fnt2)
    YButton.draw()
    UButton = Button("U", 30, 30, (295, 550), win, fnt2)
    UButton.draw()
    IButton = Button("I", 30, 30, (335, 550), win, fnt2)
    IButton.draw()
    OButton = Button("O", 30, 30, (375, 550), win, fnt2)
    OButton.draw()
    PButton = Button("P", 30, 30, (415, 550), win, fnt2)
    PButton.draw()

    #Initiate Second Row of Letters
    AButton = Button("A", 30, 30, (75, 590), win, fnt2)
    AButton.draw()
    SButton = Button("S", 30, 30, (115, 590), win, fnt2)
    SButton.draw()
    DButton = Button("D", 30, 30, (155, 590), win, fnt2)
    DButton.draw()
    FButton = Button("F", 30, 30, (195, 590), win, fnt2)
    FButton.draw()
    GButton = Button("G", 30, 30, (235, 590), win, fnt2)
    GButton.draw()
    HButton = Button("H", 30, 30, (275, 590), win, fnt2)
    HButton.draw()
    JButton = Button("J", 30, 30, (315, 590), win, fnt2)
    JButton.draw()
    KButton = Button("K", 30, 30, (355, 590), win, fnt2)
    KButton.draw()
    LButton = Button("L", 30, 30, (395, 590), win, fnt2)
    LButton.draw()

    #Initiate Third Row of Letters
    ZButton = Button("Z", 30, 30, (115, 630), win, fnt2)
    ZButton.draw()
    XButton = Button("X", 30, 30, (155, 630), win, fnt2)
    XButton.draw()
    CButton = Button("C", 30, 30, (195, 630), win, fnt2)
    CButton.draw()
    VButton = Button("V", 30, 30, (235, 630), win, fnt2)
    VButton.draw()
    BButton = Button("B", 30, 30, (275, 630), win, fnt2)
    BButton.draw()
    NButton = Button("N", 30, 30, (315, 630), win, fnt2)
    NButton.draw()
    MButton = Button("M", 30, 30, (355, 630), win, fnt2)
    MButton.draw()

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if input_active:
                    if event.key == pygame.K_RETURN and len(guess) == cols:
                        if isValidWord(guess):
                            input_active = False
                            
                            guessed = GetCorrectGuesses(board, active_row, word, guess, guessed)

                            if len(guessed) > 0:
                                updateGuessColor(guessed)

                            if checkWin(word, guess):
                                dispTxt = "CONGRATS! YOU WON!"
                                valueTxt = fnt2.render(str(dispTxt), 0, GREEN)
                                win.blit(valueTxt, (140, 510))
                                input_active = False
                            else:
                                active_row += 1
                                active_col = 0
                                guess=""
                                input_active = True
                        else:
                            print("Invalid Word")
                    elif event.key == pygame.K_BACKSPACE:
                        if active_col > 0:
                            active_col -= 1
                        board.del_letter(active_row, active_col)
                        guess = guess[:-1]

                    else:
                        if active_col < cols:
                            letter = event.unicode.upper()
                            if re.match(regex, letter):
                                board.set_letter(letter, active_row, active_col)
                                active_col += 1
                                guess += letter
                else:
                    if event.key == pygame.K_SPACE:
                        board.reset()
                        active_col = 0
                        active_row = 0
                        guess = ""
                        guessed = {}
                        win.fill(BLACK)
                        drawGuessedLetters()
                        input_active = True
                        word = generateWord()
        
        if active_row > rows-1 and input_active:
            dispTxt = "RAN OUT OF GUESSES! THE WORD WAS: " + word
            valueTxt = fnt2.render(str(dispTxt), 0, RED)
            win.blit(valueTxt, (30, 510))
            input_active = False
        
        
        board.draw()
        
        pygame.display.update()