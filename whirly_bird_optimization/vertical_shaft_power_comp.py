import numpy as np
from openmdao.api import Group, IndepVarComp, ExecComp
from lsdo_utils.api import PowerCombinationComp, LinearCombinationComp

class VerticalShaftPower(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']

        comp = ExecComp('thrust_torque_hover = thrust * wing_span', shape=shape)
        self.add_subsystem('thrust_torque_hover_comp', comp, promotes = ['*'])

        comp = ExecComp('drag_torque_hover = drag * radius * 1.5', shape=shape)
        self.add_subsystem('drag_torque_hover_comp', comp, promotes = ['*'])

        comp = LinearCombinationComp(
            shape = shape,
            in_names = ['thrust_torque_hover', 'drag_torque_hover'],
            out_name = 'vertical_torque',
            coeffs = [1., -1.]
        )

        self.add_subsystem('vertical_torque_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape = shape,
            out_name = 'vertical_shaft_power',
            coeff = 1.,
            powers_dict = dict(
                vertical_torque = 1.,
                hover_wing_angular_speed = 1.,
            )
        )
        self.add_subsystem('vertical_shaft_power_comp', comp, promotes = ['*'])