from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import LinearCombinationComp

class EqualGeometryGroup(Group):
    def initialize(self):
        self.options.declare('shape',types=tuple)

    def setup(self):
        shape = self.options['shape']

        comp = LinearCombinationComp(
            shape=(3,1),
            in_names = ['cruise_twist','hover_twist'],
            out_name = 'twist_equality',
            coeffs = [1., -1.],
        )
        self.add_subsystem('twist_equality_comp',comp, promotes = ['*'])

        comp = LinearCombinationComp(
            shape=shape,
            in_names = ['cruise_sweep','hover_sweep'],
            out_name = 'sweep_equality',
            coeffs = [1., -1.],
        )
        self.add_subsystem('sweep_equality_comp',comp, promotes = ['*'])