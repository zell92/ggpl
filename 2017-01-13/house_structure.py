from pyplasm import *
import csv
def building_wall(nameLines_path,depthWall,dimZ):
	"""
	building_house is a function that generate the HPC Model represent the wall structure by the input file in .lines files.
	@input nameLines_path,texture_path,depthWall: path of .lines file, path of texture image, depth of the wall structure.
	@return [walls,xfactor,yfactor]: HPC Model represent the structure, the factors for scaling the structure in x and y.
	"""

	#creo i muri
	with open(nameLines_path, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		listWalls = []
		for row in reader:
			listWalls.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))

	walls = STRUCT(listWalls)

	walls = OFFSET([depthWall,depthWall])(walls)
	walls = PROD([walls, Q(dimZ)])
	return walls

def building_doors(wall,linesPath,texture_path): #altezza predefinita 2,5m
	#creo le porte
	with open(linesPath, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		doorsList = []
		cuboid = []
		acc = 0
		for row in reader:
			acc = acc + 1
			cuboid.append([float(row[0]),float(row[1])])
			if(acc == 4):
				doorsList.append(MKPOL([cuboid,[[1,2,3,4]],None]))
				cuboid = []
				acc = 0
	doors = STRUCT(doorsList)
	doors = PROD([doors, Q(2.5)])
	d=DIFFERENCE([wall,doors])
	d=TEXTURE([texture_path, FALSE, TRUE, 1, 1, 0, 2, 2])(d)

	return d

def building_floor(nameLines_path):
	"""
	building_floor is a function that generate the HPC Model represent the floor structure by the input file in .lines files.
	@input nameLines_path: path of .lines file.
	@return floor: HPC Model represent the structure.
	"""
	#creo i pavimenti
	with open(nameLines_path, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		floorList = []
		cuboid = []
		acc = 0
		for row in reader:
			acc = acc + 1
			cuboid.append([float(row[0]),float(row[1])])
			if(acc == 4):
				floorList.append(MKPOL([cuboid,[[1,2,3,4]],None]))
				cuboid = []
				acc = 0
	floor = STRUCT(floorList)
	return floor


def building_windows(wall,linesPath): #altezza dal suolo predefinita meta' muro

	#creo le finestre
	with open(linesPath, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		windowList = []
		cuboid = []
		acc = 0
		for row in reader:
			acc = acc + 1
			cuboid.append([float(row[0]),float(row[1])])
			if(acc == 4):
				windowList.append(MKPOL([cuboid,[[1,2,3,4]],None]))
				cuboid = []
				acc = 0
	windows = STRUCT(windowList)
	windows = PROD([windows, Q(SIZE([3])(wall)[0]/2.)])
	windows = T(3)(SIZE([3])(wall)[0]/4.)(windows)
	#per ogni muro sottraggo la porta e la finestra e gli applico la texture
	w=DIFFERENCE([wall,windows])
	return w


def ggpl_building_house(dimX,dimY,externalLinesPath,internalLinesPath,windowsLinesPath,doorsLinesPath):
	"""
	ggpl_building_house is a function that generate the HPC Model represent the house structure by the input file in .lines files.
	@return house: HPC Model represent the structure.
	"""
	#costruzione muri
	externalWalls=building_wall(externalLinesPath,6,3)
	internalWalls= building_wall(internalLinesPath,3,3)

	#costruzione porte e finestre
	externalWalls = building_windows(externalWalls,windowsLinesPath)
	externalWalls = building_doors(externalWalls,doorsLinesPath,"texture/wall_internal.jpg")	
	internalWalls = building_doors(internalWalls,doorsLinesPath,"texture/wall_internal.jpg")


	#casa senza pavimenti
	house=STRUCT([externalWalls,internalWalls])
	

	#pavimento bagno
	bathFloor=building_floor("lines/bagno.lines")
	bathFloor=TEXTURE(["texture/bath.jpg", TRUE, FALSE, 1, 1, 0, 6, 6])(bathFloor)

	#pavimento cucina
	kitchenFloor=building_floor("lines/cucina.lines")
	kitchenFloor=TEXTURE(["texture/cucina.jpg", TRUE, FALSE, 1, 1, 0, 6, 3])(kitchenFloor)
	#pavimento resto della casa
	otherFloor=building_floor("lines/parquet.lines")
	otherFloor=TEXTURE(["texture/parquet.jpg", TRUE, FALSE, 1, 1, 0, 2, 2])(otherFloor)

	#pavimento totale
	floor=STRUCT([bathFloor,kitchenFloor,otherFloor])

	#casa con pavimento
	house=STRUCT([house,floor])

	#fattori di scala x e y
	xfactor=dimX/SIZE([1])(house)[0]
	yfactor=dimY/SIZE([2])(house)[0]

	#ridimensiono
	house = (S([1,2])([xfactor,yfactor])(house))
	

	return house

def ggpl_building_house_second_floor(dimX,dimY,externalLinesPath,internalLinesPath,windowsLinesPath,doorsLinesPath):
	"""
	ggpl_building_house_second_floor is a function that generate the HPC Model represent the second floor structure of the house by the input file in .lines files.
	@return house: HPC Model represent the structure.
	"""
	#costruzione muri
	externalWalls=building_wall(externalLinesPath,6,3)
	internalWalls= building_wall(internalLinesPath,3,3)

	#costruzione porte e finestre
	externalWalls = building_windows(externalWalls,windowsLinesPath)
	externalWalls = building_doors(externalWalls,doorsLinesPath,"texture/wall_internal.jpg")	
	internalWalls = building_doors(internalWalls,doorsLinesPath,"texture/wall_internal.jpg")


	#casa senza pavimenti
	house=STRUCT([externalWalls,internalWalls])
	

	#pavimento bagno
	bathFloor=building_floor("lines/bagno2.lines")
	bathFloor=TEXTURE(["texture/bath.jpg", TRUE, FALSE, 1, 1, 0, 14, 6])(bathFloor)

	#pavimento resto della casa
	otherFloor=building_floor("lines/parquet2.lines")
	otherFloor=TEXTURE(["texture/parquet.jpg", TRUE, FALSE, 1, 1, 0, 2, 2])(otherFloor)

	#pavimento totale
	floor=STRUCT([bathFloor,otherFloor])

	#casa con pavimento
	house=STRUCT([house,floor])

	#fattori di scala x e y
	xfactor=dimX/SIZE([1])(house)[0]
	yfactor=dimY/SIZE([2])(house)[0]

	#ridimensiono
	house = (S([1,2])([xfactor,yfactor])(house))
	#traslo in alto
	#house = STRUCT([T([3])(3),house])
	

	return house


def main():
	externalLinesPath="lines/esterno2.lines"
	internalLinesPath="lines/interno2.lines"
	windowsLinesPath = "lines/finestre2.lines"
	doorsLinesPath = "lines/porte2.lines"
	VIEW(ggpl_building_house_second_floor(19,9,externalLinesPath,internalLinesPath,windowsLinesPath,doorsLinesPath))
if __name__ == "__main__":
    main()

