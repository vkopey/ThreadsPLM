#-*- coding: utf-8 -*-
class Datalog(Agent):
    """Datalog."""
    def __init__(self, name):
        super(Datalog,self).__init__(name)
        self.oldfacts=set()
        
    def getDatalogFacts(self,facts):
        "Повертає список datalog-фактів зі списку фактів-тріплетів"
        dfacts=[]
        for k, p, v in facts:
            df='+%s(u"%s",u"%s")'%(p,k.decode('utf-8'),v.decode('utf-8'))
            dfacts.append(df)
        return dfacts
    
    def getDatalogRules(self):
        r=set()
        for k in KB:
            if hasattr(KB[k],'datalogRules'):
                r.update(KB[k].datalogRules())
        return r
               
    def rule(self):
        props=getClassObjects('Property')
        facts=KBToFacts()
        dfacts=self.getDatalogFacts(facts)
        drules=self.getDatalogRules()
        allFacts=runDatalog(dfacts, drules, props)
        factsToKB(allFacts)
        n=allFacts-self.oldfacts
        self.oldfacts=allFacts
        return len(n)