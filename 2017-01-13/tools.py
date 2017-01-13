from pyplasm import *
from fpformat import *

def color(r,g,b):
    """This function return a rgb Color"""
    return [float(fix(r/255.,6)),float(fix(g/255.,6)),float(fix(b/255.,6)),1.000000]
def rotation(HTCObject,dir):
	"""
	rotation is a function that generate a perfect rotation of HPC Model
	@input HTCObject: the object that you want to rotate
	@input dir: rotate on the left 90 degrees if dir = 1, 180 if dir = 2, 270 if dir=3 and 360 if dir = 4
	@return house: HPC Model represent the structure.
	"""
	if(dir>0 and dir < 4):

		c = CUBOID([0.1,0.1,0.1])
		sizeObj = SIZE([1,2])(HTCObject)
		box = STRUCT([c,HTCObject])
		box = BOX([1,2,3])(box)
		distance=SIZE([1,2,3])(box)
		position=[distance[0]-sizeObj[0],distance[1]-sizeObj[1]]

		elem=STRUCT([T([1,2])([-position[0],-position[1]]),HTCObject])
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

	return HTCObject


