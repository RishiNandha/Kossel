def export(name):
  import csv
  fields = []
  rows = []
  

  with open(name+".csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
     
    for row in csvreader:
      rows.append(row)
  f=open("anki.txt","w")
  for row in rows[::-1]:
    for i in range(len(row[2])):
      if row[2][i]==";":
        row[2]=row[2][:i]+"."+row[2][i+1:]
    if len(row[0])!=0:
      f.write(row[0]+r"<br>"+row[3]+";"+ row[1].lower()+r"<br>"+row[2]+"\n")

export("CY1001")