import numpy as np

from openmdao.api import Problem, Group, IndepVarComp

from whirly_bird_optimization.analysis_group import AnalysisGroup
from whirly_bird_optimization.performance_group import PerformanceGroup

n = 1
shape = (n,n)

prob = Problem()

analysis_group = AnalysisGroup(
    shape = shape,
    # mode = 'cruise',
)
prob.model.add_subsystem('cruise_analysis_group', analysis_group)

analysis_group = AnalysisGroup(
    shape = shape,
    # mode = 'hover',
)
prob.model.add_subsystem('hover_analysis_group', analysis_group)

performance_group = PerformanceGroup(
    shape = shape,
)
prob.model.add_subsystem('performance_analysis_group', performance_group)
prob.model.connect('performance_analysis_group.eta', 'cruise_analysis_group.propulsion_group.efficiency')


prob.setup(check=True)

# set indep variables

prob.run_model()
prob.model.list_inputs(prom_name=True)

# set up optimization problem
range = all the shit

