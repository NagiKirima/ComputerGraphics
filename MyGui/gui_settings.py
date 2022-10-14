from tkinter import *

# constant
WINDOW_H = 1000
WINDOW_W = 1000
BUTTON_FONT = "Arial 15"
LABEL_FONT = "Arial 12"
CANVAS_TEXT_FONT = "Arial 10"
CANVAS_BG_COLOR = "#a6a6a6"

# main window initialization
WINDOW = Tk()
WINDOW.geometry("{}x{}+0+0".format(WINDOW_W, WINDOW_H))
WINDOW.title("Gui")
WINDOW.resizable(0, 0)

# canvas initialization
CANVAS = Canvas(WINDOW, bg=CANVAS_BG_COLOR)

# slider initialization
WIDTH_SCALE = Scale(WINDOW, orient=HORIZONTAL, from_=1, to=10, resolution=1)

# init labels
STATUS_BAR = Label(text="", font=LABEL_FONT, anchor=W)
WIDTH_LABEL = Label(text="Ширина", font=LABEL_FONT, anchor=W)
