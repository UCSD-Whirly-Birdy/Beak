from openmdao.api import Group, IndepVarComp

from .aerodynamics_geom_group import AerodynamicsGeomGroup
# from .cruise_aero_group import CruiseAeroGroup
from .cruise_lift_drag_group import CruiseLiftDragGroup


class AerodynamicsGroup(Group):
    def initialize(self):
        self.options.declare('shape',types=tuple)

    def setup(self):
        shape = self.options['shape']

        group = CruiseLiftDragGroup(
            shape=shape
        )
        self.add_subsystem('cruise_lift_drag_group', group, promotes=['*'])

        # group = CruiseAeroGroup(
        #     shape=shape
        # )
        # self.add_subsystem('cruise_aero_group', group, promotes=['*'])

        group = AerodynamicsGeomGroup(
            shape=shape
        )
        self.add_subsystem('aerodynamics_geom_group',group, promotes=['*'])