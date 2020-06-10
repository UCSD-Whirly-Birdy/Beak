import numpy as np 

from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import PowerCombinationComp

class RangeGroup(Group):
    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('g', default = 9.81)
        self.options.declare('EMD', default = 265.)
        self.options.declare('W0', default = 0.7*9.81)
        self.options.declare('Wb', default = 0.14*9.81)


    def setup(self):

        shape = self.options['shape']
        g = self.options['g']
        EMD = self.options['EMD']
        W0 = self.options['W0']
        Wb = self.options['Wb']

        # comp = IndepVarComp()
        # comp.add_output('efficiency') # Propellor Efficiency
        # comp.add_output('LD') # Lift to Drag Ratio
        # self.add_subsystem('inputs_comp', comp, promotes=['*'])
        # # self.add_subsystem('inputs_comp', comp)

        comp = PowerCombinationComp(
            shape = shape,
            out_name = 'range',
            coeff = EMD / g * Wb / W0,
            powers_dict = dict(
                efficiency = 1.,
                L_D = 1.,
            )
        )
        self.add_subsystem('range_comp', comp, promotes = ['*'])
        # self.add_subsystem('range_comp', comp)

        # self.connect('performance_analysis_group.range_group.efficiency', 'cruise_analysis_group.propulsion_group.efficiency')
        # self.connect('inputs_comp.efficiency', 'cruise_analysis_group.propulsion_group.rotor_group.efficiency_comp')
        # self.connect('inputs_comp.LD', 'atmosphere_group.altitude') Pull from cruise_aero later
