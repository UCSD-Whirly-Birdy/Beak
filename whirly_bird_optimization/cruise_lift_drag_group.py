from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import PowerCombinationComp

class CruiseLiftDragGroup(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']
        
        # comp = IndepVarComp()
        # comp.add_output('C_D')
        # comp.add_output('C_L')
        # comp.add_output('speed')
        # comp.add_output('density')
        # comp.add_output('area')
        # self.add_subsystem('inputs_comp', comp, promotes=['*'])

        # # D = 0.5 * rho * v^2 * C_D * S
        # comp = PowerCombinationComp(
        #     shape=shape,
        #     out_name='cruise_drag',
        #     coeff=0.5,
        #     powers_dict=dict(
        #         area=1.,
        #         C_D=1,
        #         speed=2.,
        #         density=1.
        #     )
        # )
        # self.add_subsystem('cruise_drag_comp', comp, promotes=['*'])

        # # L = 0.5 * rho * v^2 * C_L * S
        # comp = PowerCombinationComp(
        #     shape=shape,
        #     out_name='cruise_lift',
        #     coeff=0.5,
        #     powers_dict=dict(
        #         area=1.,
        #         C_L=1,
        #         speed=2.,
        #         density=1.
        #     )
        # )
        # self.add_subsystem('cruise_lift_comp', comp, promotes=['*'])

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

