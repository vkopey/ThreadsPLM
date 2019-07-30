#-*- coding: utf-8 -*-
class Dependence(Agent):
    """Dependence. Базовий клас статистичних залежностей"""
    def __init__(self, name):
        super(Dependence,self).__init__(name)
        self.Xpar=None # independent variable
        self.Ypar=None # dependent variable
        self.X=[]
        self.Y=[]
        self.source=None
        
    def plot(self,plt):
        try:
            a=self.linregress()
            plt.plot(self.X,self.Y,'ko')
            x=np.array([min(self.X),max(self.X)])
            y=a[0]*x+a[1]
            plt.plot(x,y,'k-')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.show()
        except:
            pass
           
    def linregress(self):
        from scipy import stats
        return stats.linregress(self.X, self.Y)
    
    def fromModels(self): # result points from models
        if KB.get(self.source).__class__.__name__!='Model': return
        models=getClassObjects('Model')
        for k in models:
            m=KB[k]
            if not m.isSibling(self.source): continue
            if self.Xpar not in m.paramsIn: continue
            if self.Ypar not in m.paramsOut: continue
            y=m.paramsOut[self.Ypar]
            if y==None: continue
            x=m.paramsIn[self.Xpar]
            try:
                i=self.X.index(x)
                self.Y[i]=y # add Y value
            except ValueError:
                self.X.append(x) # add point
                self.Y.append(y)
        XY=zip(self.X, self.Y)
        XY.sort()
        self.X=[x for x,y in XY]
        self.Y=[y for x,y in XY]
        
    def modelExist(self, x): # model with x value exist?
        models=getClassObjects('Model')
        for m in models:
            if KB[m].paramsIn.get(self.Xpar)==x:
                return True
        return False
                  
    def toModels(self): # dynamically create models if y=None
        if KB.get(self.source).__class__.__name__!='Model': return
        for x,y in zip(self.X,self.Y):
            if y!=None or self.modelExist(x): continue
            k=autoKey("model")
            KB[k]=KB[self.source].__class__(k)
            KB[k].paramsIn[self.Xpar]=x
            print 'Model created'

            
    def rule(self):
        self.fromModels()
        self.toModels()
        if None in self.Y: return
        if not len(self.Y)>1: return
        slope, intercept, r_value, p_value, std_err=self.linregress()
        #print slope, intercept, r_value, p_value, std_err
        if r_value**2<0.5: return False
        #https://en.wikipedia.org/wiki/Correlation_does_not_imply_causation
        try:
            if slope>0: # додатня кореляція
                KB[KB[self.Xpar].factorHigh].isCause.add(KB[self.Ypar].factorHigh)
            else:
                KB[KB[self.Xpar].factorLow].isCause.add(KB[self.Ypar].factorHigh)
        except KeyError:
            pass
 