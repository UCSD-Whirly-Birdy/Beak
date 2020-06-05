from openmdao.api import Group, IndepVarComp

from lsdo_aircraft.atmosphere.atmosphere import Atmosphere
from lsdo_aircraft.atmosphere.atmosphere_group import AtmosphereGroup

from whirly_bird_optimization.aerodynamics_group import AerodynamicsGroup
from whirly_bird_optimization.propulsion_group import PropulsionGroup


class AnalysisGroup(Group):
    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('mode', types = str)

    def setup(self):
        shape = self.options['shape']
        # mode = self.options['mode']

        comp = IndepVarComp()
        comp.add_output('altitude')
        comp.add_output('speed')
        self.add_subsystem('inputs_comp', comp)

        group = AtmosphereGroup(
            shape=shape,
            options_dictionary=Atmosphere,
            # mode=mode,
        )
        self.add_subsystem('atmosphere_group', group)

        group = AerodynamicsGroup(
            shape=shape,
            # mode=mode,
       )
        self.add_subsystem('aerodynamics_group', group)

        group = PropulsionGroup(
            shape=shape,
        )
        self.add_subsystem('propulsion_group', group)
        # if mode == 'cruise':
        #     self.add_subsystem('cruise_propulsion_group', group)
        # else:
        #     self.add_subsystem('hover_propulsion_group', group)

        self.connect('inputs_comp.altitude', 'atmosphere_group.altitude')
        self.connect('inputs_comp.speed', 'atmosphere_group.speed')
        self.connect('inputs_comp.speed', 'propulsion_group.speed')
        self.connect('atmosphere_group.sonic_speed', 'propulsion_group.sonic_speed')
        self.connect('atmosphere_group.density', 'propulsion_group.density')
       # self.connect('cruise_analysis_group.propulsion_group.radius_scalar', 'cruise_analysis_group.propulsion_group.rotor_group.radius_comp.radius_scalar')

