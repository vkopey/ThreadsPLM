#-*- coding: utf-8 -*-
"Це приклад роботи з системою"
from tools import *

files=getFiles()
createClasses(files)
createKB(files)
#loadKB()

applyRules(n=10)
#saveKB()

