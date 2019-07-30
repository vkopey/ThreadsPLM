#-*- coding: utf-8 -*-
import sys,os,re
import numpy as np
KB={}
systemencoding=sys.getfilesystemencoding() #'mbcs'

def getFiles(ex={'main.py','tools.py'} ):
    "Повертає список файлів поточного каталогу в довільному порядку"
    files=os.listdir(os.getcwdu())
    files=[f for f in files if f[-3:]=='.py' and f not in ex]
    #print 'files:',files
    return files
    
def createClasses(files):
    files=[f for f in files if f.startswith('class_')]
    while files:
        f=files.pop(0)
        try:
            execfile(f.encode(systemencoding), globals()) #KB
        except NameError:
             files.append(f)

def createKB(files):
    "Створює систему агентів з модулів files"
    files=[f for f in files if not f.startswith('class_')]
    for f in files:
        cls,_,name=f.partition('_')
        name=name[:-3].encode('utf-8')
        #if name in KB: continue
        obj=globals()[cls](name)
        obj.__dict__['KB']=KB
        KB[obj.__name__]=obj
        execfile(f.encode(systemencoding), obj.__dict__)

def getClassObjects(clsName):
    return [k for k in KB if KB[k].__class__.__name__==clsName]
        
def KBToPropFacts(prop):
    "Повертає усі факти-тріплети KB з властивістю prop (prop має бути set)"
    facts=set()
    for k in KB:
        if hasattr(KB[k], prop):
            if KB[prop].FunctionalProperty:
                facts.add((k, prop, KB[k].__dict__[prop]))
            else:
                for v in KB[k].__dict__[prop]:
                    facts.add((k, prop, v))
    return facts

def KBToFacts():
    "Повертає усі факти-тріплети KB"
    facts=set()
    props=getClassObjects('Property')
    for p in props:
        facts.update(KBToPropFacts(p))
    return facts
    
def factToKB(subj,pred,obj):
    "Оновлює значення властивості об`єкта за тріплетом"
    #потрібна також перевірка на Domain i Range!
    if not(KB.has_key(pred) and KB[pred].__class__==Property): return #Property in KB[pred].__class__.__mro__
    if KB.has_key(subj) and hasattr(KB[subj],pred):
        if KB[pred].FunctionalProperty:
            KB[subj].__dict__[pred]=obj
        else:
            KB[subj].__dict__[pred].add(obj)

def factsToKB(facts):
    "Оновлює всю KB за списком фактів-тріплетів"
    for s,p,o in facts:
        factToKB(s,p,o)    
    
def runDatalog(facts, rules, predicates):
    """виконує логічне виведення в pyDatalog. Повертає список тріплетів.
    facts - список Datalog-фактів,
    rules - список Datalog-правил,
    predicates - список предикатів, для яких будуть шукатись факти"""
    
    #if not predicates:
    #    predicates={p for s,p,o in facts}|{r.split('(')[0] for r in rules}
    
    from pyDatalog.pyDatalog import assert_fact, load, ask, clear
    code='\n'.join(facts)+'\n'+'\n'.join(rules) # факти і правила
    load(code)
    allFacts=set()
    for pred in predicates:
        # try:
        res=ask('%s(X,Y)'%pred).answers
        # except AttributeError: #Predicate without definition
        #     continue
        for subj,obj in res:
            allFacts.add((subj.encode('utf-8'),pred.encode('utf-8'),obj.encode('utf-8')))
            print subj,pred,obj
    clear()
    return allFacts

def subClasses(n, s=set()):
    "Множина усіх субобєктів обєкта n. Рекурсивна."
    for k in KB:
        if n in KB[k].subClassOf:
            s.add(k)
            s.update(subClasses(k, s))
    return s
    
def setAtrSubClasses(name, attr, value, ch=False):
    "Установлює значення value усім атрибутам attr усіх підкласів обєкта name, якщо атрибута немає"
    for k in subClasses(name,set()):
        if not hasattr(KB[k],attr):
            setattr(KB[k],attr,value)
            ch=True
    return ch

def applyRules(lst=KB,n=5):
    "Застосовує правила до кожного агента з lst n раз поки є зміни"
    ch=True
    while ch and n>0: # поки правила створюють зміни
        ch=False
        print '*ApplyRules*'
        for k in lst.keys():
            if KB[k].active and KB[k].rule(): ch=True
        n-=1
        
def saveKB(lst=KB,new=True):
    import shelve
    from dill import Pickler
    shelve.Pickler = Pickler
    KBp=shelve.open("shelve.dat")
    if new: KBp.clear()
    for k in lst:
        KBp[k]=KB[k]
    KBp.close()
    
def loadKB():
    import shelve
    from dill import Unpickler
    shelve.Unpickler = Unpickler
    KBp=shelve.open("shelve.dat")
    for k in KBp:
        KB[k]=KBp[k]
    KBp.close()
    
def find(regexp=".*", lst=KB):
    """Повертає список назв, які відповідають регулярному виразу"""
    res=[]
    po=re.compile(regexp, re.IGNORECASE | re.UNICODE)
    for k in lst:
        mo=po.search(k.decode('utf-8'))
        if mo:
            res.append(k)
            print k
    res.sort() # сортувати
    return res

def createFile(cls,name):
    fname=cls+'_'+name+'.py'
    fname=fname.decode('utf-8') #to unicode
    if os.path.exists(fname):
        print 'Error! File exists'
        return
    t='''#-*- coding: utf-8 -*-
"""%s_%s"""
'''%(cls,name)
    with open(fname,'w') as f:
        f.write(t)
    return fname

def autoKey(start):
    """Генерує унікальний ключ для KB шляхом додавання цілого числа до start"""
    k=start+'0'
    n=0
    while k in KB.keys():
        n+=1
        k=start+str(n)
    return k
    
def isSibling(a,b):
    "Словники рівні або відрізняється знач. не більше ніж одного парам."
    if a==b: return True
    if set(a.keys()) ^ set(b.keys()): return False # keys difference
    d=set(a.items()) ^ set(b.items()) # difference
    return len(d)==2

def query1():
    for v in KB["концентрація напружень"].isEffect:
        print v
    #print KB["isCause"].__doc__

def query2():
    import matplotlib.pyplot as plt
    d=KB['dependence2']
    print d.linregress()
    d.plot(plt)
    
    
def query3():
    import networkx as nx
    G = nx.DiGraph()
    for i in KB:
        if KB[i].__class__.__name__=='Factor':
            for j in KB[i].isCause:
                G.add_edge(i.decode('utf-8'), j.decode('utf-8'), label='isCause')
    
    pr=nx.pagerank(G) # for DiGraph only
    pr={k:'%s\n%f'%(k,v) for k,v in pr.iteritems()}
    G=nx.relabel_nodes(G, pr)            
    nx.drawing.nx_agraph.write_dot(G,'graph.dot')
    os.system(r'"d:\Program Files\Graphviz2.38\bin\dot.exe" -Tsvg graph.dot -o graph.svg') # конвертуємо в SVG
    #nx.write_graphml_lxml(G, "graph.graphml")
##
def query4():
    def proToEdges(pro):
        if KB[pro].FunctionalProperty:
            G.add_edge(i.decode('utf-8'), KB[i].__dict__[pro].decode('utf-8'), label=pro)
            return
        for j in KB[i].__dict__[pro]:
            G.add_edge(i.decode('utf-8'), j.decode('utf-8'), label=pro)
            
    import networkx as nx
    G = nx.MultiDiGraph()
    for i in KB:
        if KB[i].__class__.__name__=='Factor':
            proToEdges('isCause')
            proToEdges('isEffect')
            proToEdges('subClassOf')
            proToEdges('isContraryOf')
        if KB[i].__class__.__name__=='Fact':
            proToEdges('objecT')
            proToEdges('subject')
        if KB[i].__class__.__name__=='Parameter':
            proToEdges('factorHigh')
            proToEdges('factorLow')
        if KB[i].__class__.__name__=='Dependence':
            proToEdges('Xpar')
            proToEdges('Ypar')
            proToEdges('source')
    nx.drawing.nx_agraph.write_dot(G,'graph.dot')
    replaceLongStr('graph.dot')
    os.system(r'"d:\Program Files\Graphviz2.38\bin\dot.exe" -Tsvg graph.dot -o graph.svg') # конвертуємо в SVG
##
def replaceLongStr(file='graph.dot'):
    def repl(mo):
        s=mo.group(1) # рядок знайденої групи
        n = 20 # кількість символів в рядку
        s=r'\n'.join([s[i:i+n] for i in range(0, len(s), n)])
        return s
    import re
    all=open(file,'r').read()
    po=re.compile(r'(".*?")', re.UNICODE|re.DOTALL)
    all=re.sub(po, repl, all.decode('utf-8'))
    f=open(file,'w')
    f.write(all.encode('utf-8'))
    f.close() 
      