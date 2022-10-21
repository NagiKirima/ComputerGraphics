from tkinter import *

# constant
WINDOW_H = 1000
WINDOW_W = 1000
BUTTON_FONT = "Arial 15"
LABEL_FONT = "Arial 12"
CANVAS_TEXT_FONT = "Arial 10"
CANVAS_BG_COLOR = "#a6a6a6"
CANVAS_ADD_CURSOR = "pencil"
CANVAS_EDIT_CURSOR = "fleur"
CANVAS_SCROLL_CURSOR = "fleur"

# main window initialization
WINDOW = Tk()
WINDOW.geometry("{}x{}+0+0".format(WINDOW_W, WINDOW_H))
WINDOW.title("Gui")
WINDOW.resizable(0, 0)

# canvas initialization
CANVAS = Canvas(WINDOW, bg=CANVAS_BG_COLOR, cursor=CANVAS_ADD_CURSOR, scrollregion=(0, 0, 10000, 10000))

# scrollbars for canvas
hbar = Scrollbar(CANVAS, orient=HORIZONTAL, cursor=CANVAS_SCROLL_CURSOR)
hbar.pack(side=BOTTOM, fill=X)
hbar.config(command=CANVAS.xview)
vbar = Scrollbar(CANVAS, orient=VERTICAL, cursor=CANVAS_SCROLL_CURSOR)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=CANVAS.yview)
CANVAS.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
CANVAS.pack(side=LEFT, expand=True, fill=BOTH)

# slider initialization
WIDTH_SCALE = Scale(WINDOW, orient=HORIZONTAL, from_=1, to=10, resolution=1)

# init labels
STATUS_BAR = Label(text="", font=LABEL_FONT, anchor=W)
WIDTH_LABEL = Label(text="Ширина", font=LABEL_FONT, anchor=W)
