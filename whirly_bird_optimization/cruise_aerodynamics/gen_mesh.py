import numpy as np

from openmdao.api import Group

from openaerostruct.geometry.utils import generate_mesh
from openaerostruct.geometry.geometry_group import Geometry
from openaerostruct.aerodynamics.aero_groups import AeroPoint

class GenMesh(Group):

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


