#!/usr/bin/python

import random
from math import sqrt

class Algebra:
  def __init__(self):
    # simultaneous equation coefficients
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
    # expand & simplify coefficients and question
    self.x_squared = 0
    self.x_y = 0
    self.y_squared = 0
    self.expQuestion = ''
    # question type
    # 0 = none
    # 1 = simultaneous equation
    # 2 = expand & simplify
    self.q_type = 0
    self.side=[0,0,0]

  def makeQuestion(self):
    self.q_type = random.randint(1,3)
    self.q_type = 3
    if self.q_type == 1:
      self.makeQuestSimultaneous()
    elif self.q_type == 2:
      self.makeQuestExpand()
    elif self.q_type == 3:
      self.makeQuestHeron()
    else:
      print "Eeeek! Question type invalid"

  def makeQuestSimultaneous(self):
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

  def makeQuestHeron(self):
    getSides=True
    while (getSides):
      a = random.randint(1,10)
      b = random.randint(1,10)
      c = random.randint(1,10)
      if (a+b>c) and (a+c>b) and (c+b>a):
        getSides=False
    self.side[0] = a
    self.side[1] = b
    self.side[2] = c
    self.perm=float(self.side[0]+self.side[1]+self.side[2])/2
    self.heron="%.4f" % (sqrt(self.perm * (self.perm-self.side[0]) * (self.perm-self.side[1]) * (self.perm-self.side[2])))

  def makeQuestExpand(self):
    coef1 = 0
    coef2 = 0
    coef3 = 0
    coef4 = 0

    while coef1 == 0:
      coef1 = random.randint(1,10) * self.randSign()
    while coef2 == 0:
      coef2 = random.randint(1,10) * self.randSign()
    while coef3 == 0:
      coef3 = random.randint(1,10) * self.randSign()
    while coef4 == 0:
      coef4 = random.randint(1,10) * self.randSign()

    self.x_squared = coef1 * coef3
    self.x_y = (coef1 * coef4) + (coef2 * coef3)
    self.y_squared = coef2 * coef4
    self.expQuestion = "(%sx %s %sy)(%sx %s %sy)" % (
                        coef1,
                        ["-","+"][coef2 > 0],
                        abs(coef2),
                        coef3,
                        ["-","+"][coef4 > 0],
                        abs(coef4))


if __name__ == '__main__':
  xAlg=Algebra()
  xAlg.makeQuestion()
  if xAlg.q_type == 1:
    print "Simultaneous Equation:"
    print xAlg.disp1
    print xAlg.disp2
    print xAlg.x
    print xAlg.y
  elif xAlg.q_type == 2:
    print "Expand And Simplify"
    print xAlg.x_squared
    print xAlg.x_y
    print xAlg.y_squared
    print xAlg.expQuestion
  elif xAlg.q_type == 3:
    print "Heron's Formula"
    print "Side 1: %d" % (xAlg.side[0])
    print "Side 2: %d" % (xAlg.side[1])
    print "Side 3: %d" % (xAlg.side[2])
    print "p = %.2f" % (xAlg.perm)
    print "Area = %s" % (xAlg.heron)
  else:
    print "WTF!"
