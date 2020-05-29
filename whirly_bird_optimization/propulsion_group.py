from openmdao.api import Group, IndepVarComp

from lsdo_utils.api import PowerCombinationComp
from lsdo_aircraft.simple_rotor.simple_rotor import SimpleRotor
from lsdo_aircraft.simple_rotor.simple_rotor_group import SimpleRotorGroup
from lsdo_aircraft.simple_motor.simple_motor import SimpleMotor
from lsdo_aircraft.simple_motor.simple_motor_group import SimpleMotorGroup


class PropulsionGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

        # comp = IndepVarComp()
        # comp.add_output('thrust')
        # comp.add_output('efficiency')
        # self.add_subsystem('inputs_comp', comp, promotes=['*'])

        simple_motor = SimpleMotor(
            name='glauert_model',
        )
        group = SimpleMotorGroup(
            shape=shape,
            options_dictionary=simple_motor,
        )
        self.add_subsystem('motor_group', group, promotes=['*'])

        simple_rotor = SimpleRotor(
            name='glauert_model',
            integrated_design_lift_coeff=0.3,
            blade_solidity=0.15,
        )
        group = SimpleRotorGroup(
            shape=shape,
            options_dictionary=simple_rotor,
        )
        self.add_subsystem('rotor_group', group, promotes=['*'])
        