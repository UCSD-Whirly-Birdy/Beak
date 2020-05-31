from openmdao.api import Group, IndepVarComp, Problem
from lsdo_utils.api import LinearCombinationComp

# prob = Problem()

class HorizontalCruiseEqGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('thrust_cruise')
        self.options.declare('drag_cruise')

    def setup(self):
        shape = self.options['shape']
        # thrust_cruise = self.options['thrust_cruise']
        # drag_cruise = self.options['drag_cruise']

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['thrust_cruise','drag_cruise'],
            out_name = 'horizontal_force_eq',
            coeffs = [1., -1.],
        )
        self.add_subsystem('horizontal_cruise_comp',comp, promotes = ['*'])

class VerticalCruiseEqGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']
