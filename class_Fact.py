#-*- coding: utf-8 -*-
class Fact(Agent):
    """Fact. Базовий клас фактів"""
    def __init__(self, name):
        super(Fact,self).__init__(name)
        self.subject=None
        self.predicate=None
        self.objecT=None
        self.sources=set()
    def rule(self):
        for k in KB:
            if k!=self.predicate: continue
            if KB[k].__class__.__name__!='Property': continue
            if self.subject not in KB[k].domain: continue
            if self.objecT not in KB[k].range: continue
            try:
                if KB[k].FunctionalProperty:
                    KB[self.subject].__dict__[k]=self.objecT
                else:
                    KB[self.subject].__dict__[k].add(self.objecT)
                break
            except KeyError:
                pass
        