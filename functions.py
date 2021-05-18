import csv


def format(l,mode=0):
  if mode==0:
    b=l.split("->")
    for i in range(len(b)):
      j=b[i].split("+")
      for k in range(len(j)):
        j[k]=j[k].strip()
        for l in range(10):
          j[k]=j[k].lstrip(str(l))
        j[k]=j[k].lower()
        j[k]=j[k].replace(" ", "")
      b[i]=set(j)
    return b
  elif mode==2:
    b=l.split(",")
    b=[i.strip() for i in b]
    b=[i.lower() for i in b]
    b=set(b)
    return b
  elif mode==3:
    b=l.split(",")
    b=[i.strip() for i in b]
    b=[i.lower() for i in b]
    return b
  else:
    b=l.split()
    b=[i.lower() for i in b]
    b=set(b)
    return b

def questions(name):
  f=open("Decks/" +name+".csv","r")
  a = csv.reader(f)
  l=list()
  for i in a:
    if len(i)<5:
      for j in range(5-len(i)):
        i.append('')
    if len(i[1])==0:
      i[1]="Error: Answer was not given"
    if len(i[0])>0:
      if i[4] in [str(j) for j in range(10)]:
        l.append([" "+i[0],i[1],i[2],i[3],int(i[4])])
      else:
        l.append([" "+i[0],i[1],i[2],i[3],0])
  return l


def find_num(a):
  b = []
  a = list(a)
  c = ""
  for i in range(len(a)):
    a[i]=list(a[i])
    for j in range(len(a[i])):
      try:
        b.append(int(a[i][j]))
      except ValueError:
        pass
  # print(a)
  for i in range(len(b)):
    c+=str(b[i])
  if len(c) == 0:
    return 30
  else:
    return int(c)