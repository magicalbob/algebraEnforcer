#!/usr/bin/env python3
""" Module to work out maths questions to ask """

import random
from math import sqrt

class Algebra:
    """ Class to work out maths questions to ask """
    def __init__(self):
        # simultaneous equation coefficients
        self.var_a = 0
        self.var_b = 0
        self.var_c = 0
        self.var_d = 0
        self.var_e = 0
        self.var_f = 0
        self.var_g = 0
        self.var_h = 0
        self.var_x = 0
        self.var_y = 0
        # expand & simplify coefficients and question
        self.var_x_squared = 0
        self.var_x_y = 0
        self.var_y_squared = 0
        self.exp_question = ''
        # question type
        # 0 = none
        # 1 = simultaneous equation
        # 2 = expand & simplify
        self.q_type = 0
        self.side = [0, 0, 0]
        # display questions
        self.disp1 = ''
        self.disp2 = ''
        self.perm = ''
        self.heron = ''

    def make_question(self):
        """ Function to work out maths questions to ask """
        self.q_type = random.randint(1, 3)
        if self.q_type == 1:
            self.make_quest_simultaneous()
        elif self.q_type == 2:
            self.make_quest_expand()
        elif self.q_type == 3:
            self.make_quest_heron()
        else:
            print("Eeeek! Question type invalid")

    def make_quest_simultaneous(self):
        haveanothergo = True
        while haveanothergo:
            haveanothergo = False
            self.var_a = random.randint(1, 10) * self.rand_sign()
            self.var_b = random.randint(1, 10) * self.rand_sign()
            self.var_c = random.randint(0, 10) * self.rand_sign()
            self.var_d = random.randint(0, 10) * self.rand_sign()
            self.var_e = random.randint(1, 10) * self.rand_sign()
            self.var_f = random.randint(1, 10) * self.rand_sign()
            self.var_g = random.randint(0, 10) * self.rand_sign()
            self.var_h = random.randint(0, 10) * self.rand_sign()
            self.disp1 = self.display_question(self.var_a,
                                               self.var_b,
                                               self.var_c,
                                               self.var_d)
            self.disp2 = self.display_question(self.var_e,
                                               self.var_f,
                                               self.var_g,
                                               self.var_h)
            try:
                self.var_y = ((self.var_e * self.var_c) -
                              (self.var_e * self.var_d) -
                              (self.var_a * self.var_g) +
                              (self.var_a * self.var_h)) / \
                             ((self.var_e * self.var_b) -
                              (self.var_a * self.var_f))
            except:
                haveanothergo = True

            try:
                self.var_x = ((self.var_b *
                               ((self.var_e * self.var_c) -
                                (self.var_e * self.var_d) -
                                (self.var_a * self.var_g) +
                                (self.var_a * self.var_h))) / \
                              ((self.var_e * self.var_b) -
                               (self.var_a * self.var_f)) -
                              self.var_c + self.var_d) / self.var_a
            except:
                haveanothergo = True

            if (self.var_a * self.var_x) + self.var_c == (self.var_b * self.var_y) + self.var_d:
                pass
            else:
                haveanothergo = True
            if (self.var_e * self.var_x) + self.var_g == (self.var_f * self.var_y) + self.var_h:
                pass
            else:
                haveanothergo = True

        print("Answer is X = %s, Y = %s" % (self.var_x, self.var_y))

    def display_question(self, var_a, var_b, var_c, var_d):
        if var_a == 1:
            disp_a = "x"
        else:
            disp_a = "%dx" % (var_a)

        if var_c < 0:
            disp_c = " - %d" % (-1 * var_c)
        elif var_c > 0:
            disp_c = " + %d" % (var_c)
        else:
            disp_c = ""

        if var_b == 1:
            disp_b = "y"
        else:
            disp_b = "%dy" % (var_b)

        if var_d < 0:
            disp_d = " - %d" % (-1 * var_d)
        elif var_d > 0:
            disp_d = " + %d" % (var_d)
        else:
            disp_d = ""

        return "%s%s = %s%s" % (disp_a, disp_c, disp_b, disp_d)

    def rand_sign(self):
        r_sign = random.randint(0,1)
        if r_sign == 0:
            return -1
        return 1

    def make_quest_heron(self):
        get_sides=True
        while get_sides:
            var_a = random.randint(1, 10)
            var_b = random.randint(1, 10)
            var_c = random.randint(1, 10)
            if ((var_a + var_b > var_c) and
                (var_a + var_c > var_b) and
                (var_c + var_b > var_a)):
                get_sides = False
        self.side[0] = var_a
        self.side[1] = var_b
        self.side[2] = var_c
        self.perm = float(self.side[0] + self.side[1] + self.side[2])/2
        self.heron = "%.4f" % (sqrt(self.perm *
                               (self.perm - self.side[0]) *
                               (self.perm - self.side[1]) *
                               (self.perm - self.side[2])))
        print("Answer is %s" % (self.heron))

    def make_quest_expand(self):
        coef1 = 0
        coef2 = 0
        coef3 = 0
        coef4 = 0

        while coef1 == 0:
            coef1 = random.randint(1,10) * self.rand_sign()
        while coef2 == 0:
            coef2 = random.randint(1,10) * self.rand_sign()
        while coef3 == 0:
            coef3 = random.randint(1,10) * self.rand_sign()
        while coef4 == 0:
            coef4 = random.randint(1,10) * self.rand_sign()

        self.var_x_squared = coef1 * coef3
        self.var_x_y = (coef1 * coef4) + (coef2 * coef3)
        self.var_y_squared = coef2 * coef4
        self.exp_question = "(%sx %s %sy)(%sx %s %sy)" % (
                            coef1,
                            ["-","+"][coef2 > 0],
                            abs(coef2),
                            coef3,
                            ["-","+"][coef4 > 0],
                            abs(coef4))

        print("Answer is: %s, %s & %s" % (self.var_x_squared,
                                          self.var_x_y,
                                          self.var_y_squared))


if __name__ == '__main__':
    X_ALG=Algebra()
    X_ALG.make_question()
    if X_ALG.q_type == 1:
        print ("Simultaneous Equation: %s, %s, %s, %s" % (
              X_ALG.disp1, X_ALG.disp2,  X_ALG.x,  X_ALG.y
               ))
    elif X_ALG.q_type == 2:
        print("Expand And Simplify")
        print(X_ALG.x_squared)
        print(X_ALG.x_y)
        print(X_ALG.y_squared)
        print(X_ALG.exp_question)
    elif X_ALG.q_type == 3:
        print("Heron's Formula")
        print("Side 1: %d" % (X_ALG.side[0]))
        print("Side 2: %d" % (X_ALG.side[1]))
        print("Side 3: %d" % (X_ALG.side[2]))
        print("p = %.2f" % (X_ALG.perm))
        print("Area = %s" % (X_ALG.heron))
    else:
        print("WTF!")
