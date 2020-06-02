# this file imports the optimized geometry and velocity tangential to the wing
# in hover to determine the lift and drag coefficients

# need to fix prob for geometry inputs bc prob doesn't work

import numpy as np
import openmdao.api as om

from openaerostruct.geometry.utils import generate_mesh
from openaerostruct.geometry.geometry_group import Geometry
from openaerostruct.aerodynamics.aero_groups import AeroPoint

# from openaerostruct_wb import prob
# from cruise_aero_geom import AerodynamicsGeom
from hover_aero_geom import HoverAeroVelocity

# need to import geometry from cruise_aero
# we don't want to optimize, but rather find CD and CL for the optimized geometry from
# cruise aero computation where the velocity is equal to (2pi)/60*RPM*.75r (averaged 
# or centroid drag value in parabolic shape)

shape = (1,)

prob = om.Problem()

indep_var_comp = om.IndepVarComp()
# indep_var_comp.add_output('v', val=self.setup['hover_inflow_velocity'], units='m/s') # update velocity value
indep_var_comp.add_output('v', val=50, units='m/s')
indep_var_comp.add_output('Mach_number', val=0.3)
indep_var_comp.add_output('re', val=1.e6, units='1/m')
indep_var_comp.add_output('rho', val=1.225, units='kg/m**3')
indep_var_comp.add_output('cg', val=np.zeros((3)), units='m')
indep_var_comp.add_output('alpha', val = 2.)

mesh_dict = {
        'num_y' : 15,
        'num_x' : 7,
        'wing_type' : 'rect',
        'symmetry' : True,
        'span' : prob['wing_span'],
        'chord' : prob['wing_chord'],
}

mesh = generate_mesh(mesh_dict)
# need to edit these to mimic the result of optimization from CRUISE
surface = {
        'name' : 'hover_wing',
        'symmetry' : True,
        'S_ref_type' : 'wetted',
        'twist_cp' : np.zeros(prob['wing.twist_cp']),
        'mesh' : mesh,
        'CL0' : 0.0,
        'CD0' : 0.001,
        'k_lam' : 0.05,
        't_over_c_cp' : np.array([0.1875]),
        'c_max_t' : 0.1,
        'with_viscous' : True,
        'with_wave' : False,
        'sweep' : (prob['wing.sweep']),
        'alpha' : (prob['aero_point_0.alpha']),
}

geom_group = Geometry(surface=surface)

aero_group = AeroPoint(surfaces=[surface])
point_name = 'aero_point_0'
prob.model.add_subsystem(point_name, aero_group)

# Connect flow properties to the analysis point
prob.model.connect('v', point_name + '.v')
# prob.model.connect('alpha', point_name + '.alpha')
prob.model.connect('Mach_number', point_name + '.Mach_number')
prob.model.connect('re', point_name + '.re')
prob.model.connect('rho', point_name + '.rho')
prob.model.connect('cg', point_name + '.cg')

name = 'wing'

# Connect the mesh from the geometry component to the analysis point
prob.model.connect('wing.mesh', 'aero_point_0.wing.def_mesh')

# Perform the connections with the modified names within the
# 'aero_states' group.
prob.model.connect('wing.mesh', 'aero_point_0.aero_states.wing_def_mesh')
# prob.model.connect('wing.t_over_c', 'aero_point_0.wing_perf.t_over_c')

## - - - - - - - - - - - (maybe write another script for optimization and visusalization)

prob.driver = om.ScipyOptimizeDriver()

recorder = om.SqliteRecorder("aero_wb.db")
prob.driver.add_recorder(recorder)
prob.driver.recording_options['record_derivatives'] = True
prob.driver.recording_options['includes'] = ['*']

# # Setup problem and add design variables, constraint, and objective
prob.model.add_design_var('wing.sweep', lower=prob['wing.sweep'], upper=prob['wing.sweep'])
prob.model.add_constraint('aero_point_0.wing_perf.CL')
prob.model.add_objective('aero_point_0.wing_perf.CD')