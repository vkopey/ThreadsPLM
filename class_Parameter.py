#-*- coding: utf-8 -*-
class Parameter(Agent):
    """Parameter. Базовий клас ..."""
    def __init__(self, name):
        super(Parameter,self).__init__(name)
        self.factorHigh=None
        self.factorLow=None