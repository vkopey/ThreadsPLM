#-*- coding: utf-8 -*-
class Property(Agent):
    """Property. Базовий клас властивостей"""
    def __init__(self, name):
        super(Property,self).__init__(name)
        self.inverseOf=None
        self.domain=set()
        self.range=set()
        self.SymmetricProperty=False
        self.TransitiveProperty=False
        self.FunctionalProperty=False
        
    def datalogRules(self):
        r=set()
        if self.inverseOf: r.add('%s(X,Y) <= %s(Y,X)'%(self.inverseOf, self.__name__))
        if self.SymmetricProperty: r.add('%s(X,Y) <= %s(Y,X)'%(self.__name__, self.__name__))
        return r