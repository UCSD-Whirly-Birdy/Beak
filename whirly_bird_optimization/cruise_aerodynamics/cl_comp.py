from openmdao.api import ExplicitComponent


class CLComp(ExplicitComponent):

    def setup(self):
        self.add_input('alpha')
        self.add_input('CLa')
        self.add_input('CL0')
        self.add_output('CL')

        self.declare_partials('CL', 'alpha')
        self.declare_partials('CL', 'CLa')
        self.declare_partials('CL', 'CL0', val=1.)

    def compute(self, inputs, outputs):
        alpha = inputs['alpha']
        CLa = inputs['CLa']
        CL0 = inputs['CL0']

        outputs['CL'] = CLa * alpha + CL0

    def compute_partials(self, inputs, partials):
        alpha = inputs['alpha']
        CLa = inputs['CLa']
        CL0 = inputs['CL0']

        partials['CL', 'alpha'] = CLa
        partials['CL', 'CLa'] = alpha
