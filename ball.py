#Luis Ramirez
#12/08/10
#ball.py
#pong.py library

from gv2 import *
from random import random, randrange
from time import sleep

class Vector:
  """Class for containing the motion of objects"""
  def __init__(self, x = 0, y = 0):
     self.x = x
     self.y = y

  def setX(self, num): self.x = num

  def setY(self, num): self.y = num

  def __neg__(self):
    """changes the x value, so that the vector now points in the opposite direction"""
    self.x = -self.x 
    return self

  def __pos__(self):
    self.y = -self.y
    return self

  def __invert__(self): 
    self.x = -self.x
    self.y = -self.y
    return self

  def __iadd__(self, other):
    """adds either a single number or a tuple to the vector"""
    if type(other) == type(1) or type(other) == type(1.0):
      if self.x >= 0: self.x += other
      else: self.x -= other
      if self.y >= 0: self.y += other
      else: self.y -= other
    elif type(other) == type((1,2)):
      self.x += other[0]
      self.y += other[1]
    return self

  def reset(self, x, y):
    """resets the vector, randomizing it"""
    return Vector(randrange(x[0], x[1]), randrange(y[0], y[1]))

class GameObject:
  """class inherited by all objects in the game"""
  def __contains__(self, item):
    """determines if one object is within another, graphically"""
    if (item.BBox.p1.x > self.BBox.p1.x and item.BBox.p1.x < self.BBox.p2.x) and (item.BBox.p1.y > self.BBox.p1.y and item.BBox.p1.y < self.BBox.p2.y): return True #checks if the first point is in the object
    elif (item.BBox.p2.x > self.BBox.p1.x and item.BBox.p1.x < self.BBox.p2.x) and (item.BBox.p2.y > self.BBox.p1.y and item.BBox.p1.y < self.BBox.p2.y): return True #checks if the second point is in the object
    else: return False

class GameBox(GameObject):
  """The 'box' that the game is played in, a way to check if the ball has left the window"""
  def __init__(self, window):
    self.p1 = Point(0,0)
    self.height = window.getHeight()
    self.width = window.getWidth()
    self.p2 = Point(self.width, self.height)
    self.BBox = Rectangle(self.p1, self.p2)

  def checkWall(self, other):
    """returns which if any walls an object is beyond"""
    if other.BBox.p1.x < self.p1.x: return 'Left'
    elif  other.BBox.p1.y < self.p1.y: return 'Top'
    elif other.BBox.p2.x > self.p2.x: return 'Right'
    elif  other.BBox.p2.y > self.p2.y: return 'Bottom'
    else: return False

class Ball(GameObject):
  """class describing the ball in the game"""
  def __init__(self, window, center, radius, color='red'):
    """     
    window => GraphWin object
    center => Point object
    radius => int
    color => string"""
    self.window = window
    self.radius = radius
    self.ball = Circle(center, radius)
    self.color = color
    self.ball.setFill(color)
    self.start = center.clone()
    self.center = center
    self.BBox = self._BBox()
    self.hits = 0
   
  def _BBox(self):
    """creates a bounding box for the circle, used to check for collisions"""
    p1 = self.center.clone()
    p2 = self.center.clone()
    p1.move(-self.radius -1, -self.radius -1)
    p2.move(self.radius +1, self.radius +1)
    return Rectangle(p1, p2)

  def addHit(self): self.hits += 1

  def move(self, vector):
    """moves the ball, requires a Vector object"""
    self.ball.move(vector.x, vector.y)
    self.BBox.move(vector.x, vector.y)
    self.center = self.ball.getCenter()

  def reset(self):
    """returns a new ball (with the same features) at the spawning point of the current ball"""
    self.undraw()
    new = Ball(self.window, self.start, self.radius, self.color)
    new.draw()
    return new
  def draw(self): self.ball.draw(self.window)
  def undraw(self): self.ball.undraw()

class  Paddle(GameObject):
  """class that controls the paddle objects for the pong game
  """
  def __init__(self, window, length, player = 1, diff = randrange(1,10)):
    """
    window => GraphWin object
    length => int, paddle length
    player => bool, whether the paddle is controlled by a human or a computer
    diff => int 1-9, the difficulty setting, for computer paddle"""
    self.window = window
    self.width = window.getWidth() / 20
    self.length = length
    self.player = player
    if self.player:
      self.P1 = Point(self.width * 19, ((self.window.getHeight() - self.length) / 2))
    else:
      self.P1 = Point(0, ((self.window.getHeight() - self.length) / 2))
    self.P2 = self.P1.clone()
    self.P2.move(self.width, self.length)
    self.center = self.P1.clone()
    self.center.move(self.width/2, self.length/2)
    self.paddle = Rectangle(self.P1, self.P2)
    self.paddle.setFill('black')
    self.BBox = self.paddle
    if not player: self.diff = diff

  def move(self, num):
    """moves the paddle num pixels down""" 
    self.paddle.move(0, num); self.center.move(0, num)

  def draw(self):
    """draws the paddle""" 
    self.paddle.draw(self.window)

  def undraw(self):
    """undrawsd the paddle""" 
    self.paddle.undraw()

  def reset(self):
    """returns a new paddle object with the same attributes and at the same starting point as the first"""
    self.undraw()
    new = Paddle(self.window, self.length, self.player, self.diff)
    new.draw()
    return new

  def findBall(self, ball):
    """attempts aligns the center of the paddle with the center of the ball, but prevents the paddle from moving faster than a limit determined by the difficulty setting"""
    my = ball.center.y - self.center.y
    if my >= self.diff * 2 and my >= 0:
      self.move(self.diff * 2)
    elif my <= -(self.diff * 2) and my < 0:
      self.move(-(self.diff * 2))
    else: 
      self.move(my)
