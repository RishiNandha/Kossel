import csv
import reactions
import random

def format(l):
  b=l.split("->")
  for i in range(len(b)):
    j=b[i].split("+")
    for k in range(len(j)):
      j[k]=j[k].strip()
      for l in range(10):
        j[k]=j[k].strip(str(l))
    b[i]=set(j)
  return b

def questions(name):
  f=open(name+".csv","r")
  a = csv.reader(f)
  l=list()
  for i in a:
    l.append([" "+i[0],format(i[1]),i[2]])
  return l

def pack_answer_set(l):
  a = ""
  for i in l[0]:
    a += i
  return a