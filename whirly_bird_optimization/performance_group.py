from openmdao.api import Group, IndepVarComp

from lsdo_utils.api import PowerCombinationComp

class PerformanceGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('g', default = 1.)
        self.options.declare('EMD', default = 1.)
        self.options.declare('W0', default = 1.)
        self.options.declare('Wb', default = 1.)


    def setup(self):

        shape = self.options['shape']
        g = self.options['g']
        EMD = self.options['EMD']
        W0 = self.options['W0']
        Wb = self.options['Wb']

        comp = IndepVarComp()
        comp.add_output('eta') # Propellor Efficiency
        comp.add_output('LD') # Lift to Drag Ratio
        self.add_subsystem('inputs_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape = shape,
            out_name = 'Range',
            coeff = g * EMD * Wb / W0,
            powers_dict = dict(
                eta = 1.,
                LD = 1.,
            )
        )
        self.add_subsystem('Range_comp', comp, promotes = ['*'])

        #self.connect('inputs_comp.eta', 'cruise_analysis_group.propulsion_group.rotor_group.efficiency_comp')
        # self.connect('inputs_comp.eta', 'atmosphere_group.altitude')



