#-*- coding: utf-8 -*-
"""isContraryOf. Властивість 'є протилежністю'"""
domain={"Factor"}
range={"Factor"}
def datalogRules():
    r={'isCause(X, Y) <= isContraryOf(X, NX) & isCause(NX, NY) & isContraryOf(Y, NY)',
       'isEffect(X, Y) <= isContraryOf(X, NX) & isEffect(NX, NY) & isContraryOf(Y, NY)'}
    return r
