from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import PowerCombinationComp
import numpy as np


class BladeSolidity(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']
        
        # comp = IndepVarComp()
        # comp.add_output('wing_span')
        # comp.add_output('wing_area')
        # self.add_subsystem('inputs_comp', comp, promotes=['*'])

        # sigma = 8 * S / pi / b
        comp = PowerCombinationComp(
            shape=shape,
            out_name='blade_solidity',
            coeff=8/np.pi,
            powers_dict=dict(
                wing_area=1.,
                wing_span=-1.,
            )
        )
        self.add_subsystem('blade_solidity_comp', comp, promotes=['*'])
