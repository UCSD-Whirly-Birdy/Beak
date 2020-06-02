from openmdao.api import Group, IndepVarComp, Problem

from whirly_bird_optimization.range_comp import RangeGroup
from whirly_bird_optimization.equilibrium_group import EquilibriumGroup
from whirly_bird_optimization.stability_group import StabilityGroup

# need to import stability portion for static margin

class PerformanceGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

        comp = IndepVarComp()

        comp.add_output('weight') # weight
        self.add_subsystem('inputs_comp',comp,promotes=['*'])
  
        group = EquilibriumGroup(
            shape=shape,
        )
        self.add_subsystem('equilibrium_group',group, promotes = ['*'])

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
        self.connect('weight', 'vertical_cruise_group.weight')
        self.connect('weight', 'vertical_hover_group.weight')
