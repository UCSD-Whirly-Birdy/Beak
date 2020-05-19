import unittest

from whirly_bird_optimization.cruise_propulsion.power_coeff_comp import PowerCoeffComp
from openmdao.api import Problem
from openmdao.utils.assert_utils import assert_check_partials


class TestPowerCoeffComp(unittest.TestCase):

    def test_component_and_derivatives(self):
        prob = Problem()
        prob.model = PowerCoeffComp()
        prob.setup()
        prob.run_model()

        data = prob.check_partials(out_stream=None)
        assert_check_partials(data, atol=1.e-3, rtol=1.e-3)


if __name__ == '__main__':
    unittest.main()