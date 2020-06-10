from openmdao.api import Group, IndepVarComp, ExecComp
from lsdo_utils.api import PowerCombinationComp
import numpy as np

# class HoverRadiusComp(ExplicitComponent):

#     def initialize(self):
#         self.options.declare('shape', types=tuple)

#     def setup(self):
#         self.add_input('wing_span')
#         self.add_input('sweep')
#         self.add_output('radius')

#         self.declare_partials('*','*')

#     def compute(self, inputs, outputs):
#         outputs['radius'] = inputs['wing_span']/(2.*np.cos(inputs['sweep']*np.pi/180))

#     def compute_partials(self, inputs, partials):
#         partials['radius','wing_span'] = 1./(2.*np.cos(inputs['sweep']*np.pi/180))
#         partials['radius','sweep'] = np.pi*inputs['wing_span']/360.*np.sin(np.pi/180.*inputs['sweep'])/(np.cos(np.pi/180.*inputs['sweep']))**2

class HoverVelocityGroup(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']

        # comp = IndepVarComp()
        # comp.add_output('hover_wing_angular_speed')
        # # if design variable, add as output in IVC
        # self.add_subsystem('inputs_comp', comp, promotes = ['*'])

        # make connections in run_group (aero_geom_group to this one for wing_span)
        
        # r = b/2/(cos(sweep))
        comp = ExecComp('radius = wing_span/2/(cos(sweep*pi/180))',shape=shape)
        self.add_subsystem('radius_comp', comp, promotes = ['*'])

        # ExecComp defines the equation and calculates given the equation/inputs 
        # Need to connect sweep/wingspan to this Group and then can compute the 
        # hover velocity below

        # V = 2pi*RPM/60*.75*radius or V = 2pi*RPM/60*.75* b/2/(cos(sweep))
        # V = omega * r

        comp = PowerCombinationComp(
            shape=shape,
            coeff = .75,
            out_name='hover_drag_velocity',
            powers_dict=dict(
                hover_wing_angular_speed = 1.,
                radius = 1.,
            )
        )
        self.add_subsystem('hover_drag_velocity_comp',comp,promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            coeff = .5,
            out_name='hover_torque_velocity',
            powers_dict=dict(
                hover_wing_angular_speed = 1.,
                wing_span = 1.,
            )
        )
        self.add_subsystem('hover_torque_velocity_comp',comp,promotes=['*'])