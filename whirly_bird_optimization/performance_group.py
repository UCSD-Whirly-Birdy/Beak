from openmdao.api import Group, IndepVarComp

from lsdo_utils.api import PowerCombinationComp
from whirly_bird_optimization.range_comp import RangeComp
# from whirly_bird_optimization.stability_group import 

class PerformanceGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

        comp = RangeComp(
            shape=shape,
        )
        self.add_subsystem('range_comp',comp)
  
        # group = StabilityGroup(
        #     shape=shape,
        # )
        # self.add_subsystem('stability_group',group)