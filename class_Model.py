#-*- coding: utf-8 -*-
class Model(Agent):
    """Model.ШН19 ГОСТ 13877-96"""
    def __init__(self, name):
        super(Model,self).__init__(name)
        self.paramsIn={"радіус скруглень зарізьбової канавки":3.5,
                       "зовнішній радіус різьби ніпеля":13.26}
        self.paramsOut={'коефіцієнт запасу втомної міцності':None}
    def parseOutput(self,s,t):
        "Читає результат у змінну t: parseOutput(s,t='FOS')"
        t=t+'='
        for r in s.splitlines():
            if r.startswith(t):
                return float(r.partition(t)[2])
    def isSibling(self,model):
        "Моделі відрізняється знач. не більше ніж одного парам."
        a=self.paramsIn
        b=KB[model].paramsIn
        return isSibling(a,b)
    def rule(self):
        if None not in self.paramsOut.values(): return
        from subprocess import check_output
        p=r"e:\Anaconda2\python.exe"
        m=r"e:\!Kopey_Documents\Python_projects\ThreadsOCC\main.py"
        cnvName={"радіус скруглень зарізьбової канавки":"r3n",
                 "зовнішній радіус різьби ніпеля":"d_n",
                 "коефіцієнт запасу втомної міцності":"FOS"}
        args=[cnvName[k]+'='+str(v) for k,v in self.paramsIn.iteritems()]
        s=check_output([p, m]+args, shell=True)
        for k in self.paramsOut:
            self.paramsOut[k]=self.parseOutput(s,cnvName[k])
        
        