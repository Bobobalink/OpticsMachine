import drawSvg as draw
import math
from dataclasses import dataclass

@dataclass
class RaySegment:
  startx: float
  endx: float
  # height of ray (relative to optical axis) at the start of the ray
  startHeight: float
  # angle (radians) of the ray relative to the optical axis
  angle: float

  # IOR of the material the ray is currently in
  n: float = 1.0

  def heightAt(self, x):
    return self.startHeight + math.tan(self.angle) * (x - self.startx)

  @property
  def endHeight(self):
    return self.heightAt(self.endx)

  # add the end of this ray as another step in the path
  def appendDraw(self, path: draw.Path):
    path.L(self.endx, self.endHeight)

    return path

  def draw(self):
    p = draw.Path()
    p.M(self.startx, self.startHeight)
    return self.appendDraw(p)
