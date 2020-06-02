from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import PowerCombinationComp

from whirly_bird_optimization.aerodynamics_mesh_group import AerodynamicsMeshGroup

class CruiseDragGroup(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']
        
        comp = IndepVarComp()
        comp.add_output('C_D')
        comp.add_output('speed')
        comp.add_output('density')
        comp.add_output('wing_area')
        self.add_subsystem('inputs_comp', comp, promotes=['*'])

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
