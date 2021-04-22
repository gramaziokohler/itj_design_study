from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .beam import Beam
from compas.geometry import Frame
from compas.geometry import cross_vectors
from compas.geometry.primitives import Vector
from compas.geometry import Rotation
from compas.geometry import intersection_plane_plane
from compas.geometry import intersection_line_plane
from compas.geometry import closest_point_on_line
from compas.geometry import Line
from copy import deepcopy


__all__ = ['beam_connection', 'beam_connection_short']


def beam_connection(beam1, beam2, t=0):
    """ find the set of connection beams of the given two beams """

    plane1 = (beam1.frame.point, beam1.frame.xaxis)
    plane2 = (beam2.frame.point, beam2.frame.xaxis)

    intersection_line = intersection_plane_plane(plane1, plane2)

    pt_on_beam1 = Line(*beam1.line).point(t)
    pt_on_intersection = closest_point_on_line(pt_on_beam1, intersection_line)
    beam3 = Beam.from_points_dir(pt_on_intersection, pt_on_beam1, beam1.frame.yaxis)

    plane_intersection = (pt_on_intersection, beam3.frame.xaxis)

    pt_on_beam2 = intersection_line_plane(beam2.line, plane_intersection)
    beam4 = Beam.from_points_dir(pt_on_intersection, pt_on_beam2, beam3.frame.zaxis)

    return beam3, beam4


def beam_connection_short(beam1, beam2, t=0):
    """ find the shortest set of connection beams of the given two beams """

    beam1_flip = deepcopy(beam1)
    beam1_flip.frame = Frame(beam1_flip.frame.point, beam1_flip.frame.yaxis, beam1_flip.frame.xaxis)
    beam2_flip = deepcopy(beam2)
    beam2_flip.frame = Frame(beam2_flip.frame.point, beam2_flip.frame.yaxis, beam2_flip.frame.xaxis)

    lengths = []
    beams1, beams2 = [beam1, beam1_flip], [beam2, beam2_flip]
    beams_connection = []

    for b1  in beams1:
        for b2 in beams2:
            b3, b4 = beam_connection(b1, b2, t)
            beams_connection.append([b3, b4])
            lengths.append(b3.length + b4.length)
    
    shortest_length_index = sorted(range(len(lengths)), key=lambda x:lengths[x])[0]

    return beams_connection[shortest_length_index]




if __name__ == "__main__":
    pass