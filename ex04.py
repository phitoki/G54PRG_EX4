#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 10:07:43 2018

"""

import itertools

def merge_lists(list1, list2):
    # merges two lists deleting duplicates. The lists contain the variables which we want only once in it.  
    return list1 + list(set(list2) - set(list1))

def generate_combinations(n):
 # itertools.product will generate all the binar combinations by returning an iterator and 
 # n will be the amount of variables we have in our expression
    return [list(i) for i in itertools.product([0, 1], repeat=n)]

class Expr :
    
    def __str__(self) :
        return self.str_aux(0)
    
   
    def get_evaluations(self):
        # get all the variables of the expression
        variables = self.get_variables()
        combinations = generate_combinations(len(variables))
        evaluations = []
        # loop through dictionnary
        for combination in combinations:
            dictionary = {}
            for i in range(0, len(variables)):
                dictionary[variables[i]] = combination[i]
            evaluations.append({'dictionary': dictionary, 'evaluation': bool(self.eval(dictionary)) })
            #print(evaluations)
        return evaluations
    
    def make_tt(self):
        variables = self.get_variables()
        evaluations = self.get_evaluations()
        buffer = ''
        for variable in variables:
            buffer += variable + '\t | '
        buffer += self.str_aux(0)
        buffer += '\n'
        # loop through all evaluations
        for evaluation in evaluations:
            # loop through the dictionary
            for variable, value in evaluation['dictionary'].items(): 
                #The items() method returns a view object that displays a list of a the dictionary
                buffer += str(bool(value)) + '\t | '
            buffer += str(evaluation['evaluation'])
            buffer += '\n'
        return buffer
    
    def isTauto(self):
        # returns if expression is a tautologie
        evaluations = self.get_evaluations()
        # loop through all the Booleans of evaluations to see if they are False
        for evaluation in evaluations:
            if evaluation['evaluation'] == False:
                return False
        return True


class Op(Expr) :
    # create class that has the prec and the symbol as attributes
    def __init__(self, prec, symbol):
        self.prec = prec
        self.symbol = symbol


class BinOp(Op) :    
    
    def __init__(self, prec, symbol, left_expression, right_expression):
        super().__init__(prec, symbol)
        self.left_expression = left_expression
        self.right_expression = right_expression
        
    def str_aux(self, prec) :
        s = self.left_expression.str_aux(self.prec) + self.symbol + self.right_expression.str_aux(self.prec)
        if self.prec < prec :
            return "("  + s + ")"
        else : 
            return s
        
    def get_variables(self):
        return merge_lists(self.left_expression.get_variables(), self.right_expression.get_variables())

        
class UniOp(Op) :    
    
    def __init__(self, prec, symbol, expression):
        super().__init__(prec, symbol)
        self.expression = expression
        
    def str_aux(self, prec) :
        s = self.symbol + self.expression.str_aux(self.prec)
        if self.prec < prec :
            return "(" + s + ")"
        else : 
            return s  
        
    def get_variables(self):
        return self.expression.get_variables()
        

class Not(UniOp):      
    

    def __init__(self, expression):
        super().__init__(4, '!', expression)  
        
    def eval(self, dictionary) :
        return not self.expression.eval(dictionary)
    

class And(BinOp):  
    
    def __init__(self, left_expression, right_expression):
        super().__init__(3, '&', left_expression, right_expression)
        
    def eval (self, dictionary):
        return self.left_expression.eval(dictionary) & self.right_expression.eval(dictionary)
    
      
class Or(BinOp):
    
    def __init__(self, left_expression, right_expression):
        super().__init__(2, '|', left_expression, right_expression)
        
    def eval (self, dictionary):
        return self.left_expression.eval(dictionary) | self.right_expression.eval(dictionary)
    
    
class Eq(BinOp):
    
    def __init__(self, left_expression, right_expression):
        super().__init__(1, '==', left_expression, right_expression) 
        
    def eval (self, dictionary):
        return self.left_expression.eval(dictionary) == self.right_expression.eval(dictionary)
    
    
class Var(Expr):    
    
    def __init__(self, variable):
        self.variable = variable   
        
    def str_aux(self, prec):
        return self.variable
    
    def eval(self, dictionary) :
        return dictionary[self.variable]
    
    def get_variables(self):
        return [self.variable]

e1 = Or(Var("x"),Not(Var("x")))
e2 = Eq(Var("x"),Not(Not(Var("x"))))
e3 = Eq(Not(And(Var("x"),Var("y"))),Or(Not(Var("x")),Not(Var("y"))))
e4 = Eq(Not(And(Var("x"),Var("y"))),And(Not(Var("x")),Not(Var("y"))))
e5 = Eq(Eq(Eq(Var("p"),Var("q")),Var("r")),Eq(Var("p"),Eq(Var("q"),Var("r"))))

print(e1)
print(e2)
print(e3)
print(e4)
print(e5)
"""
print(And(Not(Var("p")),Var("q")))
print(Not(And(Var("p"),Var("q"))))
print(Or(And(Var("p"),Var("q")),Var("r")))
print(And(Var("p"),Or(Var("q"),Var("r"))))
print(Eq(Or(Var("p"),Var("q")),Var("r")))
print(Or(Var("p"),Eq(Var("q"),Var("r"))))
"""
print (e2.eval({"x" : True}))
print (e3.eval({"x" : True, "y" : True}))
print (e4.eval({"x" : False, "y" : True}))
"""
print(e1.make_tt())
print(e2.make_tt())
print(e3.make_tt())
print(e4.make_tt())
print(e5.make_tt())

print (And(Var("x"),And(Var("y"),Var("z"))))
print (And(And(Var("x"),Var("y")),Var("z")))

print (e1.isTauto())
print (e2.isTauto())
print (e3.isTauto())
print (e4.isTauto())
print (e5.isTauto())
"""
