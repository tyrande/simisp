# -*- coding: utf-8 -*-
# Started by Alan
# MainTained by Alan
# Contact: alan@sinosims.com

from simisp.isp import ISPLOC
from simisp.ispPSTN import ISPPSTNLOC
from simisp.yp import YELPAGE
import re

rg = [['^(179\d{2})*(00|\+)*(86|0)*(1[34578][0-9]\d{4,8})$', [4], 1],
      ['^(179\d{2})*(0[12][0-9])(\d{7,8})(\d{3,4})*(#)*$', [2,3], 2],
      ['^(179\d{2})*(0[3456789]\d{2})(\d{7,8})(\d{3,4})*(#)*$', [2,3], 2],
      ['^(179\d{2})*(\d{7,8})(\d{3,4})*(#)*$', [2], 3],
      ['^(179\d{2})*(\d{7,8})(\d{3,4})*(#)*$', [2], 3]]

def loads(num):
    for r in rg:
        m = re.search(r[0], num)
        if m:
            if r[2] == 1:
                loc = ISPLOC.get(m.group(4)[0:7], '未知地点').replace(',', '')
            elif r[2] == 2:
                loc = "%s %s"%(ISPPSTNLOC.get(m.group(2), '未知地点'), '固话')
            else:
                loc = '未知地点'
            return ['_'.join([ g for g in m.groups() if g ]), ''.join([ m.group(i) for i in r[1] ]), loc]
    loc = YELPAGE.get(num, '未知地点')
    return [num, num, loc] 

def checkNum(number, cn):
    ld = loads(number)
    if ld[0] == cn:
        print  '\033[34m[OK] %s %s %s |%s|\033[0m'%(number, cn, ld[1], ld[2])
    elif ld[0] == number:
        print '\033[31m[NM] %s %s\033[0m'%(number, cn)
    else:
        print '\033[31m[ER] %s %s %s %s |%s|\033[0m'%(number, cn, ld[0], ld[1], ld[2])

if __name__ == '__main__':
    ns = [['13715054513', '13715054513'], 
          ['+8613715054513', '+_86_13715054513'], 
          ['15811208280', '15811208280'], 
          ['+8617345872292', '+_86_17345872292'],
          ['008615811208280', '00_86_15811208280'], 
          ['02988746532', '029_88746532'], 
          ['17951075588746532', '17951_0755_88746532'],
          ['057134562839', '0571_34562839'],
          ['01034562839001', '010_34562839_001'],
          ['1791117086542987', '17911_17086542987'],
          ['013811813110', '0_13811813110'],
          ['87345678', '87345678'],
          ['8734567#', '8734567_#'],
          ['23348976030', '23348976_030']]

    [ checkNum(s[0], s[1]) for s in ns ]