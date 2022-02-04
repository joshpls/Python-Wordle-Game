#   ----------------------------    #
#          WORDLE - Python          #
#   ----------------------------    #

import random
import pygame, sys

pygame.init()

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
        if len(word) == 5:
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
    fnt = pygame.font.SysFont("cambria", 40)
    small_fnt = pygame.font.SysFont("cambria", 10)
    fnt2 = pygame.font.SysFont("cambria", 15)
    word = generateWord()
    guess = ""
    input_active = True
    active_row = 0
    active_col = 0
    guessed = {}
    
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    
    board = Board(win, w, h, rows, cols)

    board.draw()

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
                    if event.key == pygame.K_RETURN:
                        if isValidWord(guess):
                            input_active = False
                            
                            guessed = GetCorrectGuesses(board, active_row, word, guess, guessed)

                            if len(guessed) > 0:
                                guessedLetters = ""

                                for key in guessed:
                                    guessedLetters = guessedLetters + key + ", "

                                valueTxt = fnt2.render(str(guessedLetters), 0, WHITE)
                                win.blit(valueTxt, (10, 510))

                            if checkWin(word, guess):
                                print("You won! The word was", word)
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
                        input_active = True
                        word = generateWord()
        
        if active_row > rows-1 and input_active:
            print("Game Over! Ran out of guesses! The word was", word)
            input_active = False
        
        
        board.draw()
        
        pygame.display.update()