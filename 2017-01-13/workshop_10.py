from house_structure import *
from tools import *
from windows_and_doors import *
from stair_landings import *
from roof import *


def getDataExternalDoors (dimX,dimY,externalLinesPath,doorsLinePath):
	#genero i muri esterni
	externalWalls = building_wall(externalLinesPath,6,3)
	#calcolo i fattori di scala x e y 
	xfactor=dimX/SIZE([1])(externalWalls)[0]
	yfactor=dimY/SIZE([2])(externalWalls)[0]
	#ridimensiono
	externalWalls = (S([1,2])([xfactor,yfactor])(externalWalls))
	#creo cubi dove andranno le porte e li metto, uno ad uno, in un array
	with open(doorsLinePath, "rb") as file:
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
			#calcolo la posizione e la dimensione delle porte esterne
			dataDim.append(getDimensionAndPosition(door))

	return dataDim
	
def getDatainternalDoors(dimX,dimY,externalLinesPath,internalLinesPath,doorsLinePath):
	#genero i muri interni
	externalWalls = building_wall(externalLinesPath,6,3)
	internalWalls = building_wall(internalLinesPath,3,3)
	internalWalls = STRUCT([externalWalls,internalWalls])
	#calcolo i fattori di scala x e y 
	xfactor=dimX/SIZE([1])(internalWalls)[0]
	yfactor=dimY/SIZE([2])(internalWalls)[0]
	#ridimensiono
	internalWalls = (S([1,2])([xfactor,yfactor])(internalWalls))
	externalWalls = (S([1,2])([xfactor,yfactor])(externalWalls))
	internalWalls=DIFFERENCE([internalWalls,externalWalls])
	#creo cubi dove andranno le porte e li metto, uno ad uno, in un array
	with open(doorsLinePath, "rb") as file:
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
			#calcolo la posizione e la dimensione delle porte interne
			dataDim.append(getDimensionAndPosition(door))

	return dataDim

from house_structure import *

def getDataWindows (dimX,dimY,externalLinesPath,windowsLinePath):
	#genero i muri esterni
	externalWalls = building_wall(externalLinesPath,6,3)
	#calcolo i fattori di scala x e y 
	xfactor=dimX/SIZE([1])(externalWalls)[0]
	yfactor=dimY/SIZE([2])(externalWalls)[0]
	#ridimensiono
	externalWalls = (S([1,2])([xfactor,yfactor])(externalWalls))
	#creo cubi dove andranno le finestre e li metto, uno ad uno, in un array
	with open(windowsLinePath, "rb") as file:
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
			#calcolo la posizione e la dimensione delle finestre
			dataDim.append(getDimensionAndPosition(window))


	return dataDim

def getDataStairs(dimX,dimY,externalLinesPath,internalLinesPath,stairsLinePath):
	#genero tutti i muri della casa
	externalWalls = building_wall(externalLinesPath,6,3)
	internalWalls = building_wall(internalLinesPath,3,3)
	internalWalls = STRUCT([externalWalls,internalWalls])
	#calcolo i fattori di scala x e y 
	xfactor=dimX/SIZE([1])(internalWalls)[0]
	yfactor=dimY/SIZE([2])(internalWalls)[0]
	#ridimensiono
	walls = (S([1,2])([xfactor,yfactor])(internalWalls))
	#creo cubi dove andranno le scale
	with open(stairsLinePath, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		doorsList = []
		cuboid = []
		acc = 0
		for row in reader:
			acc = acc + 1
			cuboid.append([float(row[0]),float(row[1])])
			if(acc == 4):
				cub=STRUCT([MKPOL([cuboid,[[1,2,3,4]],None])])
				cub = PROD([cub, Q(3)])
				cub = (S([1,2])([xfactor,yfactor])(cub))
				doorsList.append(cub)
				cuboid = []
				acc = 0

	#per ogni cubo mi trovo la posizione e dimensione esatta delle scale
	dataDim=[]

	for c in doorsList:
		stair=DIFFERENCE([c,walls])
		sizeStair = SIZE([1,2])(stair)
		if (sizeStair[0] != 0.0 and sizeStair[1] != 0.0):
			#calcolo la posizione e la dimensione delle scale
			dataDim.append(getDimensionAndPosition(stair))

	return dataDim

from house_structure import *

def adaptWindow(dimX,dimY,externalLinesPath,windowsLinePath):
    data=getDataWindows(dimX,dimY,externalLinesPath,windowsLinePath)
    windows=[]
    for d in data:
        print(d[0])
        if d[0][0]>d[0][1]:
            w=createWindow(d[0][0],d[0][1],d[0][2])
            w=rotation(w,2)
        else:
            w=createWindow(d[0][1],d[0][0],d[0][2])
            w=rotation(w,1)
            
        w=STRUCT([T([1,2,3])(d[1]),w])
        windows.append(w)

    return STRUCT(windows)

def adaptExternalDoor(dimX,dimY,externalLinesPath,doorsLinePath):
	data=getDataExternalDoors(dimX,dimY,externalLinesPath,doorsLinePath)
	doors=[]
	for d in data:
		if d[0][0]>d[0][1]:
			if d[0][0]>=1.5:
				door=createDubleDoor(d[0][0],d[0][1],d[0][2],color(255,255,255))
			else:
				door=createSingleDoor(d[0][0],d[0][1],d[0][2],color(255,255,255))
			door=rotation(door,2)
		else:
			if d[0][1]>=1.5:
				door=createDubleDoor(d[0][0],d[0][1],d[0][2],color(255,255,255))
			else:
				door=createSingleDoor(d[0][0],d[0][1],d[0][2],color(255,255,255))
			door=rotation(door,1)
			
		door=STRUCT([T([1,2,3])(d[1]),door])
		doors.append(door)

	return STRUCT(doors)

def adaptInternalDoor(dimX,dimY,externalLinesPath,internalLinesPath,doorsLinePath):
	data=getDatainternalDoors(dimX,dimY,externalLinesPath,internalLinesPath,doorsLinePath)
	doors=[]
	for d in data:
		if d[0][0]>d[0][1]:
			if d[0][0]>=1.5:
				door=createDubleDoor(d[0][0],d[0][1],d[0][2],color(102,51,0))
			else:
				door=createSingleDoor(d[0][0],d[0][1],d[0][2],color(102,51,0))
			door=rotation(door,2)
		else:
			if d[0][1]>=1.5:
				door=createDubleDoor(d[0][1],d[0][0],d[0][2],color(102,51,0))
			else:
				door=createSingleDoor(d[0][1],d[0][0],d[0][2],color(102,51,0))
			door=rotation(door,1)
		door=STRUCT([T([1,2,3])(d[1]),door])
		doors.append(door)


	return STRUCT(doors)

def adaptStairs(dimX,dimY,externalLinesPath,internalLinesPath,stairsLinePath):
	data=getDataStairs(dimX,dimY,externalLinesPath,internalLinesPath,stairsLinePath)
	stairs = []
	for d in data:
		if d[0][0]>d[0][1]:
			stair=ggpl_stair_landings(d[0][1],d[0][0],d[0][2])
			stair=rotation(stair,3)
		else:
			stair=ggpl_stair_landings(d[0][0],d[0][1],d[0][2])
			stair=rotation(stair,4)
		stair=STRUCT([T([1,2,3])(d[1]),stair])
		stairs.append(stair)


	return STRUCT(stairs)

def completeSecondFloor(dx,dy,externalLinesPath,internalLinesPath,windowsLinePath,doorsLinePath):
	secondFloor= ggpl_building_house_second_floor(dx,dy)
	secondFloor=STRUCT([secondFloor,adaptWindow(dx,dy,externalLinesPath,windowsLinePath),adaptInternalDoor(dx,dy,externalLinesPath,internalLinesPath,doorsLinePath)])
	return secondFloor
def completeFirstFloor(dx,dy,externalLinesPath,internalLinesPath,windowsLinePath,doorsLinePath,stairsLinePath):
	house = ggpl_building_house(dx,dy)
	house=STRUCT([house,adaptWindow(dx,dy,externalLinesPath,windowsLinePath),adaptInternalDoor(dx,dy,externalLinesPath,internalLinesPath,doorsLinePath),adaptExternalDoor(dx,dy,externalLinesPath,doorsLinePath),adaptStairs(dx,dy,externalLinesPath,internalLinesPath,stairsLinePath)])
	return house

def buildingCompleteHouse():
	def completeFloors(dx,dy,rotate):
		""""def completeFirstFloor(externalLinesPath,internalLinesPath,windowsLinePath,doorsLinePath,stairsLinePath):
			house = ggpl_building_house(dx,dy)
			house=STRUCT([house,adaptWindow(dx,dy,externalLinesPath,windowsLinePath),adaptInternalDoor(dx,dy,externalLinesPath,internalLinesPath,doorsLinePath),adaptExternalDoor(dx,dy,externalLinesPath,doorsLinePath),adaptStairs(dx,dy,externalLinesPath,internalLinesPath,stairsLinePath)])
			house=onAxes(house)
			house = rotation(house,rotate)
			return house"""
		def completeSecondFloor(externalLinesPath,internalLinesPath,windowsLinePath,doorsLinePath):
			secondFloor= ggpl_building_house_second_floor(dx,dy)
			secondFloor=STRUCT([secondFloor,adaptWindow(dx,dy,externalLinesPath,windowsLinePath),adaptInternalDoor(dx,dy,externalLinesPath,internalLinesPath,doorsLinePath)])
			secondFloor = rotation(secondFloor,rotate)
			return secondFloor

		return completeSecondFloor
	return completeFloors
def roofCreator(dx1,dy1,dx2,dy2):

	house = ggpl_building_house(dx1,dy1)
	house2 = ggpl_building_house_second_floor(dx2,dy2)
	dim1=getDimensionAndPosition(house)
	dim2=getDimensionAndPosition(house2)
	dim=[[dim1[0][0]-dim2[0][0],9,0],[dim2[1][0]+dim2[0][0],dim2[1][1],0]]

	punti=[]
	punti.append([dim[1][0],dim[1][1]])
	punti.append([dim[1][0],dim[1][1]+dim[0][1]])
	punti.append([dim[0][0]+dim[1][0],dim[0][1]+dim[1][1]])
	punti.append([dim[1][0]+dim[0][0],dim[1][1]])
	#print(punti)

	altezza=getMinDistPitch(punti)/2
	tetto=createRoof(punti,PI/5,altezza)

	punti=[]
	punti.append([dim2[1][0],dim2[1][1]])
	punti.append([dim2[1][0],dim2[1][1]+dim2[0][1]])
	punti.append([dim2[0][0]+dim2[1][0],dim2[0][1]+dim2[1][1]])
	punti.append([dim2[1][0]+dim2[0][0],dim2[1][1]])
	#print(punti)

	altezza2=getMinDistPitch(punti)/2
	tetto2=createRoof(punti,PI/5,altezza2)
	
	roof = STRUCT([tetto,T(3)(3),tetto2])
	roof = STRUCT([T(3)(3),roof])
	return roof

def main():
	#house = buildingCompleteHouse()(19,9,2)("lines/esterno.lines","lines/interno.lines","lines/finestre.lines", "lines/porte.lines", "lines/scala.lines")("lines/esterno2.lines","lines/interno2.lines","lines/finestre2.lines", "lines/porte2.lines")
	#house = buildingCompleteHouse()(19,9,2)("lines/esterno2.lines","lines/interno2.lines","lines/finestre2.lines", "lines/porte2.lines")
	first =  completeFirstFloor(19,9,"lines/esterno.lines","lines/interno.lines","lines/finestre.lines", "lines/porte.lines", "lines/scala.lines")
	first = onAxes(first)
	second = completeSecondFloor(16.3,9,"lines/esterno2.lines","lines/interno2.lines","lines/finestre2.lines", "lines/porte2.lines")
	#dimSecondFloor= getProportionalDimension(first,second,19,9)
	#second=resize(second,dimSecondFloor[0],dimSecondFloor[1],3)
	second = onAxes(second)
	roof = roofCreator(19,9,16.3,9)
	roof = onAxes(roof)
	column = CUBOID([0.3,0.3,3])
	column = TEXTURE(["texture/wall_internal.jpg", FALSE, TRUE, 1, 1, 0, 2, 2])(column)
	VIEW(first)
	house = STRUCT([first,T(3)(3),second])
	VIEW(house)
	house = STRUCT([house,roof])
	house = rotation(house,2)
	house = STRUCT([house,column])
	VIEW(house)

if __name__ == "__main__":
    main()
