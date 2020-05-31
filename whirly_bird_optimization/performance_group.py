from openmdao.api import Group, IndepVarComp

from whirly_bird_optimization.range_comp import RangeGroup
from whirly_bird_optimization.stability_group import StabilityGroup

class PerformanceGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

        # comp = IndepVarComp()
        # comp.add_output('efficiency') # Propellor Efficiency
        # comp.add_output('LD') # Lift to Drag Ratio
        # # comp.add_output()
        # self.add_subsystem('inputs_comp',comp,promotes=['*'])

        group = RangeGroup(
            shape=shape,
        )
        self.add_subsystem('range_group',group)
  
        group = StabilityGroup(
            shape=shape,
        )
        self.add_subsystem('stability_group',group)