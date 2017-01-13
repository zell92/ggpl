from pyplasm import *
import csv

def building_wall(nameLines_path,texture_path,depthWall):
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
	floor = SOLIDIFY(walls)
	xfactor = 15.1/SIZE([1])(walls)[0]
	yfactor = 25/SIZE([2])(walls)[0]
	walls = OFFSET([depthWall,depthWall])(walls)
	walls = PROD([walls, Q(3/xfactor)])
	#creo le porte
	with open("lines/porte.lines", "rb") as file:
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
	doors = PROD([doors, Q(2.5/xfactor)])
	#creo le finestre
	with open("lines/finestre.lines", "rb") as file:
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
	windows = PROD([windows, Q(SIZE([3])(walls)[0]/2.)])
	windows = T(3)(SIZE([3])(walls)[0]/4.)(windows)
	#per ogni muro sottraggo la porta e la finestra e gli applico la texture
	walls=[]

	for w in listWalls:
		w=STRUCT([w])
		w= OFFSET([depthWall,depthWall])(w)
		w=PROD([w,Q(3/xfactor)])
		#w = (S([1,2,3])([xfactor,yfactor, xfactor])(w))
		w=DIFFERENCE([w,windows,doors])
		w=STRUCT([R([2,3])(PI/2),w])
		w=TEXTURE([texture_path, FALSE, TRUE, 1, 1, 0, 2, 2])(w)
		w=STRUCT([R([2,3])(-PI/2),w])
		walls.append(w)
	walls=STRUCT(walls)
	return [walls,xfactor,yfactor]


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
			cuboid.append([float(row[1]),float(row[0])])
			if(acc == 4):
				floorList.append(MKPOL([cuboid,[[1,2,3,4]],None]))
				cuboid = []
				acc = 0
	floor = STRUCT(floorList)
	return floor



def ggpl_building_house():
	"""
	ggpl_building_house is a function that generate the HPC Model represent the house structure by the input file in .lines files.
	@return house: HPC Model represent the structure.
	"""
	external=building_wall("lines/esterno.lines","texture/wall_external.jpg",14)
	internal= building_wall("lines/interno.lines","texture/wall_internal.jpg",7)

	#muri esterni
	externalWalls=external[0]
	#muri interni
	internalWalls=internal[0]
	#fattori di scala x e y
	xfactor=external[1]
	yfactor=external[2]

	#casa senza pavimenti
	house=STRUCT([externalWalls,internalWalls])
	#ridimensiono la casa	
	#house = (S([1,2,3])([xfactor,yfactor, xfactor])(house))

	#pavimento bagno
	bathFloor=building_floor("lines/bagno.lines")
	bathFloor=TEXTURE(["texture/bath.jpg", TRUE, FALSE, 1, 1, 0, 12, 12])(bathFloor)
	#pavimento box
	boxFloor=building_floor("lines/box.lines")
	boxFloor=TEXTURE(["texture/box.jpg", TRUE, FALSE, 1, 1, 0, 2, 2])(boxFloor)
	#pavimento camere
	bedroomFloor=building_floor("lines/camere.lines")
	bedroomFloor=TEXTURE(["texture/bedroom.jpg", TRUE, FALSE, 1, 1, 0, 2, 2])(bedroomFloor)
	#pavimento resto della casa
	otherFloor=building_floor("lines/parquet.lines")
	otherFloor=TEXTURE(["texture/parquet.jpg", TRUE, FALSE, 1, 1, 0, 2, 2])(otherFloor)

	#pavimento totale
	floor=STRUCT([bathFloor,boxFloor,bedroomFloor,otherFloor])
	#ridimensiono il pavimento
	floor=(S([1,2,3])([xfactor,yfactor, xfactor])(floor))

	#casa con pavimento
	house=STRUCT([house,floor])

	#aggiusto la casa rispetto gli assi
	#house=STRUCT([R([1,2])(-PI/2),house])
	#house=STRUCT([T([2])(SIZE(2)(house)),house])

	return house


VIEW(ggpl_building_house())