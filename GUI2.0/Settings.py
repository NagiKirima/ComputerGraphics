from tkinter import *

# constant
WINDOW_H = 1000
WINDOW_W = 1920
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
MAXY = 10000
MAXX = 10000
MINX = -10000
MINY = -10000
CANVAS = Canvas(WINDOW, bg=CANVAS_BG_COLOR, cursor=CANVAS_ADD_CURSOR, scrollregion=(MINX, MINY, MAXX, MAXY))

# scrollbars for canvas
XBAR = Scrollbar(CANVAS, orient=HORIZONTAL, cursor=CANVAS_SCROLL_CURSOR)
XBAR.pack(side=BOTTOM, fill=X)
XBAR.config(command=CANVAS.xview)

YBAR = Scrollbar(CANVAS, orient=VERTICAL, cursor=CANVAS_SCROLL_CURSOR)
YBAR.pack(side=RIGHT, fill=Y)
YBAR.config(command=CANVAS.yview)

CANVAS.config(xscrollcommand=XBAR.set, yscrollcommand=YBAR.set)
CANVAS.pack(side=LEFT, expand=True, fill=BOTH)

# slider initialization
WIDTH_SCALE = Scale(WINDOW, orient=HORIZONTAL, from_=1, to=10, resolution=1)

# init labels
STATUS_BAR = Label(text="", font=LABEL_FONT, anchor=W)
WIDTH_LABEL = Label(text="Ширина", font=LABEL_FONT, anchor=W)
