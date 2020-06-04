from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import LinearCombinationComp

# from whirly_bird_optimization.cruise_equilibrium_group import HorizontalCruiseEqGroup, VerticalCruiseEqGroup
#from whirly_bird_optimization.hover_equilibrium_group import TorqueHoverEqGroup, VerticalHoverEqGroup

class EquilibriumGroup(Group):
    def initialize(self):
        self.options.declare('shape',types=tuple)

    def setup(self):
        shape = self.options['shape']

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['thrust_cruise','drag_cruise'],
            out_name = 'horizontal_cruise_eq',
            coeffs = [1., -1.],
        )
        self.add_subsystem('horizontal_cruise_comp',comp, promotes = ['*'])

        # group = HorizontalCruiseEqGroup(
        #     shape=shape
        # )
        # self.add_subsystem('horizontal_cruise_group',group)

        # group = VerticalCruiseEqGroup(
        #     shape=shape
        # )
        # self.add_subsystem('vertical_cruise_group',group)

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['lift_cruise','weight'],
            out_name = 'vertical_cruise_eq',
            coeffs = [1., -1.],
        )
        self.add_subsystem('vertical_cruise_comp',comp, promotes = ['*'])


        # group = VerticalCruiseEqGroup(
        #     shape=shape
        # )
        # self.add_subsystem('vertical_cruise_group', group, promotes=['*'])

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['thrust_torque_hover','drag_torque_hover'],
            out_name = 'torque_hover_eq',
            coeffs = [1., -1.],
        )
        self.add_subsystem('torque_hover_comp',comp, promotes = ['*'])
        
        # group = TorqueHoverEqGroup(
        #     shape=shape
        # )
        # self.add_subsystem('torque_hover_group', group, promotes=['*'])

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['lift_hover','weight'],
            out_name = 'vertical_hover_eq',
            coeffs = [1., -1.],
        )
        self.add_subsystem('vertical_hover_comp',comp, promotes = ['*'])

        # group = VerticalHoverEqGroup(
        #     shape=shape
        # )
        # self.add_subsystem('vertical_hover_group', group, promotes=['*'])
