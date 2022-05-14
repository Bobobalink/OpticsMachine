import math
import drawSvg as draw
from dataclasses import dataclass

@dataclass
class Lens:
  # positive radii curve out to the left
  # radius of curvature of the left surface
  s1Radius: float
  # radius of curvature of the right surface
  s2Radius: float
  # distance between the central point of each surface (on the optical axis)
  thickness: float
  # diameter of the lens itself
  diameter: float

  def draw(self) -> draw.Path:
    # draw the lens centered about (0, 0), optical axis is x axis
    p = draw.Path()

    # calculate the starting point for the left surface
    s1rad = self.s1Radius
    s1Swapped = False
    if s1rad < 0:
      s1rad *= -1
      s1Swapped = True
    rcos = math.sqrt(s1rad ** 2 - (self.diameter / 2) ** 2)

    # if the lens curves left, the edges go in
    # if the lens curves right, the edges flange out
    if s1Swapped:
      edgeX = self.thickness / 2 + (s1rad - rcos)
    else:
      edgeX = self.thickness / 2 - (s1rad - rcos)
    
    # start at the top left corner of the lens
    p.M(-edgeX, self.diameter / 2)
    # draw the left lens surface
    p.A(s1rad, s1rad, 0, 0, s1Swapped, -edgeX, -self.diameter / 2)

    # calculate the starting point for the right surface
    s2rad = self.s2Radius
    s2Swapped = True
    if s2rad < 0:
      s2rad *= -1
      s2Swapped = False
    rcos = math.sqrt(s2rad ** 2 - (self.diameter / 2) ** 2)

    # if the lens curves left, the edges go in
    # if the lens curves right, the edges flange out
    if s2Swapped:
      edgeX = self.thickness / 2 + (s2rad - rcos)
    else:
      edgeX = self.thickness / 2 - (s2rad - rcos)

    # draw the bottom edge of the lens
    p.L(edgeX, -self.diameter / 2)

    # draw the second lens surface from the bottom to the top
    p.A(s2rad, s2rad, 0, 0, s2Swapped, edgeX, self.diameter / 2)

    # close the loop with the top edge
    p.Z()

    return p 
