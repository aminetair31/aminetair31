"""
Instance Data generation
Input  : Instance size
Output : Data textFile "data.txt" 
"""

import os
import numpy as np
import random


#Parameters related to instance size
s=2    #Start-offices
e=3    #End-offices
b=3    #Stop-bus
m=3    #Vehicle number
cap=30 #Vehicle capacity

#Parameters used to adjust number of waiting persons at start and stop offices
startLowRate=0.7
startHighRate=1.7
stopLowRate=0.2
stopHighRate=0.5

fichier = open("data.txt", "w")

#First Line : startNodeNumber endNodeNumber intermediateNodeNumber VehicleNumber
fichier.write(str(s)+" "+str(e)+" "+str(b)+" "+str(m)+"\n")


#Second Line : Travel time or distance between graph nodes randomly generated in a range of [1,100]
for i in range(b*(s+e+b-1)):
	x = random.randint(1,100)
	fichier.write(str(x)+" ")
fichier.write("\n")

#Third Line : Number of vehicles assigned to each start-office
mArray=[]
tot=0
for i in range(s-1):
	x = int(m/s)
	fichier.write(str(x)+" ")
	tot = tot + x
	mArray.append(x)
fichier.write(str(m-tot)+" \n")
mArray.append(m-tot)

#Fourth Line : Vehicle capacity (Initially all the vehicles have the same capacity)
totcap=0
for i in range(m):
	fichier.write(str(cap)+" ")
	totcap=totcap+cap
fichier.write("\n")

#Fifth Line : Waiting persons Number at each start-office
tot=0
for i in range(s):
	x = random.randint(int(startLowRate*m*cap/(s+b)),int(startHighRate*m*cap/(s+b)))
	if x>mArray[i]*cap:
		x=mArray[i]*cap
	fichier.write(str(x)+" ")
	tot=tot+x
#Fifth Line : Waiting persons Number at each intermediate node
for i in range(b):
	x = random.randint(int(stopLowRate*m*cap/(s+b)),int(stopHighRate*m*cap/(s+b)))
	fichier.write(str(x)+" ")
	tot=tot+x

if tot>totcap:
	print("Error : Overall number of waiting persons greater than total vehicles capacity")
else:
	print("Data file (data.txt) generated successfully")

fichier.close()

print("Graph size             : "+str(s+e+b)+" ("+str(s)+" start-offices, "+str(e)+" end-offices, "+str(b)+" bus-stops)")
print("Fleet size             : "+str(m)+ " vehicles")
print("Total waiting persons : "+str(tot))
print("Total vehicle capacity   : "+str(totcap))
