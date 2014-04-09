#Luis Ramirez
#12/08/10
#pong.py
#a simple pong game

from gv2 import *
from random import random, randrange
from time import sleep
import ball

def game():

  width = 1600
  height = 1000
  window = GraphWin('Pong', width, height)
  gamebox = ball.GameBox(window)
  center = Point(width/2, height/2)

  paddle1 = ball.Paddle(window, 150)

  message = 'Please choose a difficulty (1-9)'
  messageDisplay = Text(center, message)
  messageDisplay.setSize(36)
  messageDisplay.draw(window)

  diff = None
  while True:#loop that waits for the user to input a number
    key = window.checkKey()
    if key: #only happens if the user presses a key
      try: diff = int(key); break
      except ValueError: continue #if the key is not a number
    sleep(1)                      #the loop starts over
  messageDisplay.undraw()#when completed, erases the message
  if diff == 0: diff = 1

  paddle1.draw()
  paddle2 = ball.Paddle(window, 150, None, diff)
  paddle2.draw()

  ball1 = ball.Ball(window, center, 30)
  ball1.draw()

  vec = ball.Vector(randrange(-5,5),randrange(-5,5))

  player = 0 #player score
  comp = 0 #computer score

  score = str(comp) + (' ' * 30) + str(player)
  scoreDisplay = Text(Point(width/2, 50), score)
  scoreDisplay.setSize(30)
  scoreDisplay.draw(window)
  """shows the score"""

  options = 'F1: Pause' + (' ' * 10) + 'F4: Quit'
  optionsDisplay = Text(Point(width/2, height - 50), options)
  optionsDisplay.draw(window)
  """shows the options for the user"""

  messageDisplay.setText('Please click to start')
  messageDisplay.draw(window)
  window.getMouse()
  messageDisplay.undraw()

  messageDisplay.setText('Please click to continue')
  tic1 = 0 #changed by whether the ball is touching a paddle
  tic2 = 0 #incremented each time through the loop

  while True:

    tic2 += 1

    key = window.checkKey()
    if key == 'Up': paddle1.move(-20)#moves paddle up
    elif key == 'Down': paddle1.move(20)#moves paddle down
    elif key == 'F1': #pauses the game
      messageDisplay.draw(window)
      window.getMouse()
      messageDisplay.undraw()
    elif key == 'F4': break #quits the game

    if (ball1 in paddle1 or ball1 in paddle2) and not tic1:
      vec = -vec #changes the x of the vector to its opposite
      ball1.addHit()
      tic1 = 1
      if ball1.hits % 5 == 0: #increases the vector by one
        vec += 1
    elif (ball1 in paddle1 or ball1 in paddle2) and tic1: pass 
#if the ball has not stopped touching the paddle yet, ignore it
    else: tic1 = 0

    wall = gamebox.checkWall(ball1)
    if wall:
        if wall == 'Left':

          ball1 = ball1.reset() #resets the playing field
          paddle2 = paddle2.reset()
          vec = vec.reset((-5,5), (-5,5))

          player += 1 #increments the players score
          score = str(comp) + (' ' * 30) + str(player)
          scoreDisplay.setText(score) #changes the score display

          messageDisplay.draw(window) #pauses the game until
          window.getMouse() #the user clicks the mouse
          messageDisplay.undraw()

        elif wall == 'Top': vec = +vec #reverses the y of the vector
        elif wall == 'Bottom': vec = +vec
        elif wall == 'Right': 
          ball1 = ball1.reset()
          paddle2 = paddle2.reset()
          vec = vec.reset((-5,5), (-5,5))
          comp += 1
          score = str(comp) + (' ' * 30) + str(player)
          scoreDisplay.setText(score)
          messageDisplay.draw(window)
          window.getMouse()
          messageDisplay.undraw()

    ball1.move(vec)
    if vec.x < 0:
      paddle2.findBall(ball1)
    if vec.x == 0: vec.setX(1)

    if tic2 % 20 == 0 and ball1 not in gamebox:#If the ball runs away, reset the field 
      ball1 = ball1.reset()
      paddle2 = paddle2.reset()
      vec = vec.reset()
      window.getMouse()

    if player >= 5: #if someone wins, alerts the player and ends the game
      endDisplay = Text(center, 'You Win')
      endDisplay.setSize(36)
      endDisplay.draw(window)
      window.getMouse()
      break
    elif comp >= 5:
      endDisplay = Text(center, 'Computer Wins')
      endDisplay.setSize(36)
      endDisplay.draw(window)
      window.getMouse()
      break


    sleep(0.01)

game()
