from pyplasm import *
import csv
from workshop_10 import *
#non funziona
def getPoints(linesPath): #altezza predefinita 2,5m
	#creo le porte
	with open(linesPath, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		points = []
		for row in reader:
			print(row[0])
			points.append([float(row[1]),float(row[0])])
	return points


def getStreet(controls):
	bezier = MAP( BEZIER(S1)(controls) )(INTERVALS(1)(332))
	strada=bezier
	strada = STRUCT([OFFSET([0.1,0.1])(bezier)])
	return strada
def createStreet():
	strada1 = getStreet([[0,5],[2,5.5]])
	strada2 = getStreet([[2,3.5],[2,5.5],[2,7.5],[3,10],[4,11]])
	strada3 = getStreet([[2.5,7.5],[5,6],[6,8.5],[7,11.5],[7.5,10],[8.5,7],[9.5,6],[11.5,7],[15,7],[17,6.8],[18,6.5],[19.5,5.5],[20,4.5],[20.5,3.5],[20.5,1],[20.5,0]])
	strada4 = getStreet([[18,5.8],[19,7],[21,7.5],[21.5,7.8],[22.5,8],[25,9],[27,11],[27,13],[27,14],[27,15]])
	strada5 = getStreet([[19.2,5],[21,5.5],[21,6],[21.7,7.8]])
	strada6 = getStreet([[4.5,7.2],[5.2,6],[5,5.5],[5.5,5],[8.7,8.1]])
	strada7 = getStreet([[20.2,1],[19.5,1]])
	return STRUCT([strada1,strada2,strada3,strada4,strada5,strada6,strada7])
def createBase(HPC):
	box =BOX([1,2])(HPC)
	box = OFFSET([1,1,1.5])(box)
	return box


streets = createStreet()
streets = STRUCT([S([1,2,3])([2.5,2.5,2.5]),streets])
box = createBase(streets)
casa = createHouse()
casa = STRUCT([S([1,2,3])([0.1,0.1,0.1]),casa])
casa = rotationAngle(casa,PI/4.5)

model = STRUCT([streets,T([1,2])([9.5,19]),casa,T([1,2])([2,2]),casa,T([1,2])([2,2]),casa])

VIEW(casa)
VIEW(model)
