#-*- coding: utf-8 -*-
class Agent(object):
    "Інтелектуальний агент"
    def __init__(self, name):
        self.__name__=name
        self.active=True
        
    def rule(self):
        "Правило поведінки агента. Повертає 1, якщо його застосування призвело до змін"
        return False #у іншому випадку повертає False або нічого не повертає