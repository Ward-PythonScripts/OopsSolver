import tkinter


def generate_field():
    master = tkinter.Tk()
    master.title("generate field")
    master.geometry("350x275")
    buttons = []
    for y in range(0, 5):
        rowButtons = []
        for x in range(0, 5):
            button = tkinter.Button(master, text="        ", command=lambda x=x, y=y: button_callback(x,y))
            button.grid(row=y, column=x)
            rowButtons.append(0)
        buttons.append(rowButtons)
    return master


def button_callback(x, y):
    print("you just clicked button ", x, y)


# main
master = generate_field()
master.mainloop()
