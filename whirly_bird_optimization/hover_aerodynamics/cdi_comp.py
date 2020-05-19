import numpy as np

from openmdao.api import ExplicitComponent


class CDiComp(ExplicitComponent):

    def initialize(self):
        self.options.declare('e', types=float)

    def setup(self):
        self.add_input('CL')
        self.add_input('AR')
        self.add_output('CDi')

        self.declare_partials('CDi', 'CL')
        self.declare_partials('CDi', 'AR')

    def compute(self, inputs, outputs):
        e = self.options['e']

        CL = inputs['CL']
        AR = inputs['AR']

        outputs['CDi'] = CL ** 2. / np.pi / e / AR

    def compute_partials(self, inputs, partials):
        e = self.options['e']

        CL = inputs['CL']
        AR = inputs['AR']

        partials['CDi', 'CL'] = 2. * CL / np.pi / e / AR
        partials['CDi', 'AR'] = -CL ** 2. / np.pi / e / AR ** 2.
