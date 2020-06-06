import numpy as np
import openmdao.api as om

from openmdao.api import Problem, Group, IndepVarComp

from whirly_bird_optimization.cruise_analysis_group import CruiseAnalysisGroup
from whirly_bird_optimization.hover_analysis_group import HoverAnalysisGroup
from whirly_bird_optimization.performance_group import PerformanceGroup
#from whirly_bird_optimization.equilibrium_group import EquilibriumGroup ---> not used here, it's part of performance

n = 1
shape = (n,n)

prob = Problem()

cruise_analysis_group = CruiseAnalysisGroup(
    shape = shape,
    #mode = 'cruise',
)
prob.model.add_subsystem('cruise_analysis_group', cruise_analysis_group)

hover_analysis_group = HoverAnalysisGroup(
    shape = shape,
    #mode = 'hover',
)
prob.model.add_subsystem('hover_analysis_group', hover_analysis_group)


performance_group = PerformanceGroup(
    shape = shape,
)
prob.model.add_subsystem('performance_analysis_group', performance_group)

prob.model.connect('cruise_analysis_group.cruise_propulsion_group.efficiency','performance_analysis_group.efficiency')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.L_D', 'performance_analysis_group.L_D')
# prob.model.connect('')


prob.setup(check=True)
prob.setup()

prob['cruise_analysis_group.inputs_comp.altitude'] = 500.
prob['hover_analysis_group.inputs_comp.altitude'] = 100.

prob['cruise_analysis_group.inputs_comp.speed'] = 50.
prob['hover_analysis_group.inputs_comp.speed'] = 1.

prob['cruise_analysis_group.cruise_propulsion_group.mass'] = 0.03
prob['cruise_analysis_group.cruise_propulsion_group.rotor_group.inputs_comp.radius_scalar'] = 0.127

prob['cruise_analysis_group.cruise_propulsion_group.normalized_torque'] = 1.
prob['cruise_analysis_group.cruise_propulsion_group.angular_speed'] = 1500.
prob['cruise_analysis_group.cruise_propulsion_group.stator_diameter'] = 0.022
prob['cruise_analysis_group.cruise_propulsion_group.shaft_diameter'] = 0.003
prob['cruise_analysis_group.cruise_propulsion_group.outer_diameter'] = 0.0279

# # # Setup problem and add design variables, constraint, and objective
# prob.model.add_design_var('twist_cp', lower=-20., upper=20.)
# prob.model.add_design_var('sweep', lower=0., upper=60.)
# prob.model.add_design_var('AR', lower=4., upper=16.)
# prob.model.add_design_var('wing_area', lower=0.05, upper=0.1)
# prob.model.add_design_var('alpha', lower=0., upper=10.)
# prob.model.add_design_var('power_coefficient', lower=0., upper=0.8)
# prob.model.add_design_var('propeller_diameter', lower=0.1, upper=1.2)
#prob.model.add_design_var('angular_speed', lower=0., upper=3000)
# prob.model.add_design_var('hover_RPM', lower=400., upper=600.)
# prob.model.add_design_var('ref_point', lower=0.,upper=prob['wing_span']/2*np.tan(prob['sweep']*np.pi/180) + prob['chord']) 
# # need to set upper limit of ref_point as c + b/2*tan(sweep*pi/180)

prob.run_model()

# prob.model.list_inputs(prom_name=True)
prob.model.list_inputs(prom_name=True)

# set up optimization problem

# prob.driver = om.ScipyOptimizeDriver()

# recorder = om.SqliteRecorder("aero_wb.db")
# prob.driver.add_recorder(recorder)
# prob.driver.recording_options['record_derivatives'] = True
# prob.driver.recording_options['includes'] = ['*']


# ## set RP as design variable
# # set RP whre  CM0 - CM1 = 0

# prob.model.add_constraint('L_W', equals=0.)
# prob.model.add_constraint('T_D', equals=0.)
# prob.model.add_constraint('NP_CG', lower= 0.)
# # add constraint about vertical hover minimum
# prob.model.add_constraint('Weight', equals=.75)
# prob.model.add_constraint('wing_span', upper=1.2)
# ## add constraints and design varaibles 
# prob.model.add_objective('range', scaler=1e4)


## EDIT THIS INTO RUN FILE


## - - - - - - - - - - - (maybe write another script for optimization and visualization)

# prob.driver = om.ScipyOptimizeDriver()

# recorder = om.SqliteRecorder("aero_wb.db")
# prob.driver.add_recorder(recorder)
# prob.driver.recording_options['record_derivatives'] = True
# prob.driver.recording_options['includes'] = ['*']

# # # Setup problem and add design variables, constraint, and objective
# prob.model.add_design_var('wing.twist_cp', lower=-20., upper=20.)
# prob.model.add_design_var('wing.sweep', lower=0., upper=50.)
# prob.model.add_design_var('wing.alpha', lower=0., upper=10.)
# prob.model.add_constraint('laura.wing_perf.CL', equals=0.5)
# ## add constraints and design varaibles 
# prob.model.add_objective('laura.wing_perf.CD', scaler=1e4)

# Set up the problem
#prob.setup()
# prob.run_model()
# prob.model.list_outputs(prom_name=True)
# prob.model.list_inputs(prom_name=True)

# print("\nWing CL:", prob['laura.wing_perf.CL'])
# print("Wing CD:", prob['laura.wing_perf.CD'])
# print("Wing Sweep:", prob['wing.sweep'])
# print("Wing Alpha:", prob['laura.alpha'])
# print("Wing Twist Cp:", prob['wing.twist_cp'])
# print("CoG:", prob['laura.cg'])

# plot_wing aero_wb.db to plot wing over iterations
# plot_wingbox aero_wb.db of CS of airfoil (but produces error, yet to fix)