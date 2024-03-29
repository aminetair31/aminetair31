"""
Model generation for CPLEX
Input  : Data TextFile  "data.txt" generated by DataGen.py
Output : LP-CPLEX Model "model.lp" 
"""
import os
import numpy as np
import random
import sys  


#Transfer of data generated by DateGen.py in "data.txt"  to RAM (Arrays and variables)
cost=[]        #Travel times
mArray=[]      #number of vehicles assigned to each start-office
QArray=[]      #vehicles capacity
PArray=[]      #Waiting persons at each start and intermediate nodes

fichier = open(sys.argv[1], "r")
line=fichier.readline()

fin=line.index(" ")
s=int(line[0:fin])   # number of start-offices
line=line[fin+1:]

fin=line.index(" ")
e=int(line[0:fin])   # number of end-offices
line=line[fin+1:]

fin=line.index(" ")
b=int(line[0:fin])   # number of bus-stops (intermediate nodes)
line=line[fin+1:]

m=int(line)          # number of vehicles
#Travel times or distances (cost) reading
line=fichier.readline()
for i in range(b*(s+e+b-1)):
    fin=line.index(" ")
    x = int(line[0:fin])
    line=line[fin+1:]
    cost.append(x)
#Number of vehicles assigned to start-offices reading
line=fichier.readline()
tot=0
for i in range(s):
    fin=line.index(" ")
    x = int(line[0:fin])
    line=line[fin+1:]
    mArray.append(x)
    tot = tot + x
#Vehicles capacities reading
line=fichier.readline()
totcap=0
for i in range(m):
    fin=line.index(" ")
    x = int(line[0:fin])
    line=line[fin+1:]
    QArray.append(x)
    totcap=totcap+x
#Waiting persons Number reading
line=fichier.readline()
tot=0
for i in range(s):
    fin=line.index(" ")
    x = int(line[0:fin])
    line=line[fin+1:]
    PArray.append(x)
    tot=tot+x
for i in range(b):
    fin=line.index(" ")
    x = int(line[0:fin])
    line=line[fin+1:]
    PArray.append(x)
    tot=tot+x
N=tot

#Model LP-CPLEX Generation
model = open(sys.argv[2], "w")

model.write("\\Problem name: TRANSPORT")
model.write("\n")
model.write("Minimize")
model.write("\n")
model.write(" obj: ")

#Objective Function (1)
varia = open("varia.txt","w") #Auxiliary file for decision variables
p=0
nbvar=0
for i in range(s):
	for j in range(b):
		cc = cost[p]
		p = p+1
		for k in range(m):
			model.write(str(cc)+" x"+str(i+1)+"_"+str(j+s+1)+"_"+str(k+1)+" + ")
			varia.write("x"+str(i+1)+"_"+str(j+s+1)+"_"+str(k+1)+"\n")
			nbvar+=1
for i in range(b):
	for j in range(b):
		if s+i+1 != s+j+1:
			cc = cost[p]
			p = p+1
			for k in range(m):
				model.write(str(cc)+" x"+str(s+i+1)+"_"+str(j+s+1)+"_"+str(k+1)+" + ")
				varia.write("x"+str(s+i+1)+"_"+str(j+s+1)+"_"+str(k+1)+"\n")
				nbvar+=1
for i in range(b):
	for j in range(e):
		cc = cost[p]
		p = p+1
		for k in range(m):
			varia.write("x"+str(s+i+1)+"_"+str(j+s+b+1)+"_"+str(k+1)+"\n")
			if nbvar==(b*m*(s+e+b-1)-1):  #last variable
				model.write(str(cc)+" x"+str(s+i+1)+"_"+str(j+s+b+1)+"_"+str(k+1)+"\n")
				nbvar+=1
			else:
				model.write(str(cc)+" x"+str(s+i+1)+"_"+str(j+s+b+1)+"_"+str(k+1)+" + ")
				nbvar+=1
model.write(" Subject To\n")
nbc=0

#Constraints (2)
for j in range(b):
	nbc+=1
	model.write("  c"+str(nbc)+": ")
	first=1
	for i in range(s+b):
		if i!=j+s:
			for k in range(m):
				if first==0:
					model.write(" + ")
				model.write("x"+str(i+1)+"_"+str(j+s+1)+"_"+str(k+1))
				first=0 
	model.write(" >= 1\n")				

#Constraints (3)
for i in range(b):
	nbc+=1
	model.write("  c"+str(nbc)+": ")
	first=1
	for j in range(e+b):
		if i+s!=j+s:
			for k in range(m):
				if first==0:
					model.write(" + ")
				model.write("x"+str(i+s+1)+"_"+str(j+s+1)+"_"+str(k+1))
				first=0 
	model.write(" >= 1\n")				

#Constraints (4)
for k in range(b):
	for l in range(m):
		nbc+=1
		model.write("  c"+str(nbc)+": ")
		first=1
		for i in range(s+b):
			if i!=k+s:
				if first==0:
					model.write(" + ")
				model.write("x"+str(i+1)+"_"+str(k+s+1)+"_"+str(l+1))
				first=0
		for j in range(e+b):
			if j+s!=k+s:
				model.write(" - ")
				model.write("x"+str(k+s+1)+"_"+str(j+s+1)+"_"+str(l+1))
		model.write(" = 0\n")				

#Constraints (5)
for i in range(s):
	nbc+=1
	model.write("  c"+str(nbc)+": ")
	first=1
	for j in range(b):
		for k in range(m):
			if first==0:
				model.write(" + ")
			model.write("x"+str(i+1)+"_"+str(j+s+1)+"_"+str(k+1))
			first=0 
	model.write(" <= "+str(mArray[i])+"\n")				

#for j in range(e):
	#nbc+=1
	#model.write("  c"+str(nbc)+": ")
	#first=1
	#for i in range(b):
	#	for k in range(m):
	#		if first==0:
	#			model.write(" + ")
	#		model.write("x"+str(i+s+1)+"_"+str(j+s+b+1)+"_"+str(k+1))
	#		first=0 
	#model.write(" >= 1\n")				

#Constraints (7)
for l in range(m):
	for i in range(b):
		for j in range(b):
			if i != j:
				nbc+=1
				model.write("  c"+str(nbc)+": ")
				model.write("u"+str(i+s+1)+"_"+str(l+1)+" + 101 x"+str(i+s+1)+"_"+str(j+s+1)+"_"+str(l+1)+" - u"+str(j+s+1)+"_"+str(l+1)+" <= 100\n")

#Constraints (8)
for k in range(m):
	nbc+=1
	model.write("  c"+str(nbc)+": ")
	first=1
	for i in range(s):
		for j in range(b):
			if first==0:
				model.write(" + ")
			model.write("x"+str(i+1)+"_"+str(j+s+1)+"_"+str(k+1))
			first=0 
	model.write(" <= 1\n")				

#Constraints (9)
for k in range(m):
	nbc+=1
	model.write("  c"+str(nbc)+": ")
	first=1
	for i in range(s+b):
		if first==0:
			model.write(" + ")
		model.write("y"+str(i+1)+"_"+str(k+1))
		first=0
	model.write(" <= "+str(QArray[k])+"\n")

#Constraints (10)
for i in range(s+b):
	nbc+=1
	model.write("  c"+str(nbc)+": ")
	first=1
	for k in range(m):
		if first==0:
			model.write(" + ")
		model.write("y"+str(i+1)+"_"+str(k+1))
		first=0
	model.write(" >= "+str(PArray[i])+"\n")

#Constraints (11)
for i in range(s):
	for k in range(m):
		nbc+=1
		model.write("  c"+str(nbc)+": y"+str(i+1)+"_"+str(k+1))
		for j in range(b):
			model.write(" - "+str(N)+" x"+str(i+1)+"_"+str(j+s+1)+"_"+str(k+1))
		model.write(" <= 0\n")

#Constraints (12)
for k in range(b):
	for l in range(m):
		nbc+=1
		model.write("  c"+str(nbc)+": y"+str(k+s+1)+"_"+str(l+1))
		for i in range(s+b):
			if i!=k+s:
				model.write(" - "+str(N)+" x"+str(i+1)+"_"+str(s+k+1)+"_"+str(l+1))
		for j in range(e+b):
			if j+s!=k+s:
				model.write(" - "+str(N)+" x"+str(s+k+1)+"_"+str(j+s+1)+"_"+str(l+1))
		model.write(" <= 0\n")


#Constraints (13) and (14) Decision variables range
varia.close()
varia = open("varia.txt","r")

model.write(" Binary\n")
for i in range(nbvar):
	line=varia.readline()
	model.write(line)
model.write("End")
varia.close()
fichier.close()
model.close()

if tot>totcap:
	print("Error : Overall number of waiting persons greater than total vehicles capacity")
else:
	print("LP Model (model.lp) generated successfully")

print("Graph size                : "+str(s+e+b)+" ("+str(s)+" start-offices, "+str(e)+" end-offices, "+str(b)+" bus-stops)")
print("Fleet size                : "+str(m)+ " shuttle buses")
print("Total waiting persons     : "+str(tot))
print("Total vehicles capacity   : "+str(totcap))
print("----------------------------------------")
print("#Variables   : "+str(nbvar))
print("#Constraints : "+str(nbc))
