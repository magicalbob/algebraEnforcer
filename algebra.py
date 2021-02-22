#!/usr/bin/env python3
""" Module to work out maths questions to ask """

import random
from math import sqrt
#import yaml

class Algebra:
    """ Class to work out maths questions to ask """
    def __init__(self):
        # simultaneous equation coefficients
        self.variable = { 'a': 0,
                          'b': 0,
                          'c': 0,
                          'd': 0,
                          'e': 0,
                          'f': 0,
                          'g': 0,
                          'h': 0,
                          'x': 0,
                          'y': 0,
                          'x_squared': 0,
                          'x_y': 0,
                          'y_square': 0,
                          'exp_question': 0,
                          'q_type': 0,
                          'side': [0, 0, 0],
                          'disp1': '',
                          'disp2': '',
                          'perm': '',
                          'heron': '' }

    def make_question(self):
        """ Function to work out maths questions to ask """
        self.variable['q_type'] = random.randint(1, 3)
        if self.variable['q_type'] == 1:
            self.make_quest_simultaneous()
        elif self.variable['q_type'] == 2:
            self.make_quest_expand()
        elif self.variable['q_type'] == 3:
            self.make_quest_heron()
        else:
            print("Eeeek! Question type invalid")

    def make_quest_simultaneous(self):
        """ Function to work out simultaneous equation questions to ask """
        haveanothergo = True
        while haveanothergo:
            haveanothergo = False
            self.variable['a'] = random.randint(1, 10) * self.rand_sign()
            self.variable['b'] = random.randint(1, 10) * self.rand_sign()
            self.variable['c'] = random.randint(0, 10) * self.rand_sign()
            self.variable['d'] = random.randint(0, 10) * self.rand_sign()
            self.variable['e'] = random.randint(1, 10) * self.rand_sign()
            self.variable['f'] = random.randint(1, 10) * self.rand_sign()
            self.variable['g'] = random.randint(0, 10) * self.rand_sign()
            self.variable['h'] = random.randint(0, 10) * self.rand_sign()
            self.variable['disp1'] = self.display_question(self.variable['a'],
                                                           self.variable['b'],
                                                           self.variable['c'],
                                                           self.variable['d'])
            self.variable['disp2'] = self.display_question(self.variable['e'],
                                                           self.variable['f'],
                                                           self.variable['g'],
                                                           self.variable['h'])
            try:
                self.variable['y'] = (
                              (self.variable['e'] * self.variable['c']) -
                              (self.variable['e'] * self.variable['d']) -
                              (self.variable['a'] * self.variable['g']) +
                              (self.variable['a'] * self.variable['h'])) / \
                             ((self.variable['e'] * self.variable['b']) -
                              (self.variable['a'] * self.variable['f']))
            except ZeroDivisionError:
                haveanothergo = True

            try:
                self.variable['x'] = (
                              (self.variable['b'] *
                               ((self.variable['e'] * self.variable['c']) -
                                (self.variable['e'] * self.variable['d']) -
                                (self.variable['a'] * self.variable['g']) +
                                (self.variable['a'] * self.variable['h']))) / \
                              ((self.variable['e'] * self.variable['b']) -
                               (self.variable['a'] * self.variable['f'])) -
                              self.variable['c'] + self.variable['d']) / \
                              self.variable['a']
            except ZeroDivisionError:
                haveanothergo = True

            if (self.variable['a'] * self.variable['x']) + \
               self.variable['c'] == (self.variable['b'] * self.variable['y']) + self.variable['d']:
                pass
            else:
                haveanothergo = True
            if (self.variable['e'] * self.variable['x']) + \
               self.variable['g'] == (self.variable['f'] * self.variable['y']) + self.variable['h']:
                pass
            else:
                haveanothergo = True

        print("Answer is X = %s, Y = %s" % (self.variable['x'], self.variable['y']))

    def display_question(self, var_a, var_b, var_c, var_d):
        """ Work out questions to ask """
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

        print(self)
        return "%s%s = %s%s" % (disp_a, disp_c, disp_b, disp_d)

    def rand_sign(self):
        """ Function to supply random sign """
        r_sign = random.randint(0,1)
        if r_sign == 0:
            return -1
        print(self)
        return 1

    def make_quest_heron(self):
        """ Function to work out heron questions to ask """
        get_sides=True
        while get_sides:
            self.variable['a'] = random.randint(1, 10)
            self.variable['b'] = random.randint(1, 10)
            self.variable['c'] = random.randint(1, 10)
            if ((self.variable['a'] + self.variable['b'] > self.variable['c']) and
                (self.variable['a'] + self.variable['c'] > self.variable['b']) and
                (self.variable['c'] + self.variable['b'] > self.variable['a'])):
                get_sides = False
        self.variable['side'][0] = self.variable['a']
        self.variable['side'][1] = self.variable['b']
        self.variable['side'][2] = self.variable['c']
        self.variable['perm'] = float(self.variable['side'][0] +
                                      self.variable['side'][1] +
                                      self.variable['side'][2])/2
        self.variable['heron'] = "%.4f" % (sqrt(self.variable['perm'] *
                               (self.variable['perm'] - self.variable['side'][0]) *
                               (self.variable['perm'] - self.variable['side'][1]) *
                               (self.variable['perm'] - self.variable['side'][2])))
        print("Answer is %s" % (self.variable['heron']))

    def make_quest_expand(self):
        """ Function to work out expansion questions to ask """
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

        self.variable['x_squared'] = coef1 * coef3
        self.variable['x_y'] = (coef1 * coef4) + (coef2 * coef3)
        self.variable['y_squared'] = coef2 * coef4
        self.variable['exp_question'] = "(%sx %s %sy)(%sx %s %sy)" % (
                            coef1,
                            ["-","+"][coef2 > 0],
                            abs(coef2),
                            coef3,
                            ["-","+"][coef4 > 0],
                            abs(coef4))

        print("Answer is: %s, %s & %s" % (self.variable['x_squared'],
                                          self.variable['x_y'],
                                          self.variable['y_squared']))


if __name__ == '__main__':
    X_ALG=Algebra()
    X_ALG.make_question()
    if X_ALG.variable['q_type'] == 1:
        print ("Simultaneous Equation: %s, %s, %s, %s" % (
              X_ALG.variable['disp1'],
              X_ALG.variable['disp2'],
              X_ALG.variable['x'],
              X_ALG.variable['y']
               ))
    elif X_ALG.variable['q_type'] == 2:
        print("Expand And Simplify")
        print(X_ALG.variable['x_squared'])
        print(X_ALG.variable['x_y'])
        print(X_ALG.variable['y_squared'])
        print(X_ALG.variable['exp_question'])
    elif X_ALG.variable['q_type'] == 3:
        print("Heron's Formula")
        print("Side 1: %d" % (X_ALG.variable['side'][0]))
        print("Side 2: %d" % (X_ALG.variable['side'][1]))
        print("Side 3: %d" % (X_ALG.variable['side'][2]))
        print("p = %.2f" % (X_ALG.variable['perm']))
        print("Area = %s" % (X_ALG.variable['heron']))
    else:
        print("WTF!")
