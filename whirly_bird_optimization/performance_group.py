from openmdao.api import Group, IndepVarComp, Problem

from whirly_bird_optimization.range_comp import RangeGroup
from whirly_bird_optimization.force_balance_group import ForceBalanceGroup
from whirly_bird_optimization.stability_group import StabilityGroup
from whirly_bird_optimization.equal_geometry_group import EqualGeometryGroup


class PerformanceGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

        comp = IndepVarComp()

        comp.add_output('weight') # weight
        self.add_subsystem('inputs_comp',comp,promotes=['*'])

        group = EqualGeometryGroup(
            shape=shape,
        )
        self.add_subsystem('equal_geometry_group',group, promotes = ['*'])

        group = ForceBalanceGroup(
            shape=shape,
        )
        self.add_subsystem('force_balance_group',group, promotes = ['*'])

        group = StabilityGroup(
            shape=shape,
        )
        self.add_subsystem('stability_group',group, promotes = ['*'])

        group = RangeGroup(
            shape=shape,
        )
        self.add_subsystem('range_group',group, promotes = ['*'])
        

        # self.connect('cruise_analysis_group.propulsion_group.rotor_group.efficiency_comp.efficiency','efficiency')
        # self.connect('efficiency_comp.efficiency','efficiency')
        #self.connect('weight', 'vertical_cruise_group.weight')
        #self.connect('weight', 'vertical_hover_group.weight')
