from pyplasm import *
from fpformat import *

def color(r,g,b):
    """This function return a rgb Color"""
    return [float(fix(r/255.,6)),float(fix(g/255.,6)),float(fix(b/255.,6)),1.000000]
def rotation(HPCObject,dir):
	"""
	rotation is a function that generate a perfect rotation of HPC Model
	@input HPCObject: the object that you want to rotate
	@input dir: rotate on the left 90 degrees if dir = 1, 180 if dir = 2, 270 if dir=3 and 360 if dir = 4
	@return house: HPC Model represent the structure.
	"""
	if(dir>0 and dir < 4):

		c = CUBOID([0.1,0.1,0.1])
		sizeObj = SIZE([1,2])(HPCObject)
		box = STRUCT([c,HPCObject])
		box = BOX([1,2,3])(box)
		distance=SIZE([1,2,3])(box)
		position=[distance[0]-sizeObj[0],distance[1]-sizeObj[1]]

		elem=STRUCT([T([1,2])([-position[0],-position[1]]),HPCObject])
		if dir==1:
			elem=STRUCT([R([1,2])(PI/2),elem])
			elem=STRUCT([T([1])(sizeObj[1]),elem])
			elem=STRUCT([T([1,2])([position[0],position[1]]),elem])
		if dir==2:
			elem=STRUCT([R([1,2])(PI),elem])
			elem=STRUCT([T([1,2])([sizeObj[0],sizeObj[1]]),elem])
			elem=STRUCT([T([1,2])([position[0],position[1]]),elem])
		if dir==3:
			elem=STRUCT([R([1,2])(PI*3/2),elem])
			elem=STRUCT([T([2])(sizeObj[0]),elem])
			elem=STRUCT([T([1,2])([position[0],position[1]]),elem])
		if dir==4:
			elem=STRUCT([R([1,2])(PI*2),elem])
		return elem

	return HPCObject
def onAxes (HPCObject):
	"""
	onAxys is a function that translates an HPC object, placing it exactly on the Cartesian axes
	@input HPCObject: the object that you want to translate
	@return obj: HPC Model represent the transalted structure.
	"""
	c = CUBOID([0.1,0.1,0.1])
	sizeObj = SIZE([1,2])(HPCObject)
	box = STRUCT([c,HPCObject])
	box = BOX([1,2,3])(box)
	distance=SIZE([1,2,3])(box)
	position=[distance[0]-sizeObj[0],distance[1]-sizeObj[1]]
	obj=STRUCT([T([1,2])([-position[0],-position[1]]),HPCObject])
	return obj
def getDimensionAndPosition(HPCObject):
	"""
	getPositionAndDimension is a function that return (in a list) the dimension and position of an HPCObject
	@input HPCObject: the object that you want to examine.
	@return dimAndPos: an array of length 2 containing the dimension and position (x, y, z) of the object examined
	"""
	sizeObj = SIZE([1,2,3])(HPCObject)

	c = CUBOID([0.1,0.1,0.1])	
	box = STRUCT([c,HPCObject])
	box = BOX([1,2,3])(box)
	distance=SIZE([1,2,3])(box)
	position=[distance[0]-sizeObj[0],distance[1]-sizeObj[1],distance[2]-sizeObj[2]]

	dimAndPos=[sizeObj,position]

	return dimAndPos

def resize(HPCObject,x,y,z):
	"""
	resize is a function that resize an HPCObject
	@input HPCObject: the object that you want to resize.
	@input x,y,z: the size that you want.
	@return resizeObj: the object resizes
	"""
	dim = getDimensionAndPosition(HPCObject)[0]
	sX = x/dim[0]
	sY = y/dim[1]
	sZ = z/dim[2]
	resizeObj = STRUCT([S([1,2,3])([sX,sY,sZ]),HPCObject])
	return resizeObj

def getProportionalDimension(HPCObject1,HPCObject2,x,y):
	xfactor=x/SIZE([1])(HPCObject1)[0]
	yfactor=y/SIZE([2])(HPCObject1)[0]
	newX=SIZE([1])(HPCObject2)[0]*xfactor
	newY=SIZE([2])(HPCObject2)[0]*xfactor
	return [newX,newY]



def main():
	VIEW(ggpl_building_house(19,9))
if __name__ == "__main__":
    main()




