from openmdao.api import Group, IndepVarComp

from lsdo_utils.api import PowerCombinationComp
#from lsdo_aircraft.simple_motor.simple_motor import SimpleMotor
#from lsdo_aircraft.simple_motor.simple_motor_group import SimpleMotorGroup


class AerodynamicsGroup(Group):

    def initialize(self):
        self.options.declare('shape', types = tuple)

    # def setup(self):
    #     shape = self.options['shape']

    #     comp = IndepVarComp()
    #     comp.add_output('C_L')
    #     comp.add_output('area')
    #     self.add_subsystem('inputs_comp', comp, promotes=['*'])


    def setup(self):
        shape = self.options['shape']
        
        comp = IndepVarComp()
        comp.add_output('area')
        comp.add_output('AR')
        self.add_subsystem('inputs_comp', comp, promotes=['*'])

        # b = sqrt(AR * S)
        comp = PowerCombinationComp(
            shape=shape,
            out_name='wing_span',
            powers_dict=dict(
                AR=0.5,
                area=0.5,
            )
        )
        self.add_subsystem('wing_span_comp', comp, promotes=['*'])

        # c = b / AR
        comp = PowerCombinationComp(
            shape=shape,
            out_name='wing_chord',
            powers_dict=dict(
                AR=-1.,
                wing_span=1.,
            )
        )
        self.add_subsystem('wing_chord_comp', comp, promotes=['*'])
        

        