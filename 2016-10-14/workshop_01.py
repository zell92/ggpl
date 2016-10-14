from pyplasm import *
"""this function returns some HTC values, representative of a space frame. 
Input: 
bx,bz (given dimensions of beam section), 
px,py (given dimensions of pillar section), 
[dy1,dy2,...] (distances between axes of the pillars), 
[hz1,hz2,...] (interstory heights)"""
def spaceFrame(bx,bz,px,py,distances,heights):

  d=distances[0]*-1;
  h=heights[0];

  if bx>px:
    dist=(bx-px)/2.
    pilX=[0,-dist,px]
    beaX=[bx]
  elif bx==px:
    beaX=[bx]
    pilX=[px]
  else:
    dist=(px-bx)/2.
    beaX=[0,-dist,bx]
    pilX=[px]

  
  pilY=[py]
  pilZ=[h]

  
  beaY=[py/2,0]
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
  beaY.append(py/2)

  pillarX=QUOTE(pilX)
  pillarY=QUOTE(pilY)
  pillarZ=QUOTE(pilZ)
  beamsX=QUOTE(beaX)
  beamsY=QUOTE(beaY)
  beamsZ=QUOTE (beaZ)
  beams2D=PROD([beamsX,beamsY])
  beams3D=PROD([beams2D,beamsZ])
  pillars2D=PROD([pillarX,pillarY])
  pillars3D=PROD([pillars2D,pillarZ])
  combine=STRUCT([beams3D,pillars3D])
  return combine
  

    
VIEW(spaceFrame(1.,1.,1.,1.,[4,1,5,2],[4,2,5]))

