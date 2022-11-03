from tkinter import *
import turtle
import tkinter.messagebox


class DrawShape:
    window = None
    canvas = None
    t = None
    screen = None

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(master=self.window, width=800, height=800)
        self.canvas.pack(side=LEFT)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.t = turtle.RawTurtle(self.canvas)
        self.t.hideturtle()
        self.t.speed(0)
        self.t.penup()

    def drawCircle(self, midpoints, radius, color):
        self.t.fillcolor(color)
        self.t.setx(midpoints[0])
        self.t.sety(midpoints[1])
        self.t.pendown()
        self.t.speed(0)
        self.t.begin_fill()
        self.t.circle(radius)
        self.t.end_fill()
        self.screen.mainloop()

    def drawRec(self, leftopx, toplefty, length, width, color):
        self.t.fillcolor(color)
        self.t.setx(leftopx)
        self.t.sety(toplefty)
        self.t.pendown()
        self.t.begin_fill()
        self.t.forward(length)
        self.t.left(90)
        self.t.forward(width)
        self.t.left(90)
        self.t.forward(length)
        self.t.left(90)
        self.t.forward(width)
        self.t.left(90)
        self.t.end_fill()
        self.screen.mainloop()
