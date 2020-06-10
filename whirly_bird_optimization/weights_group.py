from openmdao.api import Group, IndepVarComp, ExecComp
import numpy as np 

class WeightsGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']

        comp = ExecComp('motor_weight_ratio = motor_mass / total_mass', shape=shape) # need to define motor_mass and connect to mass in simple_motor_group
        self.add_subsystem('motor_weight_ratio_comp', comp, promotes = ['*'])

        comp = ExecComp('body_to_wing_weight_ratio = (1 - 2 * motor_weight_ratio)/(wing_weight_ratio) - 1', shape=shape)
        self.add_subsystem('body_to_wing_weight_ratio_comp', comp, promotes = ['*'])

        comp = ExecComp('body_weight_ratio = body_to_wing_weight_ratio * wing_weight_ratio', shape=shape)
        self.add_subsystem('body_weight_ratio_comp', comp, promotes = ['*'])