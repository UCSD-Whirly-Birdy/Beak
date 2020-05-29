import numpy as np
import openmdao.api as om

from openmdao.api import Group

from openaerostruct.geometry.utils import generate_mesh
from openaerostruct.geometry.geometry_group import Geometry
from openaerostruct.aerodynamics.aero_groups import AeroPoint

from whirly_bird_optimization.aerodynamics_group import AerodynamicsGroup

class AerodynamicsMeshGroup(Group):

    def setup(self):

        mesh_dict = {'num_y' : 15,
                     'num_x' : 7,
                     'wing_type' : 'rect',
                     'symmetry' : True,
                     'span' : 1.0,
                     'chord' : 0.1,
                     }

        mesh = generate_mesh(mesh_dict)

        surface = { 'name' : 'wing', 
                    'symmetry' : True,
                    'S_ref_type' : 'wetted',
                    'twist_cp' : np.zeros(2),
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
        prob = om.Problem()
        prob.model.add_subsystem(surface['name'], geom_group)
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
        # Connect the mesh from the geometry component to the analysis point
        prob.model.connect('wing.mesh', 'aero_point_0.wing.def_mesh')
        prob.model.connect('wing.mesh', 'aero_point_0.aero_states.wing_def_mesh')
        prob.model.connect('wing.t_over_c', 'aero_point_0.wing_perf.t_over_c')
