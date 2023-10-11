import turtle
from tkinter import *
import tkinter
import random

def game(board, bubbles_color, ball_color, paddle_color):
    wn = turtle.Screen()
    wn.title("Bubbles")
    wn.bgcolor("black")
    wn.setup(width=800, height=600)
    wn.tracer(0) # dont update window by itself, we update it manualy, helps game to be faster


    score = 0
    lifes = 3
    bounce = 0


    paddle_a = turtle.Turtle()
    paddle_a.speed(0) # speed of animation
    paddle_a.shape("square")
    paddle_a.color(paddle_color)
    paddle_a.shapesize(stretch_wid=1, stretch_len=5)
    paddle_a.penup() # tell turtle not to draw free lines, (when he moves)
    paddle_a.goto(0, -270)


    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("square")
    ball.color(ball_color)
    ball.penup()
    ball.goto(0, -260)  # -250 to na desce
    ball.dx = 0
    ball.dy = 0


    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write("Score 0", align='center', font=("Courier", 24, "normal"))

    bubbles = {}
    bubbles_still = []
    print(board)
    for j in range(0,6):
        for i in range(0,15):
            if board[j][i]:
                bubble = turtle.Turtle()
                bubble.speed(0)
                bubble.shape("square")
                bubble.color(bubbles_color)
                bubble.shapesize(stretch_wid=2, stretch_len=2)
                bubble.penup()
                bubble.goto((i+1)*50 - 400, 270 - (j+1)*50)
                bubbles_still.append('bubble' + str(j) + '.'+ str(i))
                bubbles['bubble' + str(j) + '.'+ str(i)] = bubble


    # throw ball
    def start_ball():
        if ball.dx == 0 and ball.dx == 0:
            m = random.randint(5, 15)
            n = random.randint(7, 12)/10
            ball.dy = n - (n/(m-1))
            if m > 10:
                ball.dx = n/(m-2) * (-1)
            else:
                ball.dx = n/(m+1)


    def paddle_a_right():
        x = paddle_a.xcor()
        x += 20
        paddle_a.setx(x)

    def paddle_a_left():
        x = paddle_a.xcor()
        x -= 20
        paddle_a.setx(x)


    # listen for clicking keyboard
    wn.listen()
    # when user pres 'w' use given function
    wn.onkeypress(paddle_a_left, "Left")
    wn.onkeypress(paddle_a_right, "Right")
    wn.onkeypress(start_ball, "space")


    while True:
        wn.update()

        # ball moving
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # borders for ball
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
        if ball.ycor() < -290:
            ball.goto(0, -260)
            ball.dx = 0
            ball.dy = 0
            lifes -= 1
        if ball.xcor() > 390:
            ball.dx *= -1
        if ball.xcor() < -390:
            ball.dx *= -1
            
        pen.clear()
        pen.write(f"Score: {score}", align='center', font=("Courier", 24, "normal"))

        # bounce ball of paddle
        if (ball.ycor() < -270 and ball.ycor() > -280) and (ball.xcor() < paddle_a.xcor()+40 and ball.xcor() > paddle_a.xcor()-40):
            ball.sety(-270)
            ball.dy *= -1
            if ball.dx > 0 and (ball.xcor() < paddle_a.xcor()+40 and ball.xcor() > paddle_a.xcor()):
                ball.dx *= -1
            elif ball.dx < 0 and (ball.xcor() < paddle_a.xcor() and ball.xcor() > paddle_a.xcor()-40):
                ball.dx *= -1


        if len(bubbles_still) > 0:
            for i in bubbles_still:
                if (ball.ycor() > bubbles[i].ycor()-25 and ball.ycor() < bubbles[i].ycor()+25) and (ball.xcor() < bubbles[i].xcor()+25 and ball.xcor() > bubbles[i].xcor()-25):
                    bubbles_still.remove(i)
                    bubbles[i].reset()
                    score += 10
                    ball.dy *= -1

        # lose
        if lifes == 0:
            wn.bye()

def menu():
    root = Tk()
    root.title("Bubble shooter") # window title
    root.geometry('750x350') # windows size

    header = Label(root, text='Bubble shooter by Maciek', font='45', height=1)
    header.pack()

    left_frame = Frame(root)
    left_frame.pack(side=LEFT)

    mid_frame1 = Frame(left_frame)
    mid_frame1.pack()

    mid_frame2 = Frame(left_frame)
    mid_frame2.pack()

    mid_frame3 = Frame(left_frame)
    mid_frame3.pack()

    down_frame = Frame(left_frame)
    down_frame.pack()

    right_frame = Frame(root)
    right_frame.pack(side=RIGHT)

    upper_frame = Frame(right_frame)
    upper_frame.pack()
    
    downer_frame = Frame(right_frame)
    downer_frame.pack()

    label_for_color_of_bubbles = Label(mid_frame1, text="Choose color of bubbles")
    label_for_color_of_bubbles.pack(side=LEFT, pady=10, padx=10)

    COLOR_OF_BUBBLES = ["red", "blue", "white", "green", "brown"]
    color_of_bubbles_var = StringVar(root)
    color_of_bubbles_var.set(COLOR_OF_BUBBLES[0])
    color_of_bubbles_menu = OptionMenu(mid_frame1, color_of_bubbles_var, *COLOR_OF_BUBBLES)
    color_of_bubbles_menu.pack(side=RIGHT, pady=10)

    label_for_color_of_ball = Label(mid_frame2, text="Choose color of ball")
    label_for_color_of_ball.pack(side=LEFT)

    COLOR_OF_BALL = ["red", "blue", "white", "green", "brown"]
    color_of_ball_var = StringVar(root)
    color_of_ball_var.set(COLOR_OF_BALL[0])
    color_of_ball_menu = OptionMenu(mid_frame2, color_of_ball_var, *COLOR_OF_BALL)
    color_of_ball_menu.pack(side=RIGHT)

    label_for_color_of_paddle = Label(mid_frame3, text="Choose color of paddle")
    label_for_color_of_paddle.pack(side=LEFT, pady=10)

    COLOR_OF_PADDLE = ["red", "blue", "white", "green", "brown"]
    color_of_paddle_var = StringVar(root)
    color_of_paddle_var.set(COLOR_OF_PADDLE[0])
    color_of_paddle_menu = OptionMenu(mid_frame3, color_of_paddle_var, *COLOR_OF_PADDLE)
    color_of_paddle_menu.pack(side=RIGHT, pady=10)

    label_for_board_size = Label(upper_frame, text="Choose set of bubbles")
    label_for_board_size.pack()

    check_boxes = {}
    for row in range(0,6):
        for col in range(0,15):
            var = IntVar()
            ch = Checkbutton(downer_frame, text='', variable=var)
            ch.grid(row=row,column=col)
            check_boxes[str(row) + '.' + str(col)] = var

    bubbles = [[None for _ in range(0,15)] for _ in range(0,6)]
    def submit_func():
        for name in check_boxes.keys():
            i,j = name.split('.')
            bubbles[int(i)][int(j)] = check_boxes[name].get()
        game(bubbles, color_of_bubbles_var.get(), color_of_ball_var.get(), color_of_paddle_var.get())

    submit_button = Button(down_frame, text='Submit', command=submit_func)
    submit_button.pack(pady=10)

if __name__ == '__main__':
    menu()
    tkinter.mainloop()