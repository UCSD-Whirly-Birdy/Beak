import numpy as np
import openmdao.api as om

from openmdao.api import Group

from openaerostruct.geometry.utils import generate_mesh, scale_x
from openaerostruct.geometry.geometry_group import Geometry
from openaerostruct.aerodynamics.aero_groups import AeroPoint

from .aerodynamics_geometry_group import AerodynamicsGeometryGroup


class HoverAerodynamicsGroup(Group):
    def initialize(self):
        self.options.declare('shape',types=tuple)

    def setup(self):
        shape = self.options['shape']