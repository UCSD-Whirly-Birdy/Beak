from openmdao.api import Group, IndepVarComp

from cruise_equilibrium_group import HorizontalCruiseEqGroup, VerticalCruiseEqGroup
from whirly_bird_optimization.hover_equilibrium_group import TorqueHoverEqGroup, VerticalHoverEqGroup

from aerodynamics_geom_group import AerodynamicsGeomGroup
from cruise_aero_group import CruiseAeroGroup
from cruise_lift_drag_group import CruiseLiftDragGroup
from cruise_equilibrium_group import HorizontalCruiseEqGroup, VerticalCruiseEqGroup


class EquilibriumGroup(Group):
    def initialize(self):
        self.options.declare('shape',types=tuple)

    def setup(self):
        shape = self.options['shape']

        group = VerticalCruiseEqGroup(
            shape=shape
        )
        self.add_subsystem('cruise_equilibrium_group', group, promotes=['*'])

        group = HorizontalCruiseEqGroup(
            shape=shape
        )
        self.add_subsystem('cruise_equilibrium_group', group, promotes=['*'])

        group = CruiseLiftDragGroup(
            shape=shape
        )
        self.add_subsystem('cruise_lift_drag_group', group, promotes=['*'])

        group = CruiseAeroGroup(
            shape=shape
        )
        self.add_subsystem('cruise_aero_group', group, promotes=['*'])

        group = AerodynamicsGeomGroup(
            shape=shape
        )
        self.add_subsystem('aerodynamics_geom_group',group, promotes=['*'])

