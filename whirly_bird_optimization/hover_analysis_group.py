from openmdao.api import Group, IndepVarComp

from lsdo_aircraft.atmosphere.atmosphere import Atmosphere
from lsdo_aircraft.atmosphere.atmosphere_group import AtmosphereGroup

from whirly_bird_optimization.hover_aerodynamics_group import HoverAerodynamicsGroup
from whirly_bird_optimization.hover_propulsion_group import HoverPropulsionGroup
from whirly_bird_optimization.hover_velocity_group import HoverVelocityGroup


class HoverAnalysisGroup(Group):
    def initialize(self):
        self.options.declare('shape', types = tuple)
        #self.options.declare('mode', types = str)

    def setup(self):
        shape = self.options['shape']


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

        # group = HoverVelocityGroup(
        #     shape=shape,
        # )
        # self.add_subsystem('hover_velocity_group', group)

        group = HoverAerodynamicsGroup(
            shape=shape,
            # mode=mode,
        )
        self.add_subsystem('hover_aerodynamics_group', group)

        group = HoverPropulsionGroup(
            shape=shape,
        )
        self.add_subsystem('hover_propulsion_group', group)

        self.connect('inputs_comp.altitude', 'atmosphere_group.altitude')
        self.connect('inputs_comp.speed', 'atmosphere_group.speed')
        #self.connect('inputs_comp.speed', 'hover_propulsion_group.speed')
        #self.connect('atmosphere_group.sonic_speed', 'hover_propulsion_group.sonic_speed')
        #self.connect('atmosphere_group.density', 'hover_propulsion_group.density')
        #self.connect('hover_analysis_group.hover_propulsion_group.radius_scalar', 'cruise_analysis_group.propulsion_group.rotor_group.radius_comp.radius_scalar')

