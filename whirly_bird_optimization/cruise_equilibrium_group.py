from openmdao.api import Group, IndepVarComp, Problem
from lsdo_utils.api import LinearCombinationComp

# prob = Problem()

class HorizontalCruiseEqGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('thrust_cruise') # update variable name later
        self.options.declare('drag_cruise') # update variable name later

    def setup(self):
        shape = self.options['shape']
        # thrust_cruise = self.options['thrust_cruise']
        # drag_cruise = self.options['drag_cruise']

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['thrust_cruise','drag_cruise'],
            out_name = 'horizontal_cruise_eq',
            coeffs = [1., -1.],
        )
        self.add_subsystem('horizontal_cruise_comp',comp, promotes = ['*'])

class VerticalCruiseEqGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('lift_cruise') # update variable name later
        self.options.declare('weight') # update variable name later

    def setup(self):
        shape = self.options['shape']

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['lift_cruise','weight'],
            out_name = 'vertical_cruise_eq',
            coeffs = [1., -1.],
        )
        self.add_subsystem('vertical_cruise_comp',comp, promotes = ['*'])
