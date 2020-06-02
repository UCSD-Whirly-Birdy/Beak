from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import LinearCombinationComp

class TorqueHoverEqGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('thrust_torque_hover') # update variable name later
        self.options.declare('drag_torque_hover') # update variable name later
        # need to import optimized sweep angle, wing span for thrust torque
        # import separate OAS calculation for previous dimensions to find CD
        # at 3/4 of wingspan (average of parabola-shaped drag distribution)

    def setup(self):
        shape = self.options['shape']

        comp = IndepVarComp()
        comp.add_output('thrust_torque_hover')
        comp.add_output('drag_torque_hover')

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['thrust_torque_hover','drag_torque_hover'],
            out_name = 'torque_hover_eq',
            coeffs = [1., -1.],
        )
        self.add_subsystem('torque_hover_comp', comp, promotes = ['*'])

class VerticalHoverEqGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('lift_hover') # update variable name later
        self.options.declare('weight') # update variable name later

    def setup(self):
        shape = self.options['shape']

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['lift_hover','weight'],
            out_name = 'vertical_hover_eq',
            coeffs = [1., -1.],
        )
        self.add_subsystem('vertical_hover_comp',comp, promotes = ['*'])
