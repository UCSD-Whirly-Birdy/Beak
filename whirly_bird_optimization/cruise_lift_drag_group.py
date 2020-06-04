from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import PowerCombinationComp

from cruise_aero_group import prob as CAOS
from analysis_group import AtmosphereGroup

class CruiseLiftDragGroup(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']
        
        comp = IndepVarComp()
        comp.add_output('C_D', val=CAOS['laura.CD']) # connect to CD from cruise_oas
        comp.add_output('C_L', val=CAOS['laura.CL']) # connect to CL from cruise_oas
        comp.add_output('speed', val=50, units='m/s')
        comp.add_output('density', val=1.225)
        comp.add_output('wing_area')
        self.add_subsystem('inputs_comp', comp, promotes=['*'])
        self.connect('analysis_group.atmosphere_group.density', 'density')


        # D = 0.5 * rho * v^2 * C_D * S
        comp = PowerCombinationComp(
            shape=shape,
            out_name='cruise_drag',
            coeff=0.5,
            powers_dict=dict(
                wing_area=1.,
                C_D=1,
                speed=2.,
                density=1.
            )
        )
        self.add_subsystem('cruise_drag_comp', comp, promotes=['*'])

        # L = 0.5 * rho * v^2 * C_L * S
        comp = PowerCombinationComp(
            shape=shape,
            out_name='cruise_lift',
            coeff=0.5,
            powers_dict=dict(
                wing_area=1.,
                C_L=1,
                speed=2.,
                density=1.
            )
        )
        self.add_subsystem('cruise_lift_comp', comp, promotes=['*'])

        # L_D = C_L/C_D
        comp = PowerCombinationComp(
            shape=shape,
            out_name='L_D',
            powers_dict=dict(
                C_L=1,
                C_D=-1.
            )
        )
        self.add_subsystem('L_D_comp', comp, promotes=['*'])
