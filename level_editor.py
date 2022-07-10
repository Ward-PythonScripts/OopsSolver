import tkinter

piece_selector = 0
grid = []
option_buttons_column = 6  # constant


def get_piece_string():
    global piece_selector
    piece_string = "  " + str(piece_selector)
    if piece_selector > 9:
        piece_string += " "
    else:
        piece_string += "  "
    return piece_string


def generate_field():
    master = tkinter.Tk()
    master.title("generate field")
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
    return master, buttons


def button_callback(x, y, btn_text):
    grid[y][x] = piece_selector
    btn_text.set(get_piece_string())


def generate_option_buttons(master):
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


def main():
    global grid
    master, buttons = generate_field()
    grid = buttons
    generate_option_buttons(master)
    master.mainloop()


# main
# pieces: standard piece -> 1, wizard -> 20, hat -> 30, empty -> 0, double_stack -> 2

main()
