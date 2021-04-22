from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import rhinoscriptsyntax as rs
from compas.geometry import Frame
from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors
from compas.geometry import add_vectors
from compas.geometry.primitives import Vector
from compas.geometry import distance_point_point

from compas_rhino.geometry import RhinoPoint
from compas_rhino.geometry import RhinoPlane


__all__ = ['Beam']


class Beam():

    def __init__(self):
        self._frame = None
        self.x = 1
        self.y = 1
        self._length = 0

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, new_frame):
        self._frame = new_frame

    @property
    def length(self):
        return self._length

    @property
    def sp(self):
        return self._frame.point

    @property
    def ep(self):
        return add_vectors(self.sp, self._frame.zaxis*self.length)

    @property
    def line(self):
        return (self.sp, self.ep)

    @classmethod
    def from_points_dir(cls, sp, ep, sec_dir=[1, 0, 0]):
        """
        Parameter:
        ----------
        sp: a tuple of 3 floats
        ep: a tuple of 3 floats

        """
        beam = cls()
        z = subtract_vectors(ep, sp)
        y = cross_vectors(z, sec_dir)
        x = cross_vectors(y, z)
        beam._frame = Frame(sp, x, y)
        beam._length = distance_point_point(sp, ep)

        return beam

    @classmethod
    def from_frame_length(cls, frame, length):
        """
        Parameter:
        ----------
        frame: a compas Frame at starting
        length: a float

        """
        beam = cls()
        beam._frame = frame
        beam._length = length
        return beam

    @classmethod
    def from_lines(cls):
        """
        Parameter:
        ----------
        lines: a list of 2 points

        """
        raise NotImplementedError


if __name__ == '__main__':
    pass