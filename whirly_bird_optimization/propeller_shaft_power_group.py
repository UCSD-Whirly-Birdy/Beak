import numpy as np 
from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import PowerCombinationComp

class PropellerShaftPowerGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']

        comp = IndepVarComp()
        comp.add_output('motor_efficiency')
        comp.add_output('voltage')
        self.add_subsystem('inputs_comp', comp, promotes = ['*'])

        comp = PowerCombinationComp(
            shape = shape,
            out_name = 'propeller_shaft_power',
            coeff = 1.,
            powers_dict = dict(
                motor_efficiency = 1.,
                voltage = 1.,
                current = 1.,
            )
        )
        self.add_subsystem('propeller_shaft_power_comp', comp)
