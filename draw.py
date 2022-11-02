import turtle


class DrawShape:
    wn = None
    t = None

    def __init__(self):
        self.t = turtle.Turtle()
        self.wn = self.t.screen
        self.wn.bgcolor("white")
        self.wn.title("Draw shapes")

    def drawCircle(self, midpoints, radius, color):
        self.wn.clearscreen()
        self.t.hideturtle()
        self.t.fillcolor(color)
        self.t.penup()
        self.t.setx(midpoints[0])
        self.t.sety(midpoints[1])
        self.t.pendown()
        self.t.begin_fill()
        self.t.circle(radius)
        self.t.end_fill()
        turtle.exitonclick()

    def drawRec(self, leftopx, toplefty, length, width, color):
        self.wn.clearscreen()
        self.t.hideturtle()
        self.t.fillcolor(color)
        self.t.penup()
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
        turtle.exitonclick()
