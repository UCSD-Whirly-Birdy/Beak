# computes drag from rotor blades in hover using variable velocity 
# along the span of the wing
# D = 2 * CD * rho * pi^2 * RPM^2 * c * cos(lambda) * s^3
# where s is the distance along the span

import numpy as np

from openmdao.api import Group, IndepVarComp
# from lsdo_utils.api import PowerCombinationComp

# from openaerostruct_wb.py import prob['aero_point_0.wing_perf.CD']
from openaerostruct_wb import prob



# class HoverDrag(Group):

#     def initialize(self):
#         self.options.declare('shape', types=tuple)

#     def setup(self):
#         shape = self.options['shape']
        
#         comp = IndepVarComp()
#         #  need to figure out how to import drag coeff. from openaerostruct_wb
#         #  includes lines 4 & 5
#         # comp.add_output('CD')
#         # comp.add_output(prob['aero_point_0.wing_perf.CD'])

#         comp.add_output('CD')
#         comp.add_output('rho')
#         comp.add_output('RPM_Hover')
#         comp.add_output('c')
#         comp.add_output('lambda')
#         comp.add_output('s')




print("Wing CD:", prob['aero_point_0.wing_perf.CD'])