from openmdao.api import Group, IndepVarComp

from whirly_bird_optimization.cruise_equilibrium_group import HorizontalCruiseEqGroup, VerticalCruiseEqGroup
from whirly_bird_optimization.hover_equilibrium_group import TorqueHoverEqGroup, VerticalHoverEqGroup

class EquilibriumGroup(Group):
    def initialize(self):
        self.options.declare('shape',types=tuple)

    def setup(self):
        shape = self.options['shape']

        group = HorizontalCruiseEqGroup(
            shape=shape
        )
        self.add_subsystem('horizontal_cruise_group', group, promotes=['*'])

        group = VerticalCruiseEqGroup(
            shape=shape
        )
        self.add_subsystem('vertical_cruise_group', group, promotes=['*'])

        group = TorqueHoverEqGroup(
            shape=shape
        )
        self.add_subsystem('torque_hover_group', group, promotes=['*'])

        group = VerticalHoverEqGroup(
            shape=shape
        )
        self.add_subsystem('vertical_hover_group', group, promotes=['*'])
