import numpy as np
import openmdao.api as om

from openmdao.api import Group

from openaerostruct.geometry.utils import generate_mesh, scale_x
from openaerostruct.geometry.geometry_group import Geometry
from openaerostruct.aerodynamics.aero_groups import AeroPoint
from openaerostruct.integration.multipoint_comps import MultiCD

from aerodynamics_geom_group import AerodynamicsGeomGroup
from hover_aero_geom import HoverAeroVelocity

prob = om.Problem()

# class CruiseAeroGroup(Group):
#     def initialize(self):
#         self.options.declare('shape', types=tuple)

#     def setup(self):
#         shape = self.options['shape']
        
indep_var_comp = om.IndepVarComp()
indep_var_comp.add_output('v', val=50, units='m/s')
# indep_var_comp.add_output('v_hover', val=50, units='m/s')
indep_var_comp.add_output('Mach_number', val=0.3)
indep_var_comp.add_output('re', val=1.e6, units='1/m')
indep_var_comp.add_output('rho', val=1.225, units='kg/m**3')
indep_var_comp.add_output('cg', val=np.zeros((3)), units='m')
# indep_var_comp.add_output('cg', val=np.array([RP, 0., 0.]), units='m') # import group with design variable 'ref_point'
indep_var_comp.add_output('alpha0', val = 2.)
indep_var_comp.add_output('alpha1', val = 2. + .001)

# prob.model.add_subsystem('ivc', indep_var_comp, promotes=['*'])
prob.model.add_subsystem('ivc', indep_var_comp) # don't want to promote since we have two alphas and velocities

shape = (1,)
prob.model.add_subsystem('AerodynamicsGeomGroup', AerodynamicsGeomGroup(shape=shape), promotes = ['*'])
# prob.model.add_subsystem('AerodynamicsGeomGroup1', AerodynamicsGeomGroup(shape=shape))
# prob.model.add_subsystem('AerodynamicsGeomGroup2', AerodynamicsGeomGroup(shape=shape))

# prob.model.connect('ivc.alpha1','AerodynamicsGeomGroup1.alpha')
# prob.model.connect('alpha2','AerodynamicsGeomGroup2')

mesh_dict = {'num_y' : 17,
            'num_x' : 9,
            'wing_type' : 'rect',
            'symmetry' : True,
            'chord': 0.1,
            'span' : 1.,
            }

mesh = generate_mesh(mesh_dict)

surface = { 'name' : 'wing', 
            'symmetry' : True,
            'S_ref_type' : 'wetted',
            'twist_cp' : np.zeros(3),
            'mesh' : mesh,
            'CL0' : 0.0,
            'CD0' : 0.001,
            'k_lam' : 0.05,
            't_over_c_cp' : np.array([0.1875]),
            'c_max_t' : 0.1,
            'with_viscous' : True,
            'with_wave' : False,
            'sweep' : 0.,
            'alpha' : 0.,
            }

geom_group = Geometry(surface=surface)

prob.model.add_subsystem(surface['name'], geom_group)
name = surface['name']
# aero_group = AeroPoint(surfaces=[surface])
# point_name = 'laura'
# prob.model.add_subsystem(point_name, aero_group)

aero_group = AeroPoint(surfaces=[surface])
point_name0 = 'laura0' # cruise & regular alpha
prob.model.add_subsystem(point_name0, aero_group)

aero_group = AeroPoint(surfaces=[surface])
point_name1 = 'laura1' # cruise & regular alpha + d_alpha
prob.model.add_subsystem(point_name1, aero_group)

# aero_group = AeroPoint(surfaces=[surface])
# # point_name3 = 'laura3' # hover-drag & regular alpha
# # prob.model.add_subsystem(point_name3, aero_group)


# Connect flow properties to the analysis point
prob.model.connect('ivc.v', point_name0 + '.v')
prob.model.connect('ivc.Mach_number', point_name0 + '.Mach_number')
prob.model.connect('ivc.re', point_name0 + '.re')
prob.model.connect('ivc.rho', point_name0 + '.rho')
prob.model.connect('ivc.cg', point_name0 + '.cg')
prob.model.connect('ivc.alpha0', point_name0 + '.alpha')

prob.model.connect('ivc.v', point_name1 + '.v')
prob.model.connect('ivc.Mach_number', point_name1 + '.Mach_number')
prob.model.connect('ivc.re', point_name1 + '.re')
prob.model.connect('ivc.rho', point_name1 + '.rho')
prob.model.connect('ivc.cg', point_name1 + '.cg')
prob.model.connect('ivc.alpha1', point_name1 + '.alpha')

prob.model.connect(point_name0 + '.CD', 'multi_CD.0_CD')
prob.model.connect(point_name1 + '.CD', 'multi_CD.1_CD')

# Connect the mesh from the geometry component to the analysis point
prob.model.connect(name + '.mesh', point_name0 + '.wing.def_mesh')
prob.model.connect(name + '.mesh', point_name1 + '.wing.def_mesh')

# Perform the connections with the modified names within the 'aero_states' group.
prob.model.connect(name + '.mesh', point_name0 + '.aero_states.wing_def_mesh')
prob.model.connect(name + '.t_over_c', point_name0 + '.wing_perf.t_over_c')

prob.model.connect(name + '.mesh', point_name1 + '.aero_states.wing_def_mesh')
prob.model.connect(name + '.t_over_c', point_name1 + '.wing_perf.t_over_c')

prob.model.connect('wing_span', 'wing.mesh.stretch.span')
prob.model.connect('oas_wing_chord', 'wing.mesh.scale_x.chord')

prob.model.add_subsystem('multi_CD', MultiCD(n_points = 2), promotes_outputs=['CD'])

## - - - - - - - - - - - (maybe write another script for optimization and visusalization)

prob.driver = om.ScipyOptimizeDriver()

# recorder = om.SqliteRecorder("aero_wb.db")
# prob.driver.add_recorder(recorder)
# prob.driver.recording_options['record_derivatives'] = True
# prob.driver.recording_options['includes'] = ['*']

# # Setup problem and add design variables, constraint, and objective
prob.model.add_design_var('wing.twist_cp', lower=-20., upper=20.)
prob.model.add_design_var('wing.sweep', lower=0., upper=50.)
# prob.model.add_design_var('alpha', lower=0., upper=10.)
# prob.model.add_constraint(point_name0 + '.wing_perf.CL', equals=0.5)
# prob.model.add_constraint(point_name1 + '.wing_perf.CL', equals=0.5)

prob.model.add_objective('CD', scaler=1e4)


# # Set up the problem
prob.setup()

prob.run_model()
prob.model.list_inputs(prom_name=True)

print(prob[point_name0 + '.CM'])
print(prob[point_name1 + '.CM'])

# # # plot_wing aero_wb.db to plot wing over iterations
# # # plot_wingbox aero_wb.db of CS of airfoil (but produces error, yet to fix)