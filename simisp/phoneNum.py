# -*- coding: utf-8 -*-
# Started by Alan
# MainTained by Alan
# Contact: alan@sinosims.com

# Algorithm of inum & location finder:
#   input num
#   remove nation_code of num as inum
#   if nation_code isn't china:
#     inum founded and location is foreign
#     done
#   else:
#     if found city_code or 17951+city_node from inum
#       if inum starts with city_code, remove city_code
#       location is city
#     else:
#       if found sth. like 1xxxxxxxxxx, and try to match location as mobile number:
#         inum doesn't change, location founded
#     at last, try to match YELPAGE
#     done

from simisp.isp import ISPLOC
from simisp.ispPSTN import ISPPSTNLOC
from simisp.ispNation import ISPNATION
from simisp.yp import YELPAGE
import re

nation_replacer = re.compile(r"^(00|[+])(%s)" % \
                              "|".join( [nation for nation in ISPNATION.keys()] ))
city_replacer = re.compile(r"^(1\d\d\d\d)?(%s)" % \
                            "|".join([city for city in ISPPSTNLOC.keys()] ))
mobile_regex = re.compile(r"(1\d{6})\d\d\d\d$")

class Replacer:
  def __init__(self):
    self.reset()
    
  def toNation(self, m):
    self.last_replace_m = m
    return ""
  
  def toCity(self, m):
    self.last_replace_m = m
    return '' if m.group(1) == None else m.group(0)
  
  def reset(self):
    self.last_replace_m = None
    

def loads(num):
  loc = "未知地点"
  
  if num.startswith("*#"):
    return num, num, loc

  org_num = num
  rep = Replacer()
  inum = nation_replacer.sub(lambda m: rep.toNation(m), org_num)
  
  if rep.last_replace_m and rep.last_replace_m.group(2) != "86":   # foreign number
    loc = ISPNATION.get(rep.last_replace_m.group(2), loc)
  
  else:   # maybe chinese number
    org_num = inum
    rep.reset()
    inum = city_replacer.sub(lambda m: rep.toCity(m), org_num)
    
    if rep.last_replace_m:  # PTSN
      loc = ISPPSTNLOC.get(rep.last_replace_m.group(2), loc)    
    else: 
      m = mobile_regex.search(inum)
      if m: # maybe mobile
        loc = ISPLOC.get(m.group(1), loc)
    
    if YELPAGE.has_key(inum):
      loc = YELPAGE[inum]
  
  return [num, inum, loc]
  

def checkNum(number, cn):
    ld = loads(number)
    if ld[1] == cn:
        print  '\033[34m[OK] %s %s %s |%s|\033[0m'%(number, cn, ld[1], ld[2])
    else:
        print '\033[31m[ER] %s %s %s %s |%s|\033[0m'%(number, cn, ld[0], ld[1], ld[2])

if __name__ == '__main__':
    ns = [['13715054513', '13715054513'],
          ['+8613715054513', '13715054513'],
          ['15811208280', '15811208280'],
          ['+8617345872292', '17345872292'],
          ['008615811208280', '15811208280'],
          ['02988746532', '88746532'],
          ['17951075588746532', '17951075588746532'],
          ['1795113811813110', '1795113811813110'],
          ['057134562839', '34562839'],
          ['01034562839001', '34562839001'],
          ['1791117086542987', '1791117086542987'],
          ['013811813110', '013811813110'],
          ['87345678', '87345678'],
          ['8734567#', '8734567#'],
          ['23348976030', '23348976030'],
          ['913715054882', '913715054882'],
          ["0011234567", '1234567'],
          ["01010000", '10000'],
          ["95555", '95555']]

    [ checkNum(s[0], s[1]) for s in ns ]
