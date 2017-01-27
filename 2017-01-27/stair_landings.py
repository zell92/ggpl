from pyplasm import *
from tools import *


def rizerAndTread(dy,dz):
    """
    this function returns a 3-values array: rizer of a step, 
    tread of a step and number of total steps.
    @Input dy,dz: (the dimensions y and z of whole structure)
    """
    #profondita' pianerottolo 1m
    
    p=0.63/((2*dz/dy)+1)
    a=(0.63-p)/2
    frazioneA= dz/a
    nGradini = round((frazioneA-1))    
    result=[p,a,nGradini]
    return result

def ggpl_stair_landings(dx,dy,dz):
    """
    this function returns some HTC values, representative of a Stair landings. 
    @Input dx,dy,dx: (the dimensions of whole structure)
    """
    dati=rizerAndTread(dy,dz)
    nGradini = dati[2]
    alzata=dati[1]
    pedata=dati[0]
    yPianerottolo = dy/3.0
    lGradino = dx/2
    pianerottolo=CUBOID([dx,yPianerottolo,alzata])
    halfSteps=0
    dispari=0
    if nGradini%2==0:
        halfSteps=nGradini/2
    else:
        halfSteps=(nGradini-1)/2
        dispari=1
    scala=[]
    diagonale=[]
    dist=[-(dx/2),dx/2]
    dist2=[dx/2]
    distDiag=QUOTE(dist)
    scala.append(T([1])(lGradino))
    a=0
    p=pedata
    diagonale.append([a,p])
    diagonale.append([alzata,p])
    diagonale.append([alzata,2*p])
    d=MKPOL([diagonale,[[1,2,3]],None])
    d=PROD([distDiag,d])
    d=STRUCT([R([2,3])(PI/2),d])
    d=STRUCT([R([1,2])(PI),d])
    d=STRUCT([T([1])(dx*3/2),d])
    for i in range (1,int(halfSteps)):
        p=p+pedata
        a=a+alzata
        scala.append(CUBOID([lGradino,pedata,alzata]))
        scala.append(T([1,2,3])([0,pedata,alzata]))
        d=STRUCT([d,T([2,3])([pedata,alzata]),d])
        
    scala.append(CUBOID([lGradino,pedata,alzata]))
    scala.append(T([1,2,3])([-lGradino,pedata,alzata]))
    scala.append(pianerottolo)
    
    scala1=STRUCT([STRUCT(scala),d])
    
    if dispari:
        halfSteps2=halfSteps+1

    scalaMirror=[]
    diagonaleMirror=[]
    dist=[-(dx/2),dx/2]
    dist2=[dx/2]
    distDiag=QUOTE(dist)
    scalaMirror.append(T([1])(lGradino))
    a=0
    p=pedata
    diagonaleMirror.append([a,p])
    diagonaleMirror.append([alzata,p])
    diagonaleMirror.append([alzata,2*p])
    d2=MKPOL([diagonale,[[1,2,3]],None])
    d2=PROD([distDiag,d2])
    d2=STRUCT([R([2,3])(PI/2),d2])
    d2=STRUCT([R([1,2])(PI),d2])
    d2=STRUCT([T([1,2,3])([dx*3/2,-pedata,-alzata]),d2])
   
    for i in range (1,int(halfSteps)):
        d2=STRUCT([d2,T([2,3])([pedata,alzata]),d2])
        p=p+pedata
        a=a+alzata
        scalaMirror.append(CUBOID([lGradino,pedata,alzata]))
        scalaMirror.append(T([1,2,3])([0,pedata,alzata]))

    p=p+pedata
    a=a+alzata
    
    scalaMirror.append(CUBOID([lGradino,pedata,alzata]))
    
    
    scala2=STRUCT([STRUCT(scalaMirror),d2])
    scala2=STRUCT([R([1,2])(PI),scala2])
    scala2=STRUCT([T([1,2,3])([lGradino*2,pedata*(halfSteps),alzata*(halfSteps+1)]),scala2])
    
    scala2=STRUCT([scala1,scala2])
    a=SIZE([1,2,3])(BOX([1,2,3])(scala2))
                
    sx=dx/a[0]                
    sy=dy/a[1]
    sz=dz/a[2]

    scala2=STRUCT([COLOR(color(255,255,255)),S([1,2,3])([sx,sy,sz]),scala2])
    return scala2

def createStair(x,y,z):
    r= ggpl_stair_landings(x,y,z)
    r=STRUCT(S)
   
def main():
    r=ggpl_stair_landings(2,3,3)
    print (getDimensionAndPosition(r))
    VIEW(r)

if __name__ == "__main__":
    main()

