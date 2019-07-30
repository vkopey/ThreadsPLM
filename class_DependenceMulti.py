#-*- coding: utf-8 -*-
class DependenceMulti(Agent):
    """DependenceMulti"""
    def __init__(self, name):
        super(DependenceMulti,self).__init__(name)
        self.Xpars=None # independent variables
        self.Ypars=None # dependent variables
        self.X=[]
        self.Y=[]
        self.source=None
        
    def toDataFrame(self):
        import pandas as pd
        XY=self.X+self.Y
        return pd.DataFrame(data = zip(*XY), columns=self.Xpars+self.Ypars)
    
    def fromDataFrame(self,df):
        for i,xp in enumerate(self.Xpars):
            self.X[i]=[x for x in df[xp]]
        for i,yp in enumerate(self.Ypars):
            self.Y[i]=[y for y in df[yp]]
            
    def linregress(self, yp): # linear regression for parameter yp 
        X=np.array(self.X).T
        Y=self.Y[self.Ypars.index(yp)]
        from sklearn import linear_model
        reg = linear_model.LinearRegression()
        reg.fit(X, Y)
        return reg.coef_, reg.score(X, Y)
      
    def byModels(self):
        if KB.get(self.source).__class__.__name__!='Model': return
        df=self.toDataFrame()
        model=KB[self.source].__class__('tmp')
        print 'Temporary model created'
        for i in df.index: # for all points
            for xp in self.Xpars:
                model.paramsIn[xp]=df[xp][i]
                print xp,'=',df[xp][i]
            for yp in self.Ypars:    
                model.paramsOut[yp]=None
            model.rule()
            for yp in self.Ypars:    
                df[yp][i]=model.paramsOut[yp]
                print yp,'=',df[yp][i]
        self.fromDataFrame(df)
        
    def simModel(self,x,yp): #simulate Model
        model=KB[self.source].__class__('tmp')
        print 'Temporary model created', x
        for i,xp in enumerate(self.Xpars):
            model.paramsIn[xp]=x[i]
        model.rule()
        print 'y=',model.paramsOut[yp]
        return model.paramsOut[yp]
        
    def optimize(self,yp="коефіцієнт запасу втомної міцності",bounds=[(2.5,3.5),(12.7, 13.26)],maximize=True):
        from scipy.optimize import differential_evolution #minimize
        s = -1 if maximize else 1
        #res=minimize(lambda x,yp: s*self.simModel(x,yp), x0=[sum(p)/2.0 for p in bounds], args=(yp,), method="L-BFGS-B", bounds=bounds, options=dict(maxfun=10,eps=0.1))
        res=differential_evolution(lambda x,yp: s*self.simModel(x,yp), args=(yp,), bounds=bounds, maxiter=5, popsize=5, tol=0.1)
        return res
                   
    def rule(self):
        if None not in [item for sublist in self.Y for item in sublist]: return
        self.byModels()
 