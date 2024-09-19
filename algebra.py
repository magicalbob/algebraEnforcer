#!/usr/bin/env python3
""" Module to work out maths questions to ask """

import random
from math import sqrt

class Algebra:
    """ Class to work out maths questions to ask """
    def __init__(self):
        # simultaneous equation coefficients
        self.variable = {
            'a': 0, 'b': 0, 'c': 0, 'd': 0,
            'e': 0, 'f': 0, 'g': 0, 'h': 0,
            'x': 0, 'y': 0,
            'x_squared': 0, 'x_y': 0, 'y_squared': 0,
            'exp_question': '',
            'q_type': 0,
            'side': [0, 0, 0],
            'disp1': '', 'disp2': '',
            'perm': 0, 'heron': ''
        }

    def make_question(self):
        """ Function to work out maths questions to ask """
        self.variable['q_type'] = random.randint(1, 3)
        question_methods = {
            1: self.make_quest_simultaneous,
            2: self.make_quest_expand,
            3: self.make_quest_heron
        }
        question_methods.get(self.variable['q_type'], self.invalid_question)()

    def invalid_question(self):
        print("Eeeek! Question type invalid")

    def make_quest_simultaneous(self):
        """ Function to work out simultaneous equation questions to ask """
        while True:
            self.set_random_coefficients()
            self.variable['disp1'] = self.display_question(self.variable['a'], self.variable['b'], self.variable['c'], self.variable['d'])
            self.variable['disp2'] = self.display_question(self.variable['e'], self.variable['f'], self.variable['g'], self.variable['h'])
            if self.calculate_simultaneous():
                print(f"Answer is: X = {self.variable['x']}, Y = {self.variable['y']}")
                break

    def set_random_coefficients(self):
        """ Set random coefficients for the equations """
        for key in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            self.variable[key] = random.randint(1 if key in ['a', 'e'] else 0, 10) * self.rand_sign()

    def calculate_simultaneous(self):
        """ Calculate the values of x and y for simultaneous equations """
        try:
            self.variable['y'] = (
                (self.variable['e'] * self.variable['c']) -
                (self.variable['e'] * self.variable['d']) -
                (self.variable['a'] * self.variable['g']) +
                (self.variable['a'] * self.variable['h'])
            ) / (
                (self.variable['e'] * self.variable['b']) -
                (self.variable['a'] * self.variable['f'])
            )

            self.variable['x'] = (
                (self.variable['b'] * ((self.variable['e'] * self.variable['c']) -
                (self.variable['e'] * self.variable['d']) -
                (self.variable['a'] * self.variable['g']) +
                (self.variable['a'] * self.variable['h']))) /
                ((self.variable['e'] * self.variable['b']) -
                (self.variable['a'] * self.variable['f'])) -
                self.variable['c'] + self.variable['d']
            ) / self.variable['a']

            return True
        except ZeroDivisionError:
            return False

    def display_question(self, var_a, var_b, var_c, var_d):
        """ Work out questions to ask """
        disp_a = f"{var_a}x" if var_a != 1 else "x"
        disp_b = f"{var_b}y" if var_b != 1 else "y"
        disp_c = self.format_term(var_c)
        disp_d = self.format_term(var_d)
        
        return f"{disp_a}{disp_c} = {disp_b}{disp_d}"

    def format_term(self, term):
        """ Format a term for display """
        if term < 0:
            return f" - {abs(term)}"
        elif term > 0:
            return f" + {term}"
        return ""

    def rand_sign(self):
        """ Function to supply random sign """
        return random.choice([-1, 1])

    def make_quest_heron(self):
        """ Function to work out heron questions to ask """
        while True:
            self.variable['side'] = [random.randint(1, 10) for _ in range(3)]
            if self.is_valid_triangle(self.variable['side']):
                self.calculate_heron()
                print(f"Answer is: Area = {self.variable['heron']}")
                break

    def is_valid_triangle(self, sides):
        """ Check if the given sides can form a triangle """
        a, b, c = sides
        return a + b > c and a + c > b and b + c > a

    def calculate_heron(self):
        """ Calculate area using Heron's formula """
        s = sum(self.variable['side']) / 2
        self.variable['heron'] = "%.4f" % sqrt(s * (s - self.variable['side'][0]) * 
                                                  (s - self.variable['side'][1]) * 
                                                  (s - self.variable['side'][2]))

    def make_quest_expand(self):
        """ Function to work out expansion questions to ask """
        coefficients = [self.random_non_zero_coefficient() for _ in range(4)]
        coef1, coef2, coef3, coef4 = coefficients

        self.variable['x_squared'] = coef1 * coef3
        self.variable['x_y'] = (coef1 * coef4) + (coef2 * coef3)
        self.variable['y_squared'] = coef2 * coef4
        self.variable['exp_question'] = self.format_expansion_question(coef1, coef2, coef3, coef4)

        print(f"Answer is: {self.variable['x_squared']}, {self.variable['x_y']} & {self.variable['y_squared']}")

    def random_non_zero_coefficient(self):
        """ Generate a non-zero random coefficient """
        coef = 0
        while coef == 0:
            coef = random.randint(1, 10) * self.rand_sign()
        return coef

    def format_expansion_question(self, coef1, coef2, coef3, coef4):
        """ Format the expansion question """
        return f"({coef1}x {'-' if coef2 < 0 else '+'} {abs(coef2)}y)({coef3}x {'-' if coef4 < 0 else '+'} {abs(coef4)}y)"

if __name__ == '__main__':
    X_ALG = Algebra()
    X_ALG.make_question()
    # Printing the questions based on q_type
    question_types = {
        1: "Simultaneous Equation: {} and {}",
        2: "Expand And Simplify: {}",
        3: "Heron's Formula: Sides: {}, {}, {}"
    }
    q_type = X_ALG.variable['q_type']
    if q_type in question_types:
        print(question_types[q_type].format(
            X_ALG.variable['disp1'] if q_type == 1 else "",
            X_ALG.variable['disp2'] if q_type == 1 else X_ALG.variable['exp_question'],
            X_ALG.variable['side'] if q_type == 3 else ""
        ))
