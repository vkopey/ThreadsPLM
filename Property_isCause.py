#-*- coding: utf-8 -*-
"""isCause. Властивість 'є причиною'"""
inverseOf="isEffect"
domain={"Factor"}
range={"Factor"}

datalogRules_=KB['isCause'].datalogRules
def datalogRules():
    r={'isCause(X,Y) <= isCause(B,Y) & subClassOf(X,B)',
       'isEffect(X,Y) <= isEffect(B,Y) & subClassOf(X,B)'}
    return r|datalogRules_()
