from house_structure import *
from tools import *
from windows_and_doors import *
from stair_landings import *
from roof import *


def getDataExternalDoors (dimX,dimY,externalLinesPath,doorsLinesPath):
	#genero i muri esterni
	externalWalls = building_wall(externalLinesPath,6,3)
	#calcolo i fattori di scala x e y 
	xfactor=dimX/SIZE([1])(externalWalls)[0]
	yfactor=dimY/SIZE([2])(externalWalls)[0]
	#ridimensiono
	externalWalls = (S([1,2])([xfactor,yfactor])(externalWalls))
	#creo cubi dove andranno le porte e li metto, uno ad uno, in un array
	with open(doorsLinesPath, "rb") as file:
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
	
def getDatainternalDoors(dimX,dimY,externalLinesPath,internalLinesPath,doorsLinesPath):
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
	with open(doorsLinesPath, "rb") as file:
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

def getDataWindows (dimX,dimY,externalLinesPath,windowsLinesPath):
	#genero i muri esterni
	externalWalls = building_wall(externalLinesPath,6,3)
	#calcolo i fattori di scala x e y 
	xfactor=dimX/SIZE([1])(externalWalls)[0]
	yfactor=dimY/SIZE([2])(externalWalls)[0]
	#ridimensiono
	externalWalls = (S([1,2])([xfactor,yfactor])(externalWalls))
	#creo cubi dove andranno le finestre e li metto, uno ad uno, in un array
	with open(windowsLinesPath, "rb") as file:
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

def getDataStairs(dimX,dimY,externalLinesPath,internalLinesPath,stairsLinesPath):
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
	with open(stairsLinesPath, "rb") as file:
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

def adaptWindow(data):

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

def adaptDoor(data):
	#data=getDataExternalDoors(dimX,dimY,externalLinesPath,doorsLinesPath)
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


def adaptStairs(data):
	#data=getDataStairs(dimX,dimY,externalLinesPath,internalLinesPath,stairsLinesPath)
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

def completeSecondFloor(secondFloorStruct,dataWindows,dataInternalDoor):

	
	secondFloor=STRUCT([secondFloorStruct,adaptWindow(dataWindows),adaptDoor(dataInternalDoor)])
	return secondFloor

def completeFirstFloor(firstFloorStruct, dataWindows, dataExternalDoor, dataInternalDoor, dataStairs):

	firstFloor = STRUCT([firstFloorStruct,adaptWindow(dataWindows),adaptDoor(dataInternalDoor),adaptDoor(dataExternalDoor),adaptStairs(dataStairs)])
	return firstFloor


def roofCreator(firstFloor, secondFloor):


	dim1=getDimensionAndPosition(firstFloor)
	dim2=getDimensionAndPosition(secondFloor)
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

def desingHouse(externalLinesPath,internalLinesPath,externalLinesPathSecond,internalLinesPathSecond):
	def houseElements(windowsLinesPath,doorsLinesPath,stairsLinesPath,windowsLinesPathSecond,doorsLinesPathSecond):
		def setDim(firstX,firstY,secondX,secondY):
			firstFloorStruct = ggpl_building_house(firstX,firstY,externalLinesPath,internalLinesPath,windowsLinesPath,doorsLinesPath)
			secondFloorStruct = ggpl_building_house_second_floor(secondX,secondY,externalLinesPathSecond,internalLinesPathSecond,windowsLinesPathSecond,doorsLinesPathSecond)

			dataWindows1 = getDataWindows(firstX,firstY,externalLinesPath,windowsLinesPath)
			dataExternalDoor1 = getDataExternalDoors(firstX,firstY,externalLinesPath,doorsLinesPath)
			dataInternalDoor1 = getDatainternalDoors(firstX,firstY,externalLinesPath,internalLinesPath,doorsLinesPath)
			dataStairs1 = getDataStairs(firstX,firstY,externalLinesPath,internalLinesPath,stairsLinesPath)
			first =  completeFirstFloor(firstFloorStruct, dataWindows1, dataExternalDoor1, dataInternalDoor1, dataStairs1)
			first = onAxes(first)
			secondFloorStruct = ggpl_building_house_second_floor(secondX,secondY,externalLinesPathSecond,internalLinesPathSecond,windowsLinesPathSecond,doorsLinesPathSecond)
			dataWindows2= getDataWindows(secondX,secondY,externalLinesPathSecond,windowsLinesPathSecond)
			dataInternalDoor2= getDatainternalDoors(secondX,secondY,externalLinesPathSecond,internalLinesPathSecond,doorsLinesPathSecond)
			second = completeSecondFloor(secondFloorStruct,dataWindows2,dataInternalDoor2)
			second = onAxes(second)
			roof = roofCreator(first,second)
			roof = onAxes(roof)
			column = CUBOID([0.3,0.3,3])
			column = TEXTURE(["texture/wall_internal.jpg", FALSE, TRUE, 1, 1, 0, 2, 2])(column)
			VIEW(first)
			house = STRUCT([first,T(3)(3),second])
			VIEW(house)
			house = STRUCT([house,roof])
			house = rotation(house,2)
			house = STRUCT([house,column])
			return house
		return setDim
	return houseElements



def main():


	externalLinesPath= "lines/esterno.lines"
	internalLinesPath= "lines/interno.lines"
	windowsLinesPath ="lines/finestre.lines"
	doorsLinesPath = "lines/porte.lines"
	stairsLinesPath = "lines/scala.lines"

	externalLinesPathSecond= "lines/esterno2.lines"
	internalLinesPathSecond= "lines/interno2.lines"
	windowsLinesPathSecond="lines/finestre2.lines"
	doorsLinesPathSecond = "lines/porte2.lines"


	house = desingHouse(externalLinesPath,internalLinesPath,externalLinesPathSecond,internalLinesPathSecond)(windowsLinesPath,doorsLinesPath,stairsLinesPath,windowsLinesPathSecond,doorsLinesPathSecond)(19,9,16.3,9)


	VIEW(house)

if __name__ == "__main__":
    main()
