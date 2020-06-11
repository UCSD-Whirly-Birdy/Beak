from openmdao.api import Problem, Group, IndepVarComp


from lsdo_utils.api import PowerCombinationComp
from lsdo_aircraft.simple_rotor.simple_rotor import SimpleRotor
from lsdo_aircraft.simple_rotor.simple_rotor_group import SimpleRotorGroup
from whirly_bird_optimization.modified_simple_rotor_group import ModifiedSimpleRotorGroup
from lsdo_aircraft.simple_motor.simple_motor import SimpleMotor
from lsdo_aircraft.simple_motor.simple_motor_group import SimpleMotorGroup

#from .aerodynamics_geometry_group import AerodynamicsGeometryGroup
from .propeller_shaft_power_group import PropellerShaftPowerGroup
from .vertical_shaft_power_comp import VerticalShaftPower

class HoverPropulsionGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        #self.options.declare('mode', types = str)

    def setup(self):
        shape = self.options['shape']
    
        # simple_motor = SimpleMotor(
        # name='glauert_model',
        # )
        # group = SimpleMotorGroup(
        #     shape=shape,
        #     options_dictionary=simple_motor,
        #     )
        # self.add_subsystem('rotational_motor_group', group, promotes=['*'])

        group = PropellerShaftPowerGroup(
            shape = shape,
        )
        self.add_subsystem('propeller_shaft_power_group', group, promotes = ['*'])

        simple_rotor_1 = SimpleRotor(
            name='glauert_model',
            integrated_design_lift_coeff=0.3, 
            blade_solidity=0.15, 
            )
        group = SimpleRotorGroup(
            shape=shape,
            options_dictionary=simple_rotor_1,
            )
        self.add_subsystem('rotational_rotor_group', group)

        group = VerticalShaftPower(
            shape = shape,
        )
        self.add_subsystem('vertical_shaft_power_group', group, promotes = ['*'])

        simple_rotor_2 = SimpleRotor(
            name='glauert_model',
            integrated_design_lift_coeff=0.5, 
            blade_solidity=0.15, 
            )
        group = ModifiedSimpleRotorGroup(
            shape=shape,
            options_dictionary=simple_rotor_2,
            )
        self.add_subsystem('vertical_rotor_group', group)