import os.path
import tkinter
import glob
import pickle
import re
from tkinter import filedialog

piece_selector = 0
level_name = ""
grid = []
master = tkinter.Tk()
option_buttons_column = 6  # constant


def get_piece_string():
    global piece_selector
    nr_str = str(piece_selector)
    if piece_selector == 0:
        nr_str = "   "
    elif piece_selector == 20:
        nr_str = "W"
    elif piece_selector == 10:
        nr_str = "H"
    piece_string = "  " + nr_str
    if piece_selector > 9:
        piece_string += " "
    else:
        piece_string += "  "
    return piece_string

def get_next_name():
    file_names = glob.glob("Levels/*")
    if len(file_names) == 0:
        return "level0.pickle"
    file_names.sort(key=lambda item:(len(item),item))
    last_name = file_names[len(file_names)-1]
    last_file = os.path.basename(last_name)
    last_file = last_file.replace(".pickle","")
    numb = re.findall(r'\d+',last_file)
    int_numb = int(numb[0])
    new_name = last_file[0:len(last_file)-len(numb[0])] + str(int_numb+1) + ".pickle"
    return new_name

def generate_field():
    master.title("level: " + level_name)
    master.geometry("350x275")
    buttons = []
    for y in range(0, 5):
        rowButtons = []
        for x in range(0, 5):
            btn_text = tkinter.StringVar()
            btn_text.set(get_piece_string())
            button = tkinter.Button(master, textvariable=btn_text,
                                    command=lambda l_x=x, l_y=y, l_txt=btn_text: button_callback(l_x, l_y, l_txt))
            button.grid(row=y, column=x)
            rowButtons.append(0)
        buttons.append(rowButtons)
    return buttons

def generate_field_with_grid():
    global piece_selector
    master.title("level: " + level_name)
    master.geometry("350x275")
    for y in range(0, 5):
        for x in range(0, 5):
            btn_text = tkinter.StringVar()
            piece_selector = grid[y][x]
            btn_text.set(get_piece_string())
            button = tkinter.Button(master, textvariable=btn_text,
                                    command=lambda l_x=x, l_y=y, l_txt=btn_text: button_callback(l_x, l_y, l_txt))
            button.grid(row=y, column=x)

def button_callback(x, y, btn_text):
    global grid
    grid[y][x] = piece_selector
    btn_text.set(get_piece_string())


def generate_option_buttons():
    # standard piece, wizard, hat, empty
    wizard_button = tkinter.Button(master, text="wizard piece", command=lambda: wizard_piece_selector())
    wizard_button.grid(row=0, column=option_buttons_column)
    hat_button = tkinter.Button(master, text="hat piece", command=lambda: hat_piece_selector())
    hat_button.grid(row=1, column=option_buttons_column)
    standard_button = tkinter.Button(master, text="standard piece", command=lambda: standard_piece_selector())
    standard_button.grid(row=2, column=option_buttons_column)
    double_button = tkinter.Button(master, text="double stack", command=lambda: double_piece_selector())
    double_button.grid(row=3, column=option_buttons_column)
    empty_button = tkinter.Button(master, text="empty space", command=lambda: empty_piece_selector())
    empty_button.grid(row=4, column=option_buttons_column)

def generate_save_buttons():
    save_button = tkinter.Button(master,text="save",command=lambda : save_level())
    save_button.grid(row = 0, column=option_buttons_column+1)
    refresh_button = tkinter.Button(master,text="clear",command=lambda : refresh_level())
    refresh_button.grid(row = 1, column=option_buttons_column+1)
    load_button = tkinter.Button(master,text="load",command=lambda : load_level())
    new_button = tkinter.Button(master,text="new",command=lambda : new_level())
    new_button.grid(row=2,column=option_buttons_column+1)
    load_button.grid(row=3,column=option_buttons_column+1)
    delete_button = tkinter.Button(master,text="delete",command=lambda : delete_level())
    delete_button.grid(row=4,column=option_buttons_column+1)


def save_level():
    global level_name
    with open(os.path.join("Levels",level_name),"wb") as f:
        pickle.dump(grid,f)
    new_level()
def new_level():
    global level_name
    level_name = get_next_name()
    refresh_level()

def refresh_level():
    global piece_selector
    piece_selector = 0
    build_gui()
def load_level():
    global level_name, grid,piece_selector
    load_name = filedialog.askopenfilename(initialdir=os.path.join("Levels"))
    if load_name == "":
        level_name = get_next_name()
        refresh_level()
    level_name = os.path.basename(load_name)
    with open(os.path.join("Levels",level_name),"rb") as f:
        grid = pickle.load(f)
    piece_selector = 0
    build_gui_no_new_grid()
def delete_level():
    os.remove(os.path.join("Levels",level_name))
    new_level()
def wizard_piece_selector():
    global piece_selector
    piece_selector = 20


def hat_piece_selector():
    global piece_selector
    piece_selector = 10


def empty_piece_selector():
    global piece_selector
    piece_selector = 0


def standard_piece_selector():
    global piece_selector
    piece_selector = 1


def double_piece_selector():
    global piece_selector
    piece_selector = 2

def build_gui_no_new_grid():
    #does the same as build_gui, except this time the grid isn't loaded again
    generate_field_with_grid()
    generate_option_buttons()
    generate_save_buttons()
    master.mainloop()

def build_gui():
    global grid
    grid = generate_field()
    generate_option_buttons()
    generate_save_buttons()
    master.mainloop()

def main():
    global level_name
    level_name = get_next_name()
    build_gui()



# main
# pieces: standard piece -> 1, wizard -> 20, hat -> 10, empty -> 0, double_stack -> 2

main()
