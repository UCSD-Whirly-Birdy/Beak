import numpy as np

from openmdao.api import Group, IndepVarComp

from lsdo_utils.api import PowerCombinationComp, ScalarExpansionComp, units

from lsdo_aircraft.simple_rotor.flow_angle_comp import FlowAngleComp
from lsdo_aircraft.simple_rotor.glauert_factor_comp import GlauertFactorComp
from lsdo_aircraft.simple_rotor.blade_drag_coeff_comp import BladeDragCoeffComp
from lsdo_aircraft.simple_rotor.eta1_comp import Eta1Comp
from lsdo_aircraft.simple_rotor.eta2_comp import Eta2Comp
from lsdo_aircraft.simple_rotor.eta3_comp import Eta3Comp


class ModifiedSimpleRotorGroup(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)
        self.options.declare('options_dictionary')

        self.promotes = None

    def setup(self):
        shape = self.options['shape']
        module = self.options['options_dictionary']

        blade_solidity = module['blade_solidity']
        integrated_design_lift_coeff = module['integrated_design_lift_coeff']

        # comp = IndepVarComp()
        # comp.add_output('radius_scalar')
        # self.add_subsystem('inputs_comp', comp, promotes=['*'])

        comp = ScalarExpansionComp(
            shape=shape,
            out_name='radius',
            in_name='radius_scalar',
        )
        self.add_subsystem('radius_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='diameter',
            coeff=2.,
            powers_dict=dict(
                radius=1.,
            )
        )
        self.add_subsystem('diameter_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='rotational_speed',
            coeff=1. / 2. / np.pi,
            powers_dict=dict(
                angular_speed=1.,
            )
        )
        self.add_subsystem('rotational_speed_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='power_coeff',
            powers_dict=dict(
                shaft_power=1.,
                density=-1.,
                rotational_speed=-3.,
                diameter=-5.,
            )
        )
        self.add_subsystem('power_coeff_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='tip_speed',
            powers_dict=dict(
                radius=1.,
                angular_speed=1.,
            )
        )
        self.add_subsystem('tip_speed_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='tip_mach',
            powers_dict=dict(
                tip_speed=1.,
                sonic_speed=-1.,
            )
        )
        self.add_subsystem('tip_mach_comp', comp, promotes=['*'])

        comp = FlowAngleComp(shape=shape)
        self.add_subsystem('flow_angle_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='advance_ratio',
            coeff=np.pi,
            powers_dict=dict(
                speed=1.,
                tip_speed=-1.,
            )
        )
        self.add_subsystem('advance_ratio_comp', comp, promotes=['*'])

        comp = GlauertFactorComp(shape=shape)
        self.add_subsystem('glauert_factor_comp', comp, promotes=['*'])

        comp = BladeDragCoeffComp(shape=shape, integrated_design_lift_coeff=integrated_design_lift_coeff)
        self.add_subsystem('blade_drag_coeff_comp', comp, promotes=['*'])

        comp = Eta1Comp(shape=shape, blade_solidity=blade_solidity)
        self.add_subsystem('eta1_comp', comp, promotes=['*'])

        comp = Eta2Comp(shape=shape)
        self.add_subsystem('eta2_comp', comp, promotes=['*'])

        comp = Eta3Comp(shape=shape, blade_solidity=blade_solidity)
        self.add_subsystem('eta3_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='efficiency',
            powers_dict=dict(
                eta1=1.,
                eta2=1.,
                eta3=1.,
            )
        )
        self.add_subsystem('efficiency_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='thrust_coeff',
            powers_dict=dict(
                efficiency=1.,
                power_coeff=1.,
                advance_ratio=-1.,
            )
        )
        self.add_subsystem('thrust_coeff_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='thrust',
            powers_dict=dict(
                thrust_coeff=1.,
                density=1.,
                rotational_speed=2.,
                diameter=4.,
            )
        )
        self.add_subsystem('thrust_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='blade_loading_coeff',
            coeff=1. / blade_solidity,
            powers_dict=dict(
                thrust_coeff=1.,
            )
        )
        self.add_subsystem('blade_loading_coeff_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='figure_of_merit',
            coeff=1. / np.sqrt(2 * np.pi),
            powers_dict=dict(
                thrust=1.5,
                density=-0.5,
                radius=-1.,
                shaft_power=-1.,
            )
        )
        self.add_subsystem('figure_of_merit_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='area',
            coeff=np.pi,
            powers_dict=dict(
                radius=2.,
            )
        )
        self.add_subsystem('area_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='disk_loading_lb_ft2',
            coeff=units('lbf/ft^2', 'N/m^2'),
            powers_dict=dict(
                thrust=1.,
                area=-1.,
            )
        )
        self.add_subsystem('disk_loading_lb_ft2_comp', comp, promotes=['*'])