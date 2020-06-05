from openmdao.api import Problem, Group, IndepVarComp


from lsdo_utils.api import PowerCombinationComp
from lsdo_aircraft.simple_rotor.simple_rotor import SimpleRotor
from lsdo_aircraft.simple_rotor.simple_rotor_group import SimpleRotorGroup
from lsdo_aircraft.simple_motor.simple_motor import SimpleMotor
from lsdo_aircraft.simple_motor.simple_motor_group import SimpleMotorGroup

from .aerodynamics_geometry_group import AerodynamicsGeometryGroup
from .blade_solidity_comp import BladeSolidity

class HoverPropulsionGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('mode', types = str)

    def setup(self):
        shape = self.options['shape']
