from openmdao.api import Group, IndepVarComp, ExplicitComponent
from lsdo_utils.api import PowerCombinationComp
import numpy as np

# r = b/(cos(sweep))
class HoverRadiusComp(ExplicitComponent):
    def setup(self):
        self.add_input('wing_span')
        self.add_input('sweep')
        self.add_output('radius')

        self.declare_partials('*','*')

    def compute(self, inputs, outputs):
        outputs['radius'] = inputs['wing_span']/(2.*np.cos(inputs['sweep']*np.pi/180))

    def compute_partials(self, inputs, partials):
        partials['radius','wing_span'] = 1./(2.*np.cos(inputs['sweep']*np.pi/180))
        partials['radius','sweep'] = np.pi*inputs['wing_span']/360.*np.sin(np.pi/180.*inputs['sweep'])/(np.cos(np.pi/180.*inputs['sweep']))**2

class HoverAeroVelocity(Group):

    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']

        comp = IndepVarComp()
        comp.add_output('hover_RPM')
        comp.add_output('radius')
        self.add_subsystem('inputs_comp', comp, promotes = ['*'])

        # V = 2pi*RPM/60*.75*radius 

        comp = PowerCombinationComp(
            shape=shape,
            coeff = 2. * np.pi / 60. * .75,
            out_name='hover_velocity',
            powers_dict=dict(
                hover_RPM = 1.,
                radius = 1.,
            )
        )
        self.add_subsystem('hover_velocity_comp',comp,promotes=['*'])