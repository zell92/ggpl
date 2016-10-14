from pyplasm import *
""" prova"""
def spaceFrame(bx,bz,px,py,distances,heights):

  d=distances[0]*-1;
  h=heights[0];

  pilX=[px]
  pilY=[py]
  pilZ=[h]

  beaX=[bx]
  beaY=[0,-py/2]
  beaZ=[0,h*-1,bz]

  

  

  for d in distances:
    pilY.append(d*-1);
    pilY.append(py)
    beaY.append((d)+py)
    beaY.append(0)
    #y.append(0)
    #y.append(py)
  for h in heights[1:]:
    pilZ.append(bz*-1)
    pilZ.append(h)
    beaZ.append(h*-1)
    beaZ.append(bz)

  a=QUOTE(pilX)
  b=QUOTE(pilY)
  c=QUOTE(pilZ)
  q=QUOTE(beaX)
  w=QUOTE(beaY)
  e=QUOTE (beaZ)
  bb=PROD([q,w])
  bbb=PROD([bb,e])
  aa=PROD([a,b])
  aaa=PROD([aa,c])
  ccc=STRUCT([aaa,bbb])
  return ccc
  

    


d = [4,3]
h=[4,3]
VIEW(spaceFrame(1.,1.,1.,1.,[4,1],[4,3]))

