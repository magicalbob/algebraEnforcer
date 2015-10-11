#!/usr/bin/python

import random

class Algebra:
  def __init__(self):
    self.a = 0
    self.b = 0
    self.c = 0
    self.d = 0
    self.e = 0
    self.f = 0
    self.g = 0
    self.h = 0
    self.x = 0
    self.y = 0

  def makeQuestion(self):
    haveanothergo = True
    while haveanothergo:
      haveanothergo = False
      self.a = random.randint(1,10) * self.randSign()   
      self.b = random.randint(1,10) * self.randSign()   
      self.c = random.randint(0,10) * self.randSign()   
      self.d = random.randint(0,10) * self.randSign()   
      self.e = random.randint(1,10) * self.randSign()   
      self.f = random.randint(1,10) * self.randSign()   
      self.g = random.randint(0,10) * self.randSign()   
      self.h = random.randint(0,10) * self.randSign()   
      self.disp1 = self.displayQuestion(self.a,self.b,self.c,self.d)
      self.disp2 = self.displayQuestion(self.e,self.f,self.g,self.h)
      try:
        self.y = ((self.e * self.c) - (self.e * self.d) - (self.a * self.g) + (self.a * self.h)) / ((self.e * self.b) - (self.a * self.f))
      except:
        haveanothergo = True
  
      try:
        self.x = ((self.b * ((self.e * self.c) - (self.e * self.d) - (self.a * self.g) + (self.a * self.h))) / ((self.e * self.b) - (self.a * self.f)) - self.c + self.d) / self.a
      except:
        haveanothergo = True
  
      if (self.a * self.x) + self.c == (self.b * self.y) + self.d:
        pass
      else:
        haveanothergo = True
      if (self.e * self.x) + self.g == (self.f * self.y) + self.h:
        pass
      else:
        haveanothergo = True

  def displayQuestion(self, a, b, c, d):
    if a == 1:
      dispA = "x"
    else:
      dispA = "%dx" % (a)

    if c < 0:
      dispC = " - %d" % (-1 * c)
    elif c > 0:
      dispC = " + %d" % (c)
    else:
      dispC = ""

    if b == 1:
      dispB = "y"
    else:
      dispB = "%dy" % (b)

    if d < 0:
      dispD = " - %d" % (-1 * d)
    elif d > 0:
      dispD = " + %d" % (d)
    else:
      dispD = ""

    return "%s%s = %s%s" % (dispA, dispC, dispB, dispD)

  def randSign(self):
    rSign = random.randint(0,1)
    if rSign == 0:
      return -1
    return 1

if __name__ == '__main__':
  xAlg=Algebra()
  xAlg.makeQuestion()
  print xAlg.disp1
  print xAlg.disp2
  print xAlg.x
  print xAlg.y
