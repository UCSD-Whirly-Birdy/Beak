rom openmdao.api import Group, IndepVarComp
from lsdo_utils.api import LinearPowerCombinationComp

#edit the following line:
#from whirly_bird_optimization.cruise_aerodynamics_group import NeutralPointGroup

class StabilityGroup(Group):
    def initialize(self):
        self.options.declare('shape',types=tuple)

    def setup(self):
        shape = self.options['shape']

        comp = LinearPowerCombinationComp(
            shape=shape,
            in_names = ['neutral_point','center_of_gravity'],
            out_name = 'static_margin',
            terms_list=[
                (dict(
                    neutral_point=1.,
                    mac=-1.
                )),
                (-1., dict(
                    center_of_gravity=1.
                    mac=-1.
                )),
            ]
        self.add_subsystem('horizontal_cruise_comp',comp, promotes = ['*'])