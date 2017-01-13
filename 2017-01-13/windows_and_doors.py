from house_windows_and_doors import *
from tools import *
from pyplasm import *
from fpformat import *
def window(X,Y,Z,occupancy):
    def window2(dx,dy,dz):
        
        #colori
        bianco=color(255,255,255)
        glass=color(201, 219, 220)
        #spessore vetro
        spessoreVetro=0.02
        #variabili di traslazione
        ty=0
        tz=0
        tz2=0
        #Variabili di supporto per la costruzione della finestra
        legno1=PROD([QUOTE([0]),QUOTE([0])])
        vetro1=PROD([QUOTE([0]),QUOTE([0])])

        
        #costruzione della cornice della finestra
        for y in range(0,len(Y)):
            for z in range(0,len(Z)):
                legnox=[]
                for x in range (0,len(X)):
                    if occupancy[z][y][x]==0:
                        legnox.append(X[x]*-1)
                    else:
                        legnox.append(X[x])
                legno2= PROD([QUOTE(legnox),QUOTE([Y[y]])])
                legno2= PROD([legno2,QUOTE([Z[z]])])
                legno1=STRUCT([legno1,T([2,3])([ty,tz]),legno2]) 
                tz=Z[z]
                tz2=tz2+tz
            tz2=tz2-tz-Z[z-1]
            legno1=STRUCT([legno1,T([2,3])([ty,tz2-tz]),legno2]) 
            tz=0
            tz2=0
            ty=Y[y]
         
        #azzeramento delle variabili di traslazione
        tz=0
        tz2=0
        ty=0
        
        #costruzione vetro
        for y in range(0,len(Y)):
            ty=ty+(Y[y]/2)-(spessoreVetro/2)
            for z in range(0,len(Z)):
                vetrox=[]
                for x in range (0,len(X)):
                    if occupancy[z][y][x]==0:
                        if occupancy[z][y][x+1]==1 and occupancy[z][y][x-1]==1:
                            vetrox.append(X[x])
                        else:
                            vetrox.append(X[x]*-1)
                            
                    else:
                        vetrox.append(X[x]*-1)
                positivo = False
                for v in vetrox:
                    if v>=0:
                        positivo=True
                if positivo:
                    vetro2= PROD([QUOTE(vetrox),QUOTE([0.02])])
                    vetro2= PROD([vetro2,QUOTE([Z[z]])])
                    vetro1=STRUCT([vetro1,T([2,3])([ty,tz]),vetro2]) 
                tz=Z[z]
                tz2=tz2+tz
            tz2=tz2-tz-Z[z-1]
            if positivo:
                vetro1=STRUCT([vetro1,T([2,3])([ty,tz2-tz]),vetro2]) 
            tz=0
            tz2=0
            
        #colorazione
        legno1 = STRUCT([COLOR(bianco),legno1])
        vetro1 = STRUCT([COLOR(glass),vetro1])
        #assemblaggio parti
        finestra= STRUCT([legno1,vetro1])
        posizioneManiglia=[X[0]+(X[1]/2)-0.015,Y[0]-0.03,(SIZE(3)(legno1))/2]
        #maniglia= STRUCT([COLOR(color(0,0,0)),T([1,2,3])(posizioneManiglia),(CUBOID([0.03,0.03,0.2]))])
        #finestra= STRUCT([finestra,maniglia])
        #adattamento alle dimenzioni desiderate
        dim=[dx/SIZE(1)(finestra),dy/SIZE(2)(finestra),dz/SIZE(3)(finestra)]
        finestra= STRUCT([S([1,2,3])(dim),finestra])
        
        return finestra
    return window2

def singleDoor(X,Y,Z,occupancy):
    def singleDoor2(dx,dy,dz,colore):
        #spessore vetro
        spessoreVetro=0.02
        #colori
        bordo=colore
        glass=color(201, 219, 220)
        gold=color(255,215,0)
        #variabili di supporto per la costruzione della porta
        legno1=PROD([QUOTE([0]),QUOTE([0])])
        vetro1=PROD([QUOTE([0]),QUOTE([0])])
        #array per la costruzione della struttura e del vetro
        s=[COLOR(bordo)]
        v=[COLOR(glass),T(2)(Y[-1])]
        
        #costruzione struttura
        for y in range(0,len(Y)):
            for z in range(0,len(Z)):
                legnox=[]
                for x in range (0,len(X)):
                    if occupancy[z][y][x]==0:
                        legnox.append(X[x]*-1)
                    else:
                        legnox.append(X[x])
               
                legno2= PROD([QUOTE(legnox),QUOTE([Y[y]])])
                legno2= PROD([legno2,QUOTE([Z[z]])])
                s.append(legno2)
                s.append(T([3])([Z[z]]))
            s.append(T([2,3])([Y[y],-SIZE(3)(STRUCT(s))]))
        #costruzione vetro    
        for z in range(0,len(Z)):
            vetrox=[]
            for x in range (0,len(X)):
                if occupancy[z][len(Y)-1][x]==0:
                    vetrox.append(X[x])
                else:
                    vetrox.append(X[x]*-1)
            positivo = False
            for i in vetrox:
                if i>=0:
                    positivo=True
            if positivo:
                vetro2= PROD([QUOTE(vetrox),QUOTE([spessoreVetro])])
                vetro2= PROD([vetro2,QUOTE([Z[z]])])
                v.append(vetro2)
            v.append(T([3])([Z[z]]))
        #costruzione porta 
        struttura=STRUCT(s)
        vetro=STRUCT(v)
        porta=STRUCT([struttura,vetro])
        #aggiunta maniglie
        centro=X[len(X)/2]/2
        posizioneManiglia=[SIZE(1)(porta)/2-(0.1+0.01)-centro,Y[0]-0.03,(SIZE(3)(porta))/2]
        maniglia=STRUCT([T(1)((centro*2)+0.12),CUBOID([0.1,0.03,0.03])])
        maniglia= STRUCT([COLOR(gold),T([1,2,3])(posizioneManiglia),maniglia])
        porta= STRUCT([porta,maniglia])
        
        #adattamento alle dimenzioni desiderate
        dim=[dx/SIZE(1)(porta),dy/SIZE(2)(porta),dz/SIZE(3)(porta)]
        porta= STRUCT([S([1,2,3])(dim),porta])
        
        return porta
    return singleDoor2

def door(X,Y,Z,occurency):
    def door2(dx,dy,dz,colore):
        #spessore vetro
        spessoreVetro=0.02
        #colori
        esterno=color
        glass=color(201, 219, 220)
        gold=color(255,215,0)
        #variabili di supporto per la costruzione della porta
        legno1=PROD([QUOTE([0]),QUOTE([0])])
        vetro1=PROD([QUOTE([0]),QUOTE([0])])
        #array per la costruzione della struttura e del vetro
        s=[COLOR(colore)]
        v=[COLOR(glass),T(2)(Y[-1])]
        
        #costruzione struttura
        for y in range(0,len(Y)):
            for z in range(0,len(Z)):
                legnox=[]
                for x in range (0,len(X)):
                    if occupancy[z][y][x]==0:
                        legnox.append(X[x]*-1)
                    else:
                        legnox.append(X[x])
               
                legno2= PROD([QUOTE(legnox),QUOTE([Y[y]])])
                legno2= PROD([legno2,QUOTE([Z[z]])])
                s.append(legno2)
                s.append(T([3])([Z[z]]))
            s.append(T([2,3])([Y[y],-SIZE(3)(STRUCT(s))]))
        #costruzione vetro    
        for z in range(0,len(Z)):
            vetrox=[]
            for x in range (0,len(X)):
                if occupancy[z][len(Y)-1][x]==0:
                    vetrox.append(X[x])
                else:
                    vetrox.append(X[x]*-1)
            positivo = False
            for i in vetrox:
                if i>=0:
                    positivo=True
            if positivo:
                vetro2= PROD([QUOTE(vetrox),QUOTE([spessoreVetro])])
                vetro2= PROD([vetro2,QUOTE([Z[z]])])
                v.append(vetro2)
            v.append(T([3])([Z[z]]))
        #costruzione porta 
        struttura=STRUCT(s)
        vetro=STRUCT(v)
        porta=STRUCT([struttura,vetro])
        #aggiunta maniglie
        centro=X[len(X)/2]/2
        posizioneManiglia=[SIZE(1)(porta)/2-(0.1+0.01)-centro,Y[0]-0.03,(SIZE(3)(porta))/2]
        maniglia=STRUCT([CUBOID([0.1,0.03,0.03]),T(1)((centro*2)+0.12),CUBOID([0.1,0.03,0.03])])
        maniglia= STRUCT([COLOR(gold),T([1,2,3])(posizioneManiglia),maniglia])
        porta= STRUCT([porta,maniglia])
        
        #adattamento alle dimenzioni desiderate
        dim=[dx/SIZE(1)(porta),dy/SIZE(2)(porta),dz/SIZE(3)(porta)]
        porta= STRUCT([S([1,2,3])(dim),porta])
        
        return porta
    return door2

def createWindow(dx,dy,dz):
	Z=[0.1,0.05,1.5,0.05,0.1]
	X=[0.1,0.05,0.7,0.05,0.7,0.05,0.1]
	Y=[0.1,0.1]
	occupancy=[[[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]],[[1,0,0,1,1,1,1],[1,1,1,1,0,0,1]],[[1,0,0,1,0,1,1],[1,1,0,1,0,0,1]],[[1,0,0,1,1,1,1],[1,1,1,1,0,0,1]],[[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]]] 
	#ZYX
	return window(X,Y,Z,occupancy)(dx,dy,dz)

def createDoubleDoor(dx,dy,dz,colore):
	Z=[0.05,.1,.15,.03,1.65,.03,.15,.1,.05]
	X=[.05,.1,.15,.03,0.5,.05,.15,.1,0.1,.1,.15,.03,0.5,.05,.15,.1,0.05]
	Y=[0.02,0.07]
	occupancy=[[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]],[[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]],[[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],[1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1]],[[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]],[[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],[1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1]],[[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]],[[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],[1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1]],[[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]],[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]]
	#ZYX
	return door(X,Y,Z,occupancy)(dx,dy,dz,colore)

def createSingleDoor(dx,dy,dz,colore):
	Z=[0.05,.1,.15,.03,1.65,.03,.15,.1,.05]
	X=[.05,.1,.15,.03,0.5,.05,.15,.1,0.05]
	Y=[0.02,0.07]
	occupancy=[[[1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1]],[[1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1]],[[1,0,0,0,0,0,0,0,1],[1,1,0,1,0,1,0,1,1]],[[1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1]],[[1,0,0,0,0,0,0,0,1],[1,1,0,1,0,1,0,1,1]],[[1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1]],[[1,0,0,0,0,0,0,0,1],[1,1,0,1,0,1,0,1,1]],[[1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1]],[[1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1]]]
	#ZYX
	return singleDoor(X,Y,Z,occupancy)(dx,dy,dz,colore)

def adaptWindow():
    data=getDataWindows(19,9)
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

def adaptExternalDoor():
	data=getDataExternalDoors(19,9)
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

def adaptInternalDoor():
	data=getDatainternalDoors(19,9)
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


def main():
	house = ggpl_building_house(19,9)
	house=STRUCT([house,adaptWindow(),adaptInternalDoor(),adaptExternalDoor()])
	VIEW(house)

if __name__ == "__main__":
    main()


