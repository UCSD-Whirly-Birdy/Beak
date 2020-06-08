from openmdao.api import Problem, Group, IndepVarComp


from lsdo_utils.api import PowerCombinationComp
from lsdo_aircraft.simple_rotor.simple_rotor import SimpleRotor
from lsdo_aircraft.simple_rotor.simple_rotor_group import SimpleRotorGroup
from lsdo_aircraft.simple_motor.simple_motor import SimpleMotor
from lsdo_aircraft.simple_motor.simple_motor_group import SimpleMotorGroup

from .aerodynamics_geometry_group import AerodynamicsGeometryGroup
from .blade_solidity_comp import BladeSolidity

class CruisePropulsionGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        #self.options.declare('mode', types = str)

    def setup(self):
        shape = self.options['shape']
        #mode = self.options['mode']

        comp = BladeSolidity(
            shape=shape
        )
        self.add_subsystem('blade_solidity_comp', comp, promotes=['*'])
        
        simple_motor = SimpleMotor(
        name='glauert_model',
        specific_power_kW_kg=8.,
        number_of_poles_per_phase=6.,
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