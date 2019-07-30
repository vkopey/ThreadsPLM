#-*- coding: utf-8 -*-
class Factor(Agent):
    """Factor. Базовий клас факторів"""
    def __init__(self, name):
        super(Factor,self).__init__(name)
        self.subClassOf=set()
        self.isCause=set()
        self.isEffect=set()
        self.isContraryOf=set()
        # 'subClassOf(O,B) :- subClassOf(A,B),subClassOf(O,A)'
    # def rule(self):
    #     "Правило установлює атрибути в підкласах, якщо їх немає"
    #     from tools import setAtrSubClasses
    #     return any( [setAtrSubClasses(__name__,"isCause",set()),
    #                 setAtrSubClasses(__name__,"isEffect",set()) ])

    # def rule(self):
    #     "Тільк для тестування прямого виведення. Ви можете протестувати цей алгоритм шляхом виключення агентів Datalog (active=False)."
    #     for k in KB:
    #         if KB[k].__class__.__name__!='Factor': continue
    #         if k not in self.isCause: continue
    #         if self.__name__ not in KB[k].__dict__['isEffect']:
    #             KB[k].__dict__['isEffect'].add(self.__name__)
    #             return True
        
        
    
