from pyplasm import *
from workshop_10 import *

def getStreet(controls):
	"""
	getStreet is a function that generate the HPC Model rapresenting the street described by some points in the list in input.
	@input controls: some points of the street.
	@return street: HPC Model rapresenting the street.
	"""
	bezier = MAP( BEZIER(S1)(controls) )(INTERVALS(1)(332))
	street=bezier
	street = STRUCT([OFFSET([0.2,0.2])(bezier)])
	return street

def getAlleyway(controls):
	"""
	getAlleyway is a function that generate the HPC Model rapresenting the alleyway described by some points in the list in input.
	@input controls: some points of the alleyway.
	@return street: HPC Model rapresenting the alleyway.
	"""
	bezier = MAP( BEZIER(S1)(controls) )(INTERVALS(1)(2))
	street=bezier
	street = STRUCT([OFFSET([0.1,0.1])(bezier)])
	return street

def createStreet():
	"""
	createStreet is a function that generate the HPC Model rapresenting the streets in the model.
	@return s: HPC Model rapresenting the streets.
	"""
	strada1 = getStreet([[0,5],[2,5.5]])
	strada2 = getStreet([[2,3.5],[2,5.5],[2,7.5],[4,9],[4.5,10], [5.5,11]])
	strada3 = getStreet([[3,7.5],[5,6],[6,8.5],[7,11.5],[7.5,10],[8.5,7],[9.5,6],[10.5,7],[11,7],[13,6.8],[14,6.5],[15.5,5.5],[16,4.5],[16.5,3.5],[16.5,1],[15.5,0]])
	strada4 = getStreet([[14,5.8],[15,7],[17,7.5],[17.5,7.8],[18,8],[18,9],[21,9],[21.5,12]])
	strada5 = getStreet([[15.2,5],[16,5.5],[16,6],[16.7,7.4]])
	strada6 = getStreet([[4.5,7.2],[5.2,6],[5,5.5],[5.5,5],[8.7,7.8]])
	strada7 = getStreet([[16,1],[15.4,1.2]])
	parking = CUBOID([4,1.8,0])
	parking = rotationAngle(parking,PI/1.1)

	vicolo1 = getAlleyway([[16.7,7.4],[15.7,9]])
	vicolo2 = getAlleyway([[8.7,7.8],[9.5,10]])
	vicolo3 = getAlleyway([[12,6.8],[12.5,9]])
	vicolo4 = getAlleyway([[16.7,7.4],[18,5.5]])
	vicolo5 = getAlleyway([[19.5,9.2],[20.2,8]])
	vicolo6 = getAlleyway([[12,6.8],[11,4]])
	vicolo7 = getAlleyway([[16,3.5],[17.4,3.5]])

	c=color(160,160,160)
	r=c[0]
	g=c[1]
	b=c[2]

	s=STRUCT([strada1,strada2,strada3,strada4,strada5,strada6,strada7,vicolo1,vicolo2,vicolo3,vicolo4,vicolo5,vicolo6,vicolo7])
	s = STRUCT([s,T([1,2])([14,2]),parking])

	s= MATERIAL([r,g,b,1,   0,0,0,1,  0,0,0,0, 0,0,0,1, 100])(s)
	return s

def createTerracedHouse(houseHPC,numberOfHouse):
	"""
	createTerracedHouse is a function that generate the HPC Model rapresenting  some terraced houses.
	@input houseHPC: HPC Model rapresenting the single house.
	@input numberOfHouse: number of houses in the terraced houses
	@return houses: HPC Model rapresenting the terraced houses.
	"""
	x = getDimensionAndPosition(houseHPC)[0][0]
	x = x + (x*0.2)
	s=[houseHPC]
	for i in range(0,numberOfHouse-1):
		s.append(T(1)(x))
		s.append(houseHPC)
	houses = STRUCT(s) 
	return houses

def createBasis(HPCModel):

	"""
	createBasis is a function that generate the HPC Model rapresenting the basis of the model.
	@input HPCModel: HPC Model rapresenting the model.
	@return terminatedBasis: HPC Model rapresenting the terminated basis.
	"""
	plan = BOX([1,2,3])(HPCModel)
	basis = BOX([1,2])(HPCModel)

	z = getDimensionAndPosition(plan)[0][2]
	

	c=color(0,104,10)
	r=c[0]
	g=c[1]
	b=c[2]
	basis = MATERIAL([r,g,b,1,   0,0,0,1,  0,0,0,0, 0,0,0,1, 20])(basis)

	c=color(182, 155, 76)
	r=c[0]
	g=c[1]
	b=c[2]
	plan = MATERIAL([r,g,b,1,   0,0,0,1,  0,0,0,0, 0,0,0,1, 20])(plan)

	terminatedBasis = STRUCT ([plan,T(3)(z+0.01),basis,T(3)(0.01),HPCModel])
	return terminatedBasis

def createTree():
	"""
	createTree is a function that generate the HPC Model rapresenting a tree.
	@return tree: HPC Model rapresenting the tree.
	"""

	leaves1 = STRUCT([T([1,2,3])([1,1,0]),(CUBOID([3,3,1]))])
	leaves2 = STRUCT([T([1,2,3])([0.5,0.5,1]),(CUBOID([4,4,1]))])
	leaves3 = STRUCT([T([1,2,3])([0,0,2]),(CUBOID([5,5,1]))])
	leaves4 = STRUCT([T([1,2,3])([1,1,3]),(CUBOID([3,3,1]))])
	leaves5 = STRUCT([T([1,2,3])([1.5,1.5,4]),(CUBOID([2,2,1]))])
	log = CUBOID([1,1,7])
	leaves = STRUCT([leaves1,leaves2,leaves3,leaves4,leaves5])
	leaves = TEXTURE(["texture/leaves.jpg", FALSE, TRUE, 1, 1, 0, 2, 2])(leaves)
	log = TEXTURE(["texture/log.jpg", FALSE, TRUE, 1, 1, 0, 2, 2])(log)
	up=[leaves]
	down=[log]
	up = STRUCT(up)
	up = onAxes(STRUCT([T([1,2,3])([20,20,7]),up]))
	down = STRUCT(down)
	down = onAxes(STRUCT([T([1,2])([20,20]),down]))
	dimUp = getDimensionAndPosition(up)[0]
	dimDown = getDimensionAndPosition (down)[0]
	down = STRUCT([T([1,2])([dimUp[0]/2-dimDown[0]/2,dimUp[1]/2-dimDown[1]/2]),down])
	tree = STRUCT([down,up])
	return tree


def createWood(tX,tY):
	"""
	createWood is a function that generate the HPC Model rapresenting the wood.
	@input tX,tY: number of trees on x and y.
	@return wood: HPC Model rapresenting the wood.
	"""
	tree = createTree()
	x=[tree]
	for i in range(1,tX):
		x.append(T(1)(6))
		x.append(tree)
	line = STRUCT(x)
	y = [line]
	for i in range(1,tY):
		y.append(T(2)(6))
		y.append(line)
	wood = STRUCT(y)
	return wood





def suburban_neighborhood():
	"""
	suburban_neighborhood is a function that generate the HPC Model rapresenting the complete model of suburban neighborhood.
	@return model: HPC Model rapresenting the complete model.
	"""

	#creazione strade
	streets = createStreet()
	streets = STRUCT([S([1,2,3])([2.5,2.5,2.5]),streets])

	#creazione elemento casa
	house = createHouse()
	house = STRUCT([S([1,2,3])([0.1,0.1,0.1]),house])

	#creazione ville a schiera
	terracedHouse1 = createTerracedHouse(house,4)
	terracedHouse1 = rotationAngle(terracedHouse1,PI/4.5)

	terracedHouse2 = createTerracedHouse(house,2)
	terracedHouse2 = rotationAngle(terracedHouse2,PI/4.5 + PI/2.3)

	terracedHouse3 = createTerracedHouse(house,3)
	terracedHouse3 = rotationAngle(terracedHouse3,PI/1.1)

	terracedHouse4 = createTerracedHouse(house,3)
	terracedHouse4 = rotationAngle(terracedHouse4,PI/1.1 + PI/2)

	terracedHouse5 = createTerracedHouse(house,1)
	terracedHouse5 = rotationAngle(terracedHouse5,PI/1.1 + PI/2 +PI)

	terracedHouse6 = createTerracedHouse(house,2)
	terracedHouse6 = rotationAngle(terracedHouse6,PI/1.1)

	terracedHouse7 = createTerracedHouse(house,2)
	terracedHouse7 = rotationAngle(terracedHouse7,PI/1.1 + PI)

	terracedHouse8 = createTerracedHouse(house,2)
	terracedHouse8 = rotationAngle(terracedHouse8,PI/1.2 + PI/2)

	terracedHouse9 = createTerracedHouse(house,2)
	terracedHouse9 = rotationAngle(terracedHouse9,PI/1.5 + PI/2)

	terracedHouse10 = createTerracedHouse(house,2)
	terracedHouse10 = rotationAngle(terracedHouse10,PI/1.4 + PI/2)

	#creazione ville singole
	house1 = rotationAngle(house,PI/1.1)
	house2 = rotationAngle(house,PI/4.8)
	house3 = rotationAngle(house,PI/0.95 + PI/2)

	#posizionamento case e ville a schiera
	model = STRUCT([streets,T([1,2])([9,19.5]),terracedHouse1])
	model = STRUCT([model,T([1,2])([11,13.5]),terracedHouse2])
	model = STRUCT([model,T([1,2])([26.5,14.8]),terracedHouse3])
	model = STRUCT([model,T([1,2])([29,14.8]),terracedHouse4])
	model = STRUCT([model,T([1,2])([31.5,10]),terracedHouse5])
	model = STRUCT([model,T([1,2])([36,9]),terracedHouse6])
	model = STRUCT([model,T([1,2])([23.3,20.3]),terracedHouse7])
	model = STRUCT([model,T([1,2])([41.5,15.5]),terracedHouse8])
	model = STRUCT([model,T([1,2])([47,20.7]),terracedHouse9])
	model = STRUCT([model,T([1,2])([53,25]),terracedHouse10])
	model = STRUCT([model,T([1,2])([19.8,24.3]),house1])
	model = STRUCT([model,T([1,2])([33,18.3]),house1])
	model = STRUCT([model,T([1,2])([36,17.5]),house2])
	model = STRUCT([model,T([1,2])([42,20.5]),house2])
	model = STRUCT([model,T([1,2])([41,7.5]),house3])

	#creazione bosco
	wood = createWood(10,30)
	wood = STRUCT([S([1,2,3])([0.07,0.07,0.07]), wood])
	dim = [getDimensionAndPosition(model)[0][0]-getDimensionAndPosition(wood)[0][0],getDimensionAndPosition(model)[0][1]-getDimensionAndPosition(wood)[0][1],getDimensionAndPosition(model)[0][2]-getDimensionAndPosition(wood)[0][2]]
	model = STRUCT([model,T([1,2])([0,dim[1]]),wood])
	wood = createWood(10,20)
	wood = STRUCT([S([1,2,3])([0.07,0.07,0.07]), wood])
	model = STRUCT([model,T([1,2])([0,0]),wood])
	wood = createWood(20,15)
	wood = STRUCT([S([1,2,3])([0.07,0.07,0.07]), wood])
	dim = [getDimensionAndPosition(model)[0][0]-getDimensionAndPosition(wood)[0][0],getDimensionAndPosition(model)[0][1]-getDimensionAndPosition(wood)[0][1],getDimensionAndPosition(model)[0][2]-getDimensionAndPosition(wood)[0][2]]
	model = STRUCT([model,T([1,2])([0,dim[1]]),wood])
	wood = createWood(120,5)
	wood = STRUCT([S([1,2,3])([0.07,0.07,0.07]), wood])
	dim = [getDimensionAndPosition(model)[0][0]-getDimensionAndPosition(wood)[0][0],getDimensionAndPosition(model)[0][1]-getDimensionAndPosition(wood)[0][1],getDimensionAndPosition(model)[0][2]-getDimensionAndPosition(wood)[0][2]]
	model = STRUCT([model,T([1,2])([0,dim[1]]),wood])
	wood = createWood(60,15)
	wood = STRUCT([S([1,2,3])([0.07,0.07,0.07]), wood])	
	model = STRUCT([model,T([1,2])([0,0]),wood])
	wood = createWood(20,30)
	wood = STRUCT([S([1,2,3])([0.07,0.07,0.07]), wood])
	dim = [getDimensionAndPosition(model)[0][0]-getDimensionAndPosition(wood)[0][0],getDimensionAndPosition(model)[0][1]-getDimensionAndPosition(wood)[0][1],getDimensionAndPosition(model)[0][2]-getDimensionAndPosition(wood)[0][2]]
	model = STRUCT([model,T([1,2])([dim[0],0]),wood])
	wood = createWood(7,50)
	wood = STRUCT([S([1,2,3])([0.07,0.07,0.07]), wood])
	dim = [getDimensionAndPosition(model)[0][0]-getDimensionAndPosition(wood)[0][0],getDimensionAndPosition(model)[0][1]-getDimensionAndPosition(wood)[0][1],getDimensionAndPosition(model)[0][2]-getDimensionAndPosition(wood)[0][2]]
	model = STRUCT([model,T([1,2])([dim[0],0]),wood])
	
	#creazione elemento albero
	tree = createTree()
	tree = STRUCT([S([1,2,3])([0.07,0.07,0.07]), tree])

	#posizionamento alberi sul bordo stradale
	model = STRUCT([model,T([1,2])([11,19]),tree])
	model = STRUCT([model,T([1,2])([12,19.7]),tree])
	model = STRUCT([model,T([1,2])([13,20.2]),tree])
	model = STRUCT([model,T([1,2])([14,21.1]),tree])
	model = STRUCT([model,T([1,2])([15,22]),tree])
	model = STRUCT([model,T([1,2])([16,22.7]),tree])
	model = STRUCT([model,T([1,2])([17,23]),tree])
	model = STRUCT([model,T([1,2])([18,23]),tree])
	model = STRUCT([model,T([1,2])([19,22.9]),tree])
	model = STRUCT([model,T([1,2])([20,22.1]),tree])
	model = STRUCT([model,T([1,2])([21,21.7]),tree])
	model = STRUCT([model,T([1,2])([23,20]),tree])
	model = STRUCT([model,T([1,2])([24,19.5]),tree])
	model = STRUCT([model,T([1,2])([25,19]),tree])
	model = STRUCT([model,T([1,2])([26,18.6]),tree])
	model = STRUCT([model,T([1,2])([27,18.1]),tree])
	model = STRUCT([model,T([1,2])([28,18]),tree])
	model = STRUCT([model,T([1,2])([29,17.8]),tree])
	model = STRUCT([model,T([1,2])([31,17]),tree])
	model = STRUCT([model,T([1,2])([32,16.8]),tree])
	model = STRUCT([model,T([1,2])([33,16.5]),tree])
	model = STRUCT([model,T([1,2])([34,16]),tree])
	model = STRUCT([model,T([1,2])([11.4,16.8]),tree])
	model = STRUCT([model,T([1,2])([11.7,15.8]),tree])
	model = STRUCT([model,T([1,2])([12.4,14.8]),tree])
	model = STRUCT([model,T([1,2])([13,14]),tree])
	model = STRUCT([model,T([1,2])([14,13.7]),tree])
	model = STRUCT([model,T([1,2])([15,13.7]),tree])
	model = STRUCT([model,T([1,2])([16,14.2]),tree])
	model = STRUCT([model,T([1,2])([17,14.7]),tree])
	model = STRUCT([model,T([1,2])([18,15.5]),tree])
	model = STRUCT([model,T([1,2])([19,16.1]),tree])
	model = STRUCT([model,T([1,2])([20,17]),tree])
	model = STRUCT([model,T([1,2])([21,18]),tree])
	model = STRUCT([model,T([1,2])([22,18.5]),tree])
	model = STRUCT([model,T([1,2])([23,18.5]),tree])
	model = STRUCT([model,T([1,2])([24,17.9]),tree])
	model = STRUCT([model,T([1,2])([25,17.5]),tree])
	model = STRUCT([model,T([1,2])([26,17]),tree])	
	model = STRUCT([model,T([1,2])([27,16.8]),tree])
	model = STRUCT([model,T([1,2])([28,16.5]),tree])
	model = STRUCT([model,T([1,2])([29,16.3]),tree])
	model = STRUCT([model,T([1,2])([31,15.7]),tree])
	model = STRUCT([model,T([1,2])([32,15.3]),tree])
	model = STRUCT([model,T([1,2])([33,14.9]),tree])
	model = STRUCT([model,T([1,2])([34,14.5]),tree])
	model = STRUCT([model,T([1,2])([35,13.8]),tree])
	model = STRUCT([model,T([1,2])([36,13]),tree])
	model = STRUCT([model,T([1,2])([37,12.3]),tree])
	model = STRUCT([model,T([1,2])([38,11]),tree])
	model = STRUCT([model,T([1,2])([15,18]),tree])
	model = STRUCT([model,T([1,2])([15,19]),tree])
	model = STRUCT([model,T([1,2])([16,19]),tree])
	model = STRUCT([model,T([1,2])([17,19]),tree])
	model = STRUCT([model,T([1,2])([17,20]),tree])
	model = STRUCT([model,T([1,2])([18,20]),tree])
	model = STRUCT([model,T([1,2])([18,19]),tree])
	model = STRUCT([model,T([1,2])([15,17]),tree])
	model = STRUCT([model,T([1,2])([16,18]),tree])
	model = STRUCT([model,T([1,2])([36,16.1]),tree])
	model = STRUCT([model,T([1,2])([37,16.9]),tree])
	model = STRUCT([model,T([1,2])([38,17.4]),tree])
	model = STRUCT([model,T([1,2])([39,18]),tree])
	model = STRUCT([model,T([1,2])([40,18.4]),tree])
	model = STRUCT([model,T([1,2])([43,20]),tree])
	model = STRUCT([model,T([1,2])([44,20.5]),tree])
	model = STRUCT([model,T([1,2])([45,21.2]),tree])
	model = STRUCT([model,T([1,2])([39.9,13.1]),tree])
	model = STRUCT([model,T([1,2])([40.5,14]),tree])
	model = STRUCT([model,T([1,2])([41,15]),tree])
	model = STRUCT([model,T([1,2])([41.3,16]),tree])
	model = STRUCT([model,T([1,2])([41.7,17]),tree])
	model = STRUCT([model,T([1,2])([43,18.7]),tree])
	model = STRUCT([model,T([1,2])([44,19.2]),tree])
	model = STRUCT([model,T([1,2])([45,19.8]),tree])
	model = STRUCT([model,T([1,2])([46,20.5]),tree])
	model = STRUCT([model,T([1,2])([47,21]),tree])
	model = STRUCT([model,T([1,2])([48,21.6]),tree])
	model = STRUCT([model,T([1,2])([50,23]),tree])
	model = STRUCT([model,T([1,2])([51,23.8]),tree])
	model = STRUCT([model,T([1,2])([52,24.8]),tree])
	model = STRUCT([model,T([1,2])([53,25.9]),tree])
	model = STRUCT([model,T([1,2])([53.4,27]),tree])
	model = STRUCT([model,T([1,2])([39,16]),tree])
	model = STRUCT([model,T([1,2])([38,16]),tree])
	model = STRUCT([model,T([1,2])([40,17]),tree])
	model = STRUCT([model,T([1,2])([39,15]),tree])
	model = STRUCT([model,T([1,2])([38,15]),tree])
	model = STRUCT([model,T([1,2])([39,12]),tree])
	model = STRUCT([model,T([1,2])([39.8,11]),tree])
	model = STRUCT([model,T([1,2])([40.2,10]),tree])
	model = STRUCT([model,T([1,2])([40.8,8]),tree])
	model = STRUCT([model,T([1,2])([40.9,7]),tree])
	model = STRUCT([model,T([1,2])([41,6]),tree])
	model = STRUCT([model,T([1,2])([41,5]),tree])
	model = STRUCT([model,T([1,2])([40.9,4]),tree])
	model = STRUCT([model,T([1,2])([40.7,3]),tree])
	model = STRUCT([model,T([1,2])([40.5,2]),tree])
	model = STRUCT([model,T([1,2])([40.1,1]),tree])
	model = STRUCT([model,T([1,2])([38.7,10]),tree])
	model = STRUCT([model,T([1,2])([39.2,9]),tree])
	model = STRUCT([model,T([1,2])([39.6,8]),tree])
	model = STRUCT([model,T([1,2])([39.8,7]),tree])
	model = STRUCT([model,T([1,2])([39.8,6]),tree])


	#creazione modello finale (con base di legno)
	model = createBasis(model)
	
	return model

def main():
	VIEW(suburban_neighborhood())
if __name__ == "__main__":
    main()

