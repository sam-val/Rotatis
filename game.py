from libs import Board, MyRect, Display
import pprint
import pygame
import copy
import random
from collections import namedtuple
import time
from tkinter import messagebox as mb
import tkinter
from tkinter import ttk
import pickle
from pathlib import Path
from datetime import datetime

# GLOBAL/SETTING VARIABLES:
BOARD_W = 6
BOARD_H = 6
SCREEN_WIDTH = 9
SCREEN_HEIGHT = 8
MENU_W = 3
MENU_H = 6
FRAME_RATE = 30
TITLE = "Rotatis"
CUBE_WIDTH = 100
PLAYTER_TIME = 60
DEFAULT_LEVEL = 0
RECORDS_PATH = "./.records.pickle"


CLOCK_POS_X = SCREEN_WIDTH - 1
CLOCK_POS_Y = 0.5

turn_commands = ['left', 'right', 'horizontal', 'vertical']

# settings
Settings = namedtuple('Settings', 'shapes_num moves_num time_reward')
normal = Settings(shapes_num=3, moves_num=3, time_reward=8)
easy = Settings(shapes_num=1, moves_num=3, time_reward=30)
hard = Settings(shapes_num=4, moves_num=4, time_reward=5)

Score = namedtuple("Score", "name difficulty level time_spent time_stamp")

DIFFICULTY_SETTINGS = {'easy':easy, 'normal': normal, 'hard': hard}

## COLOURS:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 26, 0)
BRIGHT_RED = (170,1,20)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
BEIGE = (250, 175, 0)
AQUA = (128, 206, 207)
DARK_GREY = (64, 64, 64)
YELLOW = (255, 204, 0)
PURPLE = (148,0,211)
ORANGE = (255,106,2)
INDIGO = (75,0,130)
VIOLET = (238,130,238)
PINK = (231,84,128)
BROWN = (102,51,0)
CYAN = 0,173,238
SHAPE_COLOUR = ORANGE
CLICK_BUTTON_COLOUR = PINK
SIDE_SHAPE_COLOUR = ORANGE

#functions:

def checkBoard(*args, **kwargs):
    global time_adding
    global compare_text
    global remaining_time
    global display
    global swear
    global  result_board_array
    global compare_text_start
    global swear_start
    global swear_text
    global difficulty
    global current_time_reward
    global currentSettings
    if result_board_array == []:
        print("result board is empty")
        return
    def ridBorders(board):
        b = []
        for y in range(board.h):
            for x in range(board.w):
                if not board.checkIfBorder(x, y):
                    ob = board.array[x + y * board.w]
                    b.append(ob)
        return b

    b2 = ridBorders(field)
    b1 = result_board_array
    print('board b2')
    print_board(b2)
    print('board b1')
    print_board(b1)



    if compareShapes(b1, b2):
        ## if correct:
        remaining_time += currentSettings['current_time_reward']
        check_current_level(remaining_time) ## adjust current level
        set_settings() ## adjust settings
        set_puzzle(currentSettings)
        time_adding = True
        display = "correct"
        if not compare_text:
            compare_text = True
        compare_text_start = True
    else:
        if not compare_text:
            compare_text=True
        compare_text_start = True
        display = "WRONG!"

        if not swear:
            swear = True
        swear_start = True
        swear_adj = random.choice(adjs_cleaned)
        swear_noun = random.choice(nouns_cleaned)

        swear_text =  swear_adj + " " + swear_noun
        swear_text = swear_text.capitalize() + "!!!"
        global swear_x,swear_y
        swear_x = random.randint(0, CUBE_WIDTH * (SCREEN_WIDTH-3))
        swear_y = random.randint(0,CUBE_WIDTH * (SCREEN_HEIGHT-2))


def compareShapes(b1,b2):
    # def findFirstElem(list):
    #     x = None
    #     for i, ob in enumerate(list):
    #         if ob.click == True:
    #             x = i
    #             break
    #     return x
    #
    # b1_first = findFirstElem(b1)
    # # print(b1_first)
    # b2_first = findFirstElem(b2)
    # # print(b2_first)
    # if b1_first == None or b2_first == None:
    #     return False
    #
    # first_list = b1[b1_first:]
    # second_list = b2[b2_first:]
    #
    #
    # for x,y in zip(first_list, second_list):
    #     pair = x.click,y.click
    #     if pair != (True, True) and pair != (False, False):l
    #         return False
    # return True
    if (len(b1) != len(b2)):
        return False

    for x,y in zip(b1,b2):
       pair = x.click,y.click
       if pair != (True,True) and pair != (False,False):
           return False
    return True


def makeRandomShape(settings):
    global side_field
    global difficulty
    side_field.init_array()
    cubes = side_field.array
    rans = []
    chooseRandomElement(settings['current_shapes_num'], cubes, rans)
    for r in rans:
        r.colour = SIDE_SHAPE_COLOUR
        r.click = True

    print("side field after random():")
    print_board(side_field.array)
    global result_board_array
    result_board_array = copy.deepcopy(side_field.array)

def turnRandom(settings):
    global difficulty
    global result_board_array
    commands = []
    for _ in range(settings['current_moves_num']):
        command = random.choice(turn_commands)
        # command = 'vertical'
        commands.append(command)
        move(command=command)

    print(commands)
    return commands

def chooseRandomElement(n, l, result_l):
    import random
    for i in range(n):
        if len(result_l) == n:
            return
        r = random.choice(l)
        if r not in result_l:
            result_l.append(r)
        else:
            chooseRandomElement(n, l, result_l)
            return

def time_added_animation():
    global time_added_ani_alpha
    global time_added_ani_start_time
    global time_added_ani_start
    global current_time_reward
    if time_added_ani_start:
        time_added_ani_start_time = time.time()
        time_added_ani_start = False

    reward = current_time_reward
    text = "+" + str(reward)
    original_sur = font.render(text, True, ORANGE)
    text_sur = original_sur.copy()
    alpha_sur = pygame.Surface(text_sur.get_size(), pygame.SRCALPHA)
    fading_speed = 4
    t2 = time.time()
    if t2 - time_added_ani_start_time > 1:
        if time_added_ani_alpha > 0:
            time_added_ani_alpha = max(time_added_ani_alpha - fading_speed, 0)
            text_sur = original_sur.copy()
            alpha_sur.fill((255, 255, 255, time_added_ani_alpha))
            text_sur.blit(alpha_sur, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            global time_adding
            time_adding = False
            time_added_ani_alpha = 255
            time_added_ani_start = True
            return
    # animation loop:
    display_ob.display_textSur(CUBE_WIDTH * CLOCK_POS_X, CUBE_WIDTH * 0.7, text_sur=text_sur)

def fade_text(state, alpha, start_time, start,staying_still_time,text, x , y,
              colour=ORANGE, centeredY = False, centeredX=False,
              font = None, fading_speed=4):
    if font == None:
        print('no font!')
        return
    if globals()[start]:
        globals()[start_time] = time.time()
        globals()[start] = False

    original_sur = font.render(text, True, colour)
    text_sur = original_sur.copy()
    alpha_sur = pygame.Surface(text_sur.get_size(), pygame.SRCALPHA)
    t2 = time.time()
    if t2 - globals()[start_time] > globals()[staying_still_time]:
        if globals()[alpha] > 0:
            globals()[alpha] = max(globals()[alpha] - fading_speed, 0)
            text_sur = original_sur.copy()
            alpha_sur.fill((255, 255, 255, globals()[alpha]))
            text_sur.blit(alpha_sur, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            globals()[state] = False
            globals()[alpha] = 255
            globals()[start] = True
            return
    # animation loop:
    display_ob.display_textSur(x, y, text_sur=text_sur,centeredX=centeredX,centeredY=centeredY)

def exit_game(*args, **kwargs):
    global running
    if confirmBox("Quitting game", "Are you sure, dear?"):
        running = False

def pause_game(*args, **kwargs):
    global paused
    global side
    paused = not paused
    print('game is','paused' if paused else 'resumed')

    if not paused:

        print('reset the puzzle')
        set_puzzle(currentSettings)

def change_colour_wrapper(to_colour, from_colour):
    def change_colour(*args, **kwargs):
        rect = kwargs['currentRect']
        board = kwargs['currentBoard']
        if rect.click:
            if to_colour:
                rect.colour = to_colour
            else:
                rect.colour = SHAPE_COLOUR
        else:
            if from_colour:
                rect.colour = from_colour
            else:
                rect.colour = DARK_GREY

    return change_colour

def move(command):
    # pass in the non bordered board
     # 0,1,2,3 is rotate left, rotate right, flip honrizontally, flip vertically respectively
    global side_field
    global result_board_array
    board = side_field
    shapes = []
    if command in turn_commands:
        print('move: ', command)
        for x in range(board.w):
            for y in range(board.h):
                cur_pos = x+y*board.w
                rect = result_board_array[cur_pos]
                if rect.click:
                    changed_pos = None
                    if command == 'left':
                        changed_pos = (board.w*(board.h-1)) - board.w*x + y
                    elif command == 'right':
                        changed_pos = (board.w-1) + board.w*x - y
                    elif command == 'horizontal':
                        changed_pos = (board.w-1) - x + y*board.w
                    elif command == 'vertical':
                        changed_pos = (board.w*(board.h-1)) + x - y*board.w

                    shapes.append(changed_pos)

    result_board_array = side_field.make_new_array()
    for i in shapes:
        result_board_array[i].colour = SIDE_SHAPE_COLOUR
        result_board_array[i].click = True
    print_board(result_board_array)

def print_board(board):
    global side_field
    for y in range(side_field.h):
        for x in range(side_field.w):
            print("X" if board[x + y * side_field.w].click else '0',end=", ")
        print("")
    print("")





def count_down_clock(*args, **kwargs):
    global remaining_time
    global start_time
    global elapse
    sec = 1
    cur_time = time.time()
    if not paused:
        elapse = cur_time - start_time
        if elapse >= sec:
                start_time = time.time()
                remaining_time -= 1
    else:
        start_time = cur_time - elapse

def set_puzzle(settings):
    makeRandomShape(settings)
    turnRandom(settings)


def reset_game():
    global remaining_time
    global display
    global currentSettings
    global side_field
    global field
    global current_level
    remaining_time = PLAYTER_TIME
    display = ""
    current_level = 0
    set_settings()
    side_field.array = side_field.make_new_array()
    field.array = field.make_new_array()
    if not paused:
        pause_game()

def user_reset_game(*args, **kwargs
                    ):
    if confirmBox("Resetting game", "Are you sure?"):
        reset_game()

def confirmBox(title,content):
    root = tkinter.Tk()
    root.withdraw()
    rs = mb.askokcancel(title, content)
    root.destroy()
    return rs
    # label = tkinter.Label(root, text="Are you sure?")
    # label.place(anchor='n', relheight=1, relwidth=1)

def record_player(root,record):
    global records
    global cleaned_records
    global difficulty
    with open(RECORDS_PATH, "wb") as data:
        records.append(record)
        pickle.dump(records, data)
    # ## also update the cleaned_records:
    # cleaned_records.append(record)
    # cleaned_records = sort_records(difficulty, cleaned_records)
    root.destroy()


def finish(lose = True):
    global current_level
    global total_elapse
    global difficulty

    def set_records():
        name = text_field.get()
        score = Score(name=name, difficulty=difficulty,
                      level=current_level,
                      time_spent=total_elapse, time_stamp=datetime.now())
        record_player(root,score)

    time_spent = display_ob.convert(int(total_elapse))
    root = tkinter.Tk()
    if lose:
        root.title = "Game Over!"
        label = tkinter.Label(root, text= f"You Lost!\nLevel: {current_level}\n"
                                          f"Total time spent: {time_spent}\nEnter your name here:")
    else:
        root.title = "YOU WON!!"
        label = tkinter.Label(root, text="You Won!\nTotal time spent:  " + display_ob.convert(
    int(total_elapse)) + "\nEnter your name here:")
    text_field = tkinter.Entry(root)


    # label.place(anchor='n',relheight=1, relwidth=1)
    button = tkinter.Button(root, text='ok', command = set_records)
    label.grid(row=0, columnspan=2)
    text_field.grid(row=1,column=0)
    button.grid(row=1, column=1)

    root.mainloop()
    reset_game()

def set_settings():
    global currentSettings
    global current_level
    global remaining_time
    level = current_level
    if level == 0:
        currentSettings['current_shapes_num'] = DIFFICULTY_SETTINGS[difficulty].shapes_num
        currentSettings['current_moves_num'] = DIFFICULTY_SETTINGS[difficulty].moves_num
        currentSettings['current_time_reward'] = DIFFICULTY_SETTINGS[difficulty].time_reward
    elif level >= 4:
        currentSettings['current_moves_num'] = DIFFICULTY_SETTINGS[difficulty].moves_num + 3
        currentSettings['current_shapes_num'] = DIFFICULTY_SETTINGS[difficulty].moves_num + 3
    elif level == 3:
        currentSettings['current_shapes_num'] = DIFFICULTY_SETTINGS[difficulty].shapes_num + 2
        currentSettings['current_moves_num'] = DIFFICULTY_SETTINGS[difficulty].moves_num + 2
    elif level == 2:
        currentSettings['current_moves_num'] = DIFFICULTY_SETTINGS[difficulty].moves_num + 1
    elif level == 1:
        currentSettings['current_shapes_num'] = DIFFICULTY_SETTINGS[difficulty].shapes_num + 1

def check_current_level(time):
    global current_level
    if time >= 60*5:
        level = 4
    elif time >= 60*4:
        level = 3
    elif time >= 60*3:
        level = 2
    elif time >= 60*2:
        level = 1
    else:
        level = 0
    
    current_level = max(current_level, level)

def sort_records(difficulty, records):
    ### sort and return top 10
    def by_time_spent(x):
        return x.time_spent
    def by_time_stamp(x):
        return x.time_stamp
    def by_level(x):
        return x.level
    records = list(filter(lambda x: x.difficulty==difficulty, records))
    records.sort(key=by_time_stamp,reverse=True)
    records.sort(key=by_time_spent)
    records.sort(key=by_level, reverse=True)

    length = len(records)
    quanity = 10
    return records[:length] if length < quanity else records[:quanity]

def display_high_scores(*args, **kwargs):
    global records
    global difficulty
    def close():
        root.destroy()
    ### clean up, sort and arrange the score records - as a list:
    cleaned_records = sort_records(difficulty, records)

    root = tkinter.Tk()
    root.title("High Scores")
    h_title = tkinter.Label(root, text='Top 10 High Scores')

    # create columns and table:
    cols = ('No.', 'Name', 'Difficult', 'Level', 'Time Spent', 'Time Stamp')
    table = ttk.Treeview(root, column=cols, show='headings')
    exit_button = tkinter.Button(root,text='Close', width=50, command=close)

    ## set columns headings:
    for i, c in enumerate(cols):
        table.heading(c, text=c, anchor=tkinter.N)
        width = 0
        if i == len(cols)-1:
            width = 200
        elif i== 1:
            width = 200
        elif i == 0:
            width = 50
        else:
            width = 100
        table.column(i, width=width)

    ## populate
    for index, score in enumerate(cleaned_records,start=1):
        time_stamp = score.time_stamp.strftime("%Y/%m/%d -- %H:%M:%S")
        time_spent = display_ob.convert(score.time_spent)
        table.insert(parent="", index='end',
                     values=(index, score.name.upper(), score.difficulty.upper(), score.level
                             ,time_spent,time_stamp))
    h_title.grid(row=0, columnspan=5)
    table.grid(row=1, columnspan=1)
    exit_button.grid(row=2,columnspan=5)

    root.resizable(False, False)
    root.mainloop()


#classes:
class Field(Board):
    def draw(self):
        pass

    def update(self):
        pass

class Side(Board):
    def __init__(self, screen, x, y, width, height, cube_width, cube_height, rect):
        super().__init__(screen, x, y, width, height, cube_width, cube_height, rect, border= False)

    def update(self):
        global game_state_text
        global game_state_text_colour
        side.array[0].colour = BLACK if paused else RED

        game_state_text = "START" if paused else "PAUSE"

class MyDisplay(Display):
    def my_display_clock(self, x, y, secs=0, colour = None, font=None, bg = None, centeredX = False, centeredY=False):
        if secs < 20:
            colour = RED
        self.display_clock(x,y,secs=secs,colour=colour,font=font,bg=bg,centeredX=centeredX,centeredY=centeredY)


# game initilization
pygame.mixer.pre_init()
pygame.init()
scr = pygame.display.set_mode((SCREEN_WIDTH*CUBE_WIDTH, SCREEN_HEIGHT*CUBE_WIDTH))

pygame.display.set_caption(TITLE)
scr.fill(BLACK)
pygame.display.flip()

pygame.font.init()
clock = pygame.time.Clock()

# assets -- elements -- objects:
field_rect_func = change_colour_wrapper(to_colour=SHAPE_COLOUR, from_colour=DARK_GREY)
field_rect = MyRect(border_colour=BLACK, colour=DARK_GREY, line_colour=WHITE, click_colour=SHAPE_COLOUR, func= [field_rect_func])
field = Field(scr, x=CUBE_WIDTH*MENU_W, y=CUBE_WIDTH*(SCREEN_HEIGHT-MENU_H),
              width=BOARD_W, height=BOARD_H,cube_width= CUBE_WIDTH, cube_height=CUBE_WIDTH, rect=field_rect)

side_rect = MyRect(line_colour=WHITE)
side = Side(scr, x=0, y=CUBE_WIDTH * (SCREEN_HEIGHT-MENU_H),
            width=1, height=BOARD_H, cube_width=CUBE_WIDTH * 3, cube_height=CUBE_WIDTH,rect= side_rect)


button_rect = MyRect(colour=CLICK_BUTTON_COLOUR, line_colour=WHITE, func=[checkBoard])
button = Field(scr, x = 0, y = CUBE_WIDTH*1,
               width = SCREEN_WIDTH, height= 1, rect=button_rect, cube_width=CUBE_WIDTH, cube_height=CUBE_WIDTH, border=False, line=None)

# button2_rect = MyRect(colour=BLUE, line_colour=WHITE, func=[makeRandomShape])
# button2 = Field(scr, x = CUBE_WIDTH*7, y = CUBE_WIDTH,
#                width = 1, height= 1, rect=button2_rect, cube_width=CUBE_WIDTH, cube_height=CUBE_WIDTH, border=False)

side_field_rect = MyRect(border_colour=BLACK, colour=DARK_GREY, line_colour=WHITE, click_colour=ORANGE, func= None)
side_field = Field(scr, x=0, y=CUBE_WIDTH*(SCREEN_HEIGHT-MENU_H+1),
              width=BOARD_W-2, height=BOARD_H-2,cube_width= CUBE_WIDTH/7, cube_height=CUBE_WIDTH/7, rect=side_field_rect, border= False)



# Menu buttons:
### pause/start button
side.array[0].colour = BLACK
pause_button_change_colour = change_colour_wrapper(to_colour=RED, from_colour=BLACK)
side.array[0].func = [pause_game]

### box displaying the puzzle
side.array[1].colour = ORANGE

### reset button
side.array[2].colour = YELLOW
side.array[2].func = [user_reset_game]

### high scores
side.array[3].colour = GREEN
side.array[3].func = [display_high_scores]

### help
side.array[4].colour = BLUE

### exit game
side.array[5].colour = INDIGO
side.array[5].func = [exit_game]

# in-game variables:
running = True
paused = True
font_colour = BLACK
result_board_array = []

## user chooses difficulty
difficulty = 'easy'

# current stuff
current_level = 0
currentSettings = { 'shapes_num' :DIFFICULTY_SETTINGS[difficulty].shapes_num,
                 'moves_num': DIFFICULTY_SETTINGS[difficulty].moves_num,
                 'time_reward' : DIFFICULTY_SETTINGS[difficulty].time_reward}

# import stuff from files:
records = []
if Path(RECORDS_PATH).resolve().exists():
    with open(RECORDS_PATH, "rb") as score_data:
        records = pickle.load(score_data)



with open("text/insults_adjectives.txt", 'r') as file:
    adjs = file.readlines()

with open("text/insults_nouns.txt", 'r') as file1:
    nouns = file1.readlines()

### and cleaning them-- removing '\n':
adjs_cleaned = [insult.replace('\n', '') if ('\n' in insult) else insult for insult in adjs ]
nouns_cleaned = [insult.replace('\n', '') if ('\n' in insult) else insult for insult in nouns ]

my_font = 'ubuntu'
font = pygame.font.SysFont(my_font, size = 25, bold=True)
time_added_font = pygame.font.SysFont(my_font, size=40, bold=True)
clock_font = pygame.font.SysFont(my_font, size=60, bold=False)
clock_font_bold = pygame.font.SysFont(my_font, size=60, bold=True)
menu_font = pygame.font.SysFont("dejavusansmono", size=25, bold=False)
compare_font = pygame.font.SysFont(my_font, size=40, bold=True)
swear_font = pygame.font.SysFont(my_font, size=25, bold=True)

# text variables:
display = ""
    # text on the menu:
game_state_text = "START" if paused else "PAUSE"
game_state_text_colour = WHITE

# animation effects variales:
    # fade in & out text:
time_adding = False
time_added_ani_alpha = 255
time_added_ani_start_time = 0
time_added_ani_start = True
time_added_ani_still_time = 1

compare_text = False
compare_text_start = True
compare_text_alpha = 255
compare_text_start_time = 0
compare_text_still_time = 3

swear = False
swear_start = True
swear_alpha = 255
swear_start_time = 0
swear_still_time = 2
swear_x, swear_y = 0,0
swear_text = ""

remaining_time = PLAYTER_TIME
# remaining_time = 5
start_time = 0 # for the count down clock
total_start_time = 0 # for calculating total time
elapse = 0
total_elapse = 0
start_game = True

# non-game objects:
display_ob = MyDisplay(surface=scr, font=font, colour=font_colour)

# GAME LOOP:
while running:
    # timing:
    clock.tick(FRAME_RATE)

    # input & update the game:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            exit_game()
        # mouse clicks:
        if e.type == pygame.MOUSEBUTTONDOWN:
            side.click(e.pos)
            if not paused:
                field.click(e.pos)
                button.click(e.pos)

        #### check current levels and adjusting things accordingly:
    if remaining_time <= 0:
        finish(lose=True)
    elif remaining_time >= 60*6:
        finish(lose=False)

        ####
    check_current_level(remaining_time)
    set_settings()

    # updating the fields
    side.update()
    count_down_clock()
    click_text = "CLICK ME TO CHECK!"
    click_colour = WHITE
    if not paused:
        button.change_colour(CLICK_BUTTON_COLOUR)
        if start_game:
            set_puzzle(currentSettings)
            start_game = False
            total_start_time = time.time()
        cur_time = time.time()
        total_elapse =  cur_time - total_start_time
        # update game elements
        field.update()
    else:
        click_colour = GREEN
        click_text = "click start to play"
        button.change_colour(BLACK)

        total_start_time = time.time() - total_elapse


    # draw and render:
        ## draw border and panels:
    pygame.draw.rect(scr, WHITE, pygame.Rect(0,0,SCREEN_WIDTH*CUBE_WIDTH, CUBE_WIDTH*(SCREEN_HEIGHT-BOARD_H)))

        ## draw buttons and fields:
    side.draw_plain_init()
    field.draw_plain_init()
    button.draw_plain_init()
    side_field.draw_plain_init()

        ## draw menu text:
    display_ob.display_text(x=CUBE_WIDTH*1.5, y=CUBE_WIDTH*2.5, text=game_state_text, centeredY=True,centeredX=True,
                            colour=game_state_text_colour, font=menu_font)
    display_ob.display_text(x=CUBE_WIDTH*1.5, y=CUBE_WIDTH*7.5, text="EXIT", centeredY=True,centeredX=True, colour=WHITE ,font=menu_font)
    display_ob.display_text(x=CUBE_WIDTH*1.5, y=CUBE_WIDTH*5.5, text="HIGH SCORES", centeredY=True,centeredX=True, colour=WHITE, font=menu_font,  )
    display_ob.display_text(x=CUBE_WIDTH*1.5, y=CUBE_WIDTH*4.5, text="RESET", centeredY=True,centeredX=True, colour=WHITE, font=menu_font)
    display_ob.display_text(x=CUBE_WIDTH*1.5, y=CUBE_WIDTH*6.5, text="HELP", centeredY=True,centeredX=True, colour=WHITE, font=menu_font)
    ### display the level label:
    level = 'level {}'.format(str(current_level if current_level < 4 else ""))
    display_ob.display_text(x=CUBE_WIDTH*0.5, y=CUBE_WIDTH*0.15, text=level, centeredY=False,centeredX=False, colour=BLACK, font=clock_font)
    if current_level == 4:
        display_ob.display_text(x=CUBE_WIDTH*1.1, y=CUBE_WIDTH*0.15, text=''.join([' ' for x in level]) + 'S',
                                centeredY=False,centeredX=False, colour=YELLOW, font=clock_font_bold)

    # display_ob.display_text(CUBE_WIDTH * 3, CUBE_WIDTH * 1, text=display, centeredX=False)
    display_ob.my_display_clock(CUBE_WIDTH * CLOCK_POS_X, CUBE_WIDTH * CLOCK_POS_Y,
                                secs=remaining_time, centeredX=True, centeredY=True,
                                font=clock_font)


    display_ob.display_text(x=CUBE_WIDTH * (SCREEN_WIDTH/2), y=CUBE_WIDTH * 1.5, text=click_text, centeredY=True, centeredX=True,
                            colour=click_colour)
    ## draw affects:
    if time_adding:
        reward = currentSettings['current_time_reward']
        text = "+" + str(reward)
        fade_text('time_adding', 'time_added_ani_alpha', 'time_added_ani_start_time',
                  'time_added_ani_start', 'time_added_ani_still_time', text,
                  x=CUBE_WIDTH*CLOCK_POS_X, y=CUBE_WIDTH*CLOCK_POS_Y*0.3,colour=ORANGE, font=time_added_font,centeredY=True,
                  centeredX=True)

    if compare_text:
        colour = GREEN if display != 'WRONG!' else RED
        fade_text('compare_text', 'compare_text_alpha', 'compare_text_start_time',
                  'compare_text_start','compare_text_still_time',display,
                  x=CUBE_WIDTH*(SCREEN_WIDTH/2),y=CUBE_WIDTH*0.5,colour=colour, centeredX=True,centeredY=True, font=compare_font)
    if swear:
        fade_text('swear', 'swear_alpha', 'swear_start_time',
                  'swear_start','swear_still_time',text=swear_text,
                  x=swear_x,y=swear_y,colour=CYAN,font=swear_font,
                  fading_speed= 6
                  )
        ## executing drawing & rendering:
    pygame.display.flip()

pygame.quit()






