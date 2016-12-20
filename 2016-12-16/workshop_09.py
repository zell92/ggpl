from pyplasm import *
from scipy import *  
from numpy import *  
import math
import csv

def createRoof(pathFileLines,angle,diagonal):
	"""
	createRoof ritorna l'HPC di un tetto secondo 3 parametri: un file .lines che descrive il perimetro della base del tetto, i gradi della pendenza delle falde, 
	la lunghezza della pendenza delle falde
	@param pathFileLines: stringa che identifica la posizione del file .lines
	@param angle: l'angolo di inclinazione che si vuole dare alla falda
	@param diagonal: lunghezza della pendenza della falda
	@return struttura: l'HPC del tetto
	"""
	vertexes=getVertexes(pathFileLines)
	directions=getDirections(vertexes)

	falde = []
	for i in range(len(directions)):
		if i==len(directions)-1:
			falde.append(createPitch(vertexes[i],vertexes[0],angle,diagonal,directions[i]))
		else:
			s = i+1
			falde.append(createPitch(vertexes[i],vertexes[s],angle,diagonal,directions[i]))

	rette = []
	for i in range(len(falde)):
		rette.append(lineFrom2Points(falde[i][2],falde[i][3]))

	intersezioni = []
	for i in range(len(rette)):
		if i==len(rette)-1:
			intersezioni.append(linesIntersection(rette[i],rette[0]))
			intersezioni.append(linesIntersection(rette[i],rette[0]))
		else:
			s = i+1
			intersezioni.append(linesIntersection(rette[i],rette[s]))


	faldeFinali = []
	for i in range(len(directions)):
		if i == 0:
			f = MKPOL([[[falde[i][0][0],falde[i][0][1],0],[falde[i][1][0],falde[i][1][1],0],[intersezioni[i][0],intersezioni[i][1],falde[1][2][2]],[intersezioni[len(directions)-1][0],intersezioni[len(directions)-1][1],falde[0][2][2]]],[[1,2,3,4]],None])
			f = TEXTURE("tegole.jpg")(f)
			faldeFinali.append(f)
		else:
			f = MKPOL([[[falde[i][0][0],falde[i][0][1],0],[falde[i][1][0],falde[i][1][1],0],[intersezioni[i][0],intersezioni[i][1],falde[1][2][2]],[intersezioni[i-1][0],intersezioni[i-1][1],falde[0][2][2]]],[[1,2,3,4]],None])
			f = TEXTURE("tegole.jpg")(f)
			faldeFinali.append(f)

	vertexesContorno = [[] for _ in range(len(intersezioni)+1)]
	cella = []
	for i in range (len(intersezioni)):
		vertexesContorno[i].append(intersezioni[i][0])
		vertexesContorno[i].append(intersezioni[i][1])
		s = i+1
		if i==len(intersezioni)-1:
			vertexesContorno[s].append(intersezioni[0][0])
			vertexesContorno[s].append(intersezioni[0][1])
		cella.append(s)

	contorno = POLYLINE(vertexesContorno)
	contorno = SOLIDIFY(contorno)

	terrazzo = T(3)(falde[0][2][2])(contorno)
	terrazzo = TEXTURE("pavimento.jpg")(terrazzo)

	tetto = STRUCT(faldeFinali)
	return STRUCT([terrazzo,tetto])






def createPitch(vert1, vert2, angle, diagonal, direction):
	"""
	createPitch ritorna i 4 vertici del piano che giace sulla falda
	@param vert1: lista delle coordinate xyz del vertice1
	@param vert2: lista delle coordinate xyz del vertice2
	@param angle: l'angle di inclinazione che si vuole dare alla falda
	@param diagonal: lunghezza della pendenza della falda
	@param direction: indica in quale quadrante (di un ipotetico piano cartesiano) 1,2,3 o 4 va direzionata la falda
	@return vertexes: i quattro vertici della falda
	"""
	linea = MKPOL([[vert1,vert2],[[1,2]],None])

	if vert1[1]>vert2[1]:
		x=vert1[0]
		y=vert2[1]
	else:
		x=vert2[0]
		y=vert1[1]

	vert3 = [x,y,0]

	#AB = sqrt[(x2- x1)^2 + (y2- y1)^2]
	distv1v2 = sqrt((vert1[0]-vert2[0])*(vert1[0]-vert2[0])+(vert1[1]-vert2[1])*(vert1[1]-vert2[1]))
	distv1v3 = sqrt((vert1[0]-vert3[0])*(vert1[0]-vert3[0])+(vert1[1]-vert3[1])*(vert1[1]-vert3[1]))
	distv2v3 = sqrt((vert2[0]-vert3[0])*(vert2[0]-vert3[0])+(vert2[1]-vert3[1])*(vert2[1]-vert3[1]))
	
	#distv2v3 = distv1v2 * math.cos(a)
	#math.cos(a) = distv2v3/distv1v2
	a = math.asin(distv2v3/distv1v2)


	b = PI/2-a


	distv2v4 = diagonal * math.cos(angle)

	hPerpendicularPitch = sqrt(diagonal*diagonal-distv2v4*distv2v4)
	distv2v5 = distv2v4 * math.cos(b)
	distv4v5 = sqrt(distv2v4*distv2v4-distv2v5*distv2v5)

	if direction==1:
		vert6 = [vert2[0]+distv2v5,vert2[1]+distv4v5,hPerpendicularPitch]
		vert7 = [vert1[0]+distv2v5,vert1[1]+distv4v5,hPerpendicularPitch]
	elif direction==2:
		vert6 = [vert2[0]-distv2v5,vert2[1]+distv4v5,hPerpendicularPitch]
		vert7 = [vert1[0]-distv2v5,vert1[1]+distv4v5,hPerpendicularPitch]
	elif direction==3:
		vert6 = [vert2[0]-distv2v5,vert2[1]-distv4v5,hPerpendicularPitch]
		vert7 = [vert1[0]-distv2v5,vert1[1]-distv4v5,hPerpendicularPitch]
	elif direction==4:
		vert6 = [vert2[0]+distv2v5,vert2[1]-distv4v5,hPerpendicularPitch]
		vert7 = [vert1[0]+distv2v5,vert1[1]-distv4v5,hPerpendicularPitch]

	vertexes = [vert1,vert2,vert6,vert7]

	return vertexes



def lineFrom2Points(vert1,vert2):
	"""
	lineFrom2Points ritorna la retta dati come input due vertici
	@param vert1: lista delle coordinate xy del vertice1 
	@param vert2: lista delle coordinate xy del vertice2 
	@return line: ritorna la retta (una lista di tre elementi) secondo il seguente schema x + y = n --> [x,y,n]
	"""

	x1=vert1[0]
	x2=vert2[0]
	y1=vert1[1]
	y2=vert2[1]
	m=0
	q=0

	# Se i due punti hanno la stessa ascissa, la retta che li comprende e' parallela all'asse y
	# Se i due punti hanno la stessa ordinata, la retta che li comprende e' parallela all'asse x
	if x1==x2:
		line = [1,0,x1]
	elif y1==y2:
		line = [0,1,y1]
	else:
		m=(float(y2)-float(y1))/(float(x2)-float(x1))
		q=float(y1)-m*float(x1)
		line = [-m,1,q]

	return line


	
def linesIntersection(line1,line2):
	"""
	linesIntersection ritorna il punto di intersezione di due rette
	@param line1: e' la retta definita secondo le regole del metodo lineFrom2Points
	@param line2: e' la retta definita secondo le regole del metodo lineFrom2Points
	@return point: ritorna il punto x y dell'intersezione
	"""
	  
	# La matrice A contiene i coefficenti (a sinistra del simbolo di uguale).  
	A = matrix([[line1[0], line1[1]], [line2[0], line2[1]]])  
	
	# l'array b contiene i valori noti  
	b = array([line1[2], line2[2]])  
	  
	# la funzione linalg.solve risolve sistemi lineari
	point = linalg.solve(A, b)  
	return point


def getDirections(vertexes):
	directions=[]
	for i in range(1,len(vertexes)):
		x1=vertexes[i-1][0]
		x2=vertexes[i][0]
		y1=vertexes[i-1][1]
		y2=vertexes[i][1]
		if x2>=x1:
			if y2>=y1:
				directions.append(4)
			else:
				directions.append(3)
		else:
			if y2>=y1:
				directions.append(1)
			else:
				directions.append(2)
	return directions

def getVertexes(pathFileLines):
	with open(pathFileLines, "rb") as file:
		reader = csv.reader(file, delimiter=",")
		vertexes=[]
		for row in reader:
			vertexes.append([float(row[0]),float(row[1])])
			vertexes.append([float(row[2]),float(row[3])])

		vertexes2=[]
		for i in range(len(vertexes)):
			if i%2==0:
				vertexes2.append(vertexes[i])
			if i==len(vertexes)-3:
				vertexes2.append(vertexes[i])

	copy = vertexes2[len(vertexes2)-2]



	return vertexes2      



VIEW(createRoof("border.lines",PI/4,60))
