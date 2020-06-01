from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import PowerCombinationComp
import numpy as np

class HoverAeroVelocity(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)
        self.options.declare('b', default = 9.81)
        self.options.declare('sweep', default = 1.)

    def setup(self):
        shape = self.options['shape']
        b = self.options['b']
        sweep = self.options['sweep']

        # V = 2pi*RPM/60*.75r where r = b/(cos(sweep))
        comp = PowerCombinationComp(
            shape=shape,
            coeff = 2. * np.pi / 60. * .75 * b / np.cos(np.pi*sweep/180.),
            out_name='hover_inflow_velocity',
            powers_dict=dict(
                RPM = 1.
            )
        )
        self.add_subsystem('hover_inflow_velocity_comp',comp,promotes=['*'])