import numpy as np 

from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import LinearPowerCombinationComp

# need to incorporate actual MAC, NP and CG calculations

class StabilityGroup(Group):
    def initialize(self):
        self.options.declare('shape',types=tuple)
        self.options.declare('chord',default=1.)

    def setup(self):

        shape = self.options['shape']
        MAC = self.options['chord']

        comp = LinearPowerCombinationComp(
            shape=shape,
            out_name = 'static_margin',
            terms_list = [
                (1/MAC, dict(
                    NP = 1.,
                )),
                (-1/MAC, dict(
                    CG = 1.,
                )),
            ]
        )
        self.add_subsystem('static_margin_comp',comp,promotes=['*'])