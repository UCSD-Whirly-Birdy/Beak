import numpy as np
import openmdao.api as om

from openmdao.api import Problem, Group, IndepVarComp

from whirly_bird_optimization.cruise_analysis_group import CruiseAnalysisGroup
from whirly_bird_optimization.hover_analysis_group import HoverAnalysisGroup
from whirly_bird_optimization.performance_group import PerformanceGroup

n = 1
shape = (n,n)

prob = Problem()

# global_ivc = IndepVarComp()
# global_ivc.add_output('AR')
# global_ivc.add_output('wing_area')
# global_ivc.add_output('sweep')
# global_ivc.add_output('alpha')
# global_ivc.add_output('cruise_propeller_angular_speed')
# global_ivc.add_output('power_coefficient')
# global_ivc.add_output('hover_wing_angular_speed')
# global_ivc.add_output('twist')
# global_ivc.add_output('hover_propellor_angular_speed')
# prob.model.add_subsystem('global_inputs_comp', global_ivc, promotes=['*'])

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

# general connections

prob.model.connect('cruise_analysis_group.cruise_propulsion_group.efficiency','performance_analysis_group.efficiency')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.L_D', 'performance_analysis_group.L_D')
prob.model.connect('cruise_analysis_group.cruise_propulsion_group.thrust', 'performance_analysis_group.thrust_cruise')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.aero_point.wing_perf.D', 'performance_analysis_group.drag_cruise')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.aero_point.wing_perf.L', 'performance_analysis_group.lift_cruise')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.wing_chord', ['performance_analysis_group.chord', 'performance_analysis_group.mac'])
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.wing_span', ['performance_analysis_group.wing_span', 'cruise_analysis_group.cruise_propulsion_group.wing_span', 'hover_analysis_group.hover_velocity_group.wing_span', 'hover_analysis_group.hover_propulsion_group.wing_span'])
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.aero_point.CL', 'cruise_analysis_group.cruise_aerodynamics_group.C_L')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.aero_point.CL', 'hover_analysis_group.hover_aerodynamics_group.C_L')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.aero_point.CD', 'cruise_analysis_group.cruise_aerodynamics_group.C_D')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.aero_point.CD', 'hover_analysis_group.hover_aerodynamics_group.C_D')
prob.model.connect('cruise_analysis_group.inputs_comp.speed', 'cruise_analysis_group.cruise_aerodynamics_group.aero_point.v')
prob.model.connect('hover_analysis_group.inputs_comp.speed', ['hover_analysis_group.hover_aerodynamics_group.aero_point.v', 'hover_analysis_group.hover_propulsion_group.rotational_rotor_group.speed'])
prob.model.connect('cruise_analysis_group.atmosphere_group.density', 'cruise_analysis_group.cruise_aerodynamics_group.aero_point.rho')
prob.model.connect('hover_analysis_group.atmosphere_group.density', ['hover_analysis_group.hover_aerodynamics_group.aero_point.rho', 'hover_analysis_group.hover_propulsion_group.rotational_rotor_group.density'])
prob.model.connect('cruise_analysis_group.atmosphere_group.mach_number', 'cruise_analysis_group.cruise_aerodynamics_group.aero_point.Mach_number')
prob.model.connect('hover_analysis_group.atmosphere_group.mach_number', 'hover_analysis_group.hover_aerodynamics_group.aero_point.Mach_number')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.area', ['cruise_analysis_group.cruise_propulsion_group.wing_area', 'hover_analysis_group.hover_propulsion_group.wing_area'])
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.beta', 'cruise_analysis_group.cruise_aerodynamics_group.aero_point.beta')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.beta', 'hover_analysis_group.hover_aerodynamics_group.aero_point.beta')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.wing.sweep', ['performance_analysis_group.sweep', 'hover_analysis_group.hover_velocity_group.sweep'])
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.xshear', 'cruise_analysis_group.cruise_aerodynamics_group.wing.mesh.shear_x.xshear')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.yshear', 'cruise_analysis_group.cruise_aerodynamics_group.wing.mesh.shear_y.yshear')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.zshear', 'cruise_analysis_group.cruise_aerodynamics_group.wing.mesh.shear_z.zshear')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.xshear', 'hover_analysis_group.hover_aerodynamics_group.wing.mesh.shear_x.xshear')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.yshear', 'hover_analysis_group.hover_aerodynamics_group.wing.mesh.shear_y.yshear')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.zshear', 'hover_analysis_group.hover_aerodynamics_group.wing.mesh.shear_z.zshear')
prob.model.connect('hover_analysis_group.atmosphere_group.sonic_speed', 'hover_analysis_group.hover_propulsion_group.rotational_rotor_group.sonic_speed')


# design variables connections (connections from global variables to design variables throughout model)

# prob.model.connect('AR', ['cruise_analysis_group.cruise_aerodynamics_group.AR', 'hover_analysis_group.hover_aerodynamics_group.AR'])
# prob.model.connect('wing_area', ['cruise_analysis_group.cruise_aerodynamics_group.area', 'hover_analysis_group.hover_aerodynamics_group.area'])
# prob.model.connect('sweep', ['cruise_analysis_group.cruise_aerodynamics_group.wing.sweep', 'hover_analysis_group.hover_aerodynamics_group.wing.sweep'])
# prob.model.connect('alpha', ['cruise_analysis_group.cruise_aerodynamics_group.aero_point.alpha', 'hover_analysis_group.hover_aerodynamics_group.aero_point.alpha'])
# prob.model.connect('cruise_propeller_angular_speed', 'cruise_analysis_group.cruise_propulsion_group.angular_speed')
# prob.model.connect('power_coefficient', 'cruise_analysis_group.cruise_propulsion_group.power_coeff')
# prob.model.connect('hover_wing_angular_speed', 'hover_analysis_group.hover_velocity_group.hover_wing_angular_speed')
# prob.model.connect('twist', ['cruise_analysis_group.cruise_aerodynamics_group.wing.twist_cp', 'hover_analysis_group.hover_aerodynamics_group.wing.twist_cp'])
# prob.model.connect('hover_propellor_angular_speed', 'hover_analysis_group.hover_propulsion_group.angular_speed')

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
# prob.model.add_design_var('angular_speed', lower=0., upper=3000)
# prob.model.add_design_var('hover_RPM', lower=400., upper=600.)
# prob.model.add_design_var('ref_point', lower=0.,upper=prob['wing_span']/2*np.tan(prob['sweep']*np.pi/180) + prob['chord']) 
# # need to set upper limit of ref_point as c + b/2*tan(sweep*pi/180)

prob.run_model()

#prob.model.list_inputs(prom_name=True)
prob.model.list_outputs(prom_name=True)

# set up optimization problem

# prob.driver = om.ScipyOptimizeDriver()
# prob.driver.options['optimizer'] = 'SLSQP' # options include: [‘Powell’, ‘CG’, ‘L-BFGS-B’, ‘COBYLA’, ‘shgo’, ‘Nelder-Mead’, ‘basinhopping’, ‘SLSQP’, ‘dual_annealing’, ‘trust-constr’, ‘Newton-CG’, ‘TNC’, ‘BFGS’, ‘differential_evolution’]
# prob.driver.options['tol'] = 1e-9 # or maybe 1e-6
# prob.driver.options['disp'] = True

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
# prob.model.add_objective('range', scaler=-1e4)

# plot_wing aero_wb.db to plot wing over iterations
# plot_wingbox aero_wb.db of CS of airfoil (but produces error, yet to fix)