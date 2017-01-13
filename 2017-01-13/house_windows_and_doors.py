from house_structure import *
def getDataExternalDoors (dimX,dimY):
	#genero i muri esterni
	externalWalls = building_wall("lines/esterno.lines",6,3)
	#calcolo i fattori di scala x e y 
	xfactor=dimX/SIZE([1])(externalWalls)[0]
	yfactor=dimY/SIZE([2])(externalWalls)[0]
	#ridimensiono
	externalWalls = (S([1,2])([xfactor,yfactor])(externalWalls))
	#creo cubi dove andranno le porte e li metto, uno ad uno, in un array
	with open("lines/porte.lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		doorsList = []
		cuboid = []
		acc = 0
		for row in reader:
			acc = acc + 1
			cuboid.append([float(row[0]),float(row[1])])
			if(acc == 4):
				cub=STRUCT([MKPOL([cuboid,[[1,2,3,4]],None])])
				cub = PROD([cub, Q(2.5)])
				cub = (S([1,2])([xfactor,yfactor])(cub))
				doorsList.append(cub)
				cuboid = []
				acc = 0

	#per ogni cubo mi trovo la corrispettiva porta e calcolo la dimensione e la posizione 
	dataDim=[]

	for c in doorsList:
		externalWalls2=DIFFERENCE([externalWalls,c])
		door = DIFFERENCE([externalWalls,externalWalls2])
		sizeDoor = SIZE([1,2])(door)
		if (sizeDoor[0] != 0.0 and sizeDoor[1] != 0.0):
			#grandezza porta
			doorDimension=SIZE([1,2,3])(door)
			#posizione porta
			c=CUBOID([1,1,1])
			box =STRUCT([c,door])
			box = BOX([1,2,3])(box)
			distanceDoor=SIZE([1,2])(box)
			doorPosition=[distanceDoor[0]-doorDimension[0],distanceDoor[1]-doorDimension[1]]
			#inserisco la posizione e la dimensione in un array
			dataDim.append([doorDimension,doorPosition])

	return dataDim
	
def getDatainternalDoors(dimX,dimY):
	#genero i muri interni
	externalWalls = building_wall("lines/esterno.lines",6,3)
	internalWalls = building_wall("lines/interno.lines",3,3)
	internalWalls = STRUCT([externalWalls,internalWalls])
	#calcolo i fattori di scala x e y 
	xfactor=dimX/SIZE([1])(internalWalls)[0]
	yfactor=dimY/SIZE([2])(internalWalls)[0]
	#ridimensiono
	internalWalls = (S([1,2])([xfactor,yfactor])(internalWalls))
	externalWalls = (S([1,2])([xfactor,yfactor])(externalWalls))
	internalWalls=DIFFERENCE([internalWalls,externalWalls])
	#creo cubi dove andranno le porte e li metto, uno ad uno, in un array
	with open("lines/porte.lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		doorsList = []
		cuboid = []
		acc = 0
		for row in reader:
			acc = acc + 1
			cuboid.append([float(row[0]),float(row[1])])
			if(acc == 4):
				cub=STRUCT([MKPOL([cuboid,[[1,2,3,4]],None])])
				cub = PROD([cub, Q(2.5)])
				cub = (S([1,2])([xfactor,yfactor])(cub))
				doorsList.append(cub)
				cuboid = []
				acc = 0

	#per ogni cubo mi trovo la corrispettiva porta e calcolo la dimensione e la posizione 
	dataDim=[]

	for c in doorsList:
		internalWalls2=DIFFERENCE([internalWalls,c])
		door = DIFFERENCE([internalWalls,internalWalls2])
		sizeDoor = SIZE([1,2])(door)
		if (sizeDoor[0] != 0.0 and sizeDoor[1] != 0.0):
			#grandezza porta
			doorDimension=SIZE([1,2,3])(door)
			#posizione porta
			c=CUBOID([1,1,1])
			box =STRUCT([c,door])
			box = BOX([1,2,3])(box)
			distanceDoor=SIZE([1,2])(box)
			doorPosition=[distanceDoor[0]-doorDimension[0],distanceDoor[1]-doorDimension[1]]
			#inserisco la posizione e la dimensione in un array
			dataDim.append([doorDimension,doorPosition])

	return dataDim

from house_structure import *

def getDataWindows (dimX,dimY):
	#genero i muri esterni
	externalWalls = building_wall("lines/esterno.lines",6,3)
	#calcolo i fattori di scala x e y 
	xfactor=dimX/SIZE([1])(externalWalls)[0]
	yfactor=dimY/SIZE([2])(externalWalls)[0]
	#ridimensiono
	externalWalls = (S([1,2])([xfactor,yfactor])(externalWalls))
	#creo cubi dove andranno le finestre e li metto, uno ad uno, in un array
	with open("lines/finestre.lines", "rb") as file:
		reader = csv.reader(file, delimiter=",")
		windowsList = []
		cuboid = []
		acc = 0
		for row in reader:
			acc = acc + 1
			cuboid.append([float(row[0]),float(row[1])])
			if(acc == 4):

				cub=STRUCT([MKPOL([cuboid,[[1,2,3,4]],None])])
				cub = PROD([cub, Q(SIZE([3])(externalWalls)[0]/2.)])
				cub = T(3)(SIZE([3])(externalWalls)[0]/4.)(cub)
				cub = (S([1,2])([xfactor,yfactor])(cub))
				windowsList.append(cub)
				cuboid = []
				acc = 0

	#per ogni cubo mi trovo la corrispettiva finestra e calcolo la dimensione e la posizione 
	dataDim=[]

	for c in windowsList:
		externalWalls2=DIFFERENCE([externalWalls,c])
		window = DIFFERENCE([externalWalls,externalWalls2])
		sizeDoor = SIZE([1,2])(window)
		if (sizeDoor[0] != 0.0 and sizeDoor[1] != 0.0):
			#grandezza finestra
			windowDimension=SIZE([1,2,3])(window)
			#posizione finestra
			c=CUBOID([1,1,1])
			box =STRUCT([c,window])
			box = BOX([1,2,3])(box)
			distanceWindow=SIZE([1,2,3])(box)
			windowPosition=[distanceWindow[0]-windowDimension[0],distanceWindow[1]-windowDimension[1],distanceWindow[2]-windowDimension[2]]
			#inserisco la posizione e la dimensione in un array
			dataDim.append([windowDimension,windowPosition])

	return dataDim
def main():
	#VIEW(ggpl_building_house(19,9))
	print(getDatainternalDoors(19,9))

if __name__ == "__main__":
    main()