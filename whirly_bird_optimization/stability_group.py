from openmdao.api import Group, IndepVarComp, ExecComp
from lsdo_utils.api import LinearPowerCombinationComp
import numpy as np
from lsdo_aircraft.simple_motor.simple_motor import SimpleMotor
from lsdo_aircraft.simple_motor.simple_motor_group import SimpleMotorGroup

class StabilityGroup(Group):
    def initialize(self):
        self.options.declare('shape',types=tuple)

    def setup(self):
        shape = self.options['shape']

        # comp = IndepVarComp()
        # # comp.add_output('sweep')
        # comp.add_output('body_weight_ratio') # weight of wing/total weight
        # comp.add_output('wing_to_total_weight_ratio') # weight of wing/total weight
        # comp.add_output('motor_weight_ratio') # weight of wing/total weight
        # self.add_subsystem('inputs_comp',comp, promotes = ['*'])

        comp = ExecComp('neutral_point = (chord + wing_span*tan(sweep*pi/180))/4', shape=shape)
        self.add_subsystem('neutral_point_comp', comp, promotes = ['*'])

        comp = ExecComp('center_of_gravity = ' + 
            'body_weight_ratio*chord/2 + ' +
            'wing_weight_ratio*(wing_span*tan(sweep*pi/180)/4 + chord/2) + ' + 
            'motor_weight_ratio*(wing_span*tan(sweep*pi/180)/2 + chord/2)', shape=shape)
        self.add_subsystem('center_of_gravity_comp', comp, promotes = ['*'])

        comp = LinearPowerCombinationComp(
            shape=shape,
            in_names = ['neutral_point','center_of_gravity', 'mean_aerodynamic_chord'],
            out_name = 'static_margin',
            terms_list=[
                (1., dict(
                    neutral_point=1.,
                    mean_aerodynamic_chord=-1.,
                )),
                (-1., dict(
                    center_of_gravity=1.,
                    mean_aerodynamic_chord=-1.,
                )),
            ]
       )
        self.add_subsystem('static_margin_comp',comp, promotes = ['*'])