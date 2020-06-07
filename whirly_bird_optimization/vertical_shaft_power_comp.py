import numpy as np
from openmdao.api import Group, IndepVarComp, ExecComp
from lsdo_utils.api import PowerCombinationComp

class VerticalShaftPower(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']

        comp = ExecComp('vertical_torque = thrust * wing_span' + 
        '- drag * wing_span / cos(sweep*pi/180) * .75', shape=shape)
        self.add_subsystem('vertical_torque_comp', comp, promotes = ['*'])

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