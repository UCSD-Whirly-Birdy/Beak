import unittest
import numpy as np
from openmdao.utils.assert_utils import assert_near_equal

class TestTravis(unittest.TestCase):
    
    def test_example(self):

        import openmdao.api as om

        from simple_optimization.components.cl_comp import CLComp

        # build the model
        prob = om.Problem()
        model = prob.model
        

        model.add_subsystem('p1', om.IndepVarComp('CLa', 2 * np.pi))
        model.add_subsystem('p2', om.IndepVarComp('alpha', 0.04))
        model.add_subsystem('p3', om.IndepVarComp('CL0', 0.2))
        model.add_subsystem('comp', CLComp())

        model.connect('p1.CLa', 'comp.CLa')
        model.connect('p2.alpha', 'comp.alpha')
        model.connect('p3.CL0', 'comp.CL0')

        prob.setup()
        prob.run_model()

        assert_near_equal(prob['comp.CL'], 0.45, 10**-2)

if __name__ == "__main__":

    unittest.main()