import math
import drawSvg as draw
from dataclasses import dataclass
from sys import float_info
from rays import RaySegment

def clamp(x, low, high):
  return min(max(x, low), high)

def noinfs(x):
  return clamp(x, float_info.min, float_info.max)

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
  # position of the lens along the optical axis
  position: float

  # index of refraction
  n: float

  @property
  def scaledThickness(self):
    return self.thickness / self.n

  def s1Power(self, otherIOR):
    return noinfs((self.n - otherIOR) / self.s1Radius)

  def s2Power(self, otherIOR):
    return noinfs((otherIOR - self.n) / self.s2Radius)

  @property
  def s1Curvature(self):
    return noinfs(1 / self.s1Radius)

  @s1Curvature.setter
  def s1Curvature(self, c):
    self.s1Radius = noinfs(1 / c)

  @property
  def s2Curvature(self):
    return noinfs(1 / self.s2Radius)

  @s2Curvature.setter
  def s2Curvature(self, c):
    self.s2Radius = noinfs(1 / c)

  # trace the ray through s1 of the lens, truncating the current ray segment
  # and returning the next one
  def snuFTraceS1(self, ray: RaySegment) -> RaySegment:
    if ray.endx < self.position:
      raise ValueError('ray does not reach lens')

    if abs(ray.endHeight) > self.diameter / 2:
      # ray misses lens above or below, don't change ray and don't make a new ray
      return None
      
    # terminate ray at the lens
    ray.endx = self.position

    phi = self.s1Power(ray.n)


  def draw(self) -> draw.Path:
    # draw the lens centered about (0, 0), optical axis is x axis
    p = draw.Path()

    # draw the left lens surface
    # if the surface is flat, draw it flat
    if abs(self.s1Radius) >= float_info.max:
      p.M(self.position - self.thickness / 2, self.diameter / 2)
      p.L(self.position - self.thickness / 2, -self.diameter / 2)
    else:
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
      p.M(self.position - edgeX, self.diameter / 2)
      p.A(s1rad, s1rad, 0, 0, s1Swapped, self.position - edgeX, -self.diameter / 2)

    if abs(self.s2Radius) >= float_info.max:
      # draw the bottom edge of the lens
      p.L(self.position + self.thickness / 2, -self.diameter / 2)
      # draw the right surface flat
      p.L(self.position + self.thickness / 2, self.diameter / 2)
    else:
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
      p.L(self.position + edgeX, -self.diameter / 2)

      # draw the second lens surface from the bottom to the top
      p.A(s2rad, s2rad, 0, 0, s2Swapped, self.position + edgeX, self.diameter / 2)

    # close the loop with the top edge
    p.Z()

    return p
