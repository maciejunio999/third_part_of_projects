import turtle
import random

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
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=1, stretch_len=5)
paddle_a.penup() # tell turtle not to draw free lines, (when he moves)
paddle_a.goto(0, -270)


ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
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
board = [
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]
for j in range(0,6):
    for i in range(0,15):
        if board[j][i]:
            bubble = turtle.Turtle()
            bubble.speed(0)
            bubble.shape("square")
            bubble.color("blue")
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