import numpy as np
import openmdao.api as om

from openmdao.api import Problem, Group, IndepVarComp

from whirly_bird_optimization.cruise_analysis_group import CruiseAnalysisGroup
from whirly_bird_optimization.hover_analysis_group import HoverAnalysisGroup
from whirly_bird_optimization.performance_group import PerformanceGroup

n = 1
shape = (n,n)

prob = Problem()
# # SETTING UP GLOBAL INDEPENDENT VARIABLE COMPONENTS 
# NOTE: Sweep, twist are design variables in the indepvarcomp within the aerodynamics 
global_ivc = IndepVarComp()
global_ivc.add_output('re', val=1.e5, units='1/m')
global_ivc.add_output('cg', val=np.zeros((3)), units='m')
global_ivc.add_output('beta', val = 0.)
global_ivc.add_output('xshear', val = np.zeros((9)))
global_ivc.add_output('yshear', val = np.zeros((9)))
global_ivc.add_output('zshear', val = np.zeros((9)))
global_ivc.add_output('AR', val = 12)
global_ivc.add_output('wing_area', val = 0.05)
global_ivc.add_output('current', val = 15.)
# global_ivc.add_output('power_coefficient')
# CRUISE VARIABLES:
global_ivc.add_output('v_cruise', val=50, units='m/s')
global_ivc.add_output('rho_cruise')
global_ivc.add_output('cruise_alpha', val = 2.)
global_ivc.add_output('cruise_propeller_angular_speed', val = 1500)
# HOVER VARIABLES:
global_ivc.add_output('v_hover', val=50, units='m/s')
global_ivc.add_output('rho_hover')
global_ivc.add_output('hover_alpha', val = 2.)
global_ivc.add_output('hover_wing_angular_speed', val = 50.)
global_ivc.add_output('hover_propeller_angular_speed', val = 1500)
prob.model.add_subsystem('global_inputs_comp', global_ivc, promotes=['*'])

# # IMPORTING CRUISE/HOVER/PERFORMANCE GROUPS
cruise_analysis_group = CruiseAnalysisGroup(
    shape = shape,
    # mode = 'cruise',
)
prob.model.add_subsystem('cruise_analysis_group', cruise_analysis_group)

hover_analysis_group = HoverAnalysisGroup(
    shape = shape,
    # mode = 'hover',
)
prob.model.add_subsystem('hover_analysis_group', hover_analysis_group)

performance_group = PerformanceGroup(
    shape = shape,
)
prob.model.add_subsystem('performance_analysis_group', performance_group)

## CONNECTIONS

prob.model.connect('cruise_analysis_group.cruise_propulsion_group.efficiency','performance_analysis_group.efficiency')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.L_D', 'performance_analysis_group.L_D')
prob.model.connect('cruise_analysis_group.cruise_propulsion_group.thrust', 'performance_analysis_group.thrust_cruise')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.aero_point.wing_perf.D', 'performance_analysis_group.drag_cruise')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.aero_point.wing_perf.L', 'performance_analysis_group.lift_cruise')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.wing_chord', ['performance_analysis_group.chord', 'performance_analysis_group.mean_aerodynamic_chord'])
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.wing_span', ['performance_analysis_group.wing_span', 'hover_analysis_group.hover_velocity_group.wing_span', 'hover_analysis_group.hover_propulsion_group.wing_span'])
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.aero_point.CL', 'cruise_analysis_group.cruise_aerodynamics_group.C_L')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.aero_point.CL', 'hover_analysis_group.hover_aerodynamics_group.C_L')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.aero_point.CD', 'cruise_analysis_group.cruise_aerodynamics_group.C_D')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.aero_point.CD', 'hover_analysis_group.hover_aerodynamics_group.C_D')
prob.model.connect('cruise_analysis_group.inputs_comp.speed', 'cruise_analysis_group.cruise_aerodynamics_group.aero_point.v')
prob.model.connect('hover_analysis_group.inputs_comp.speed', ['hover_analysis_group.hover_aerodynamics_group.aero_point.v', 'hover_analysis_group.hover_propulsion_group.rotational_rotor_group.speed', 'hover_analysis_group.hover_propulsion_group.vertical_rotor_group.speed'])
prob.model.connect('cruise_analysis_group.atmosphere_group.density', 'cruise_analysis_group.cruise_aerodynamics_group.aero_point.rho')
prob.model.connect('hover_analysis_group.atmosphere_group.density', ['hover_analysis_group.hover_aerodynamics_group.aero_point.rho', 'hover_analysis_group.hover_propulsion_group.rotational_rotor_group.density', 'hover_analysis_group.hover_propulsion_group.vertical_rotor_group.density'])
prob.model.connect('cruise_analysis_group.atmosphere_group.mach_number', 'cruise_analysis_group.cruise_aerodynamics_group.aero_point.Mach_number')
prob.model.connect('hover_analysis_group.atmosphere_group.mach_number', 'hover_analysis_group.hover_aerodynamics_group.aero_point.Mach_number')
# prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.area', ['hover_analysis_group.hover_propulsion_group.wing_area'])
prob.model.connect('beta', 'cruise_analysis_group.cruise_aerodynamics_group.aero_point.beta')
prob.model.connect('beta', 'hover_analysis_group.hover_aerodynamics_group.aero_point.beta')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.wing.sweep', ['performance_analysis_group.sweep', 'hover_analysis_group.hover_velocity_group.sweep'])
prob.model.connect('xshear', 'cruise_analysis_group.cruise_aerodynamics_group.wing.mesh.shear_x.xshear')
prob.model.connect('yshear', 'cruise_analysis_group.cruise_aerodynamics_group.wing.mesh.shear_y.yshear')
prob.model.connect('zshear', 'cruise_analysis_group.cruise_aerodynamics_group.wing.mesh.shear_z.zshear')
prob.model.connect('xshear', 'hover_analysis_group.hover_aerodynamics_group.wing.mesh.shear_x.xshear')
prob.model.connect('yshear', 'hover_analysis_group.hover_aerodynamics_group.wing.mesh.shear_y.yshear')
prob.model.connect('zshear', 'hover_analysis_group.hover_aerodynamics_group.wing.mesh.shear_z.zshear')
prob.model.connect('hover_analysis_group.atmosphere_group.sonic_speed', ['hover_analysis_group.hover_propulsion_group.rotational_rotor_group.sonic_speed', 'hover_analysis_group.hover_propulsion_group.vertical_rotor_group.sonic_speed'])

# prob.model.connect('hover_analysis_group.hover_velocity_group.hover_wing_angular_speed', 'hover_analysis_group_hover_propulsion_group.rotational_motor_group.angular_speed')
prob.model.connect('hover_analysis_group.hover_propulsion_group.vertical_torque', 'performance_analysis_group.vertical_torque')
prob.model.connect('hover_analysis_group.hover_propulsion_group.vertical_rotor_group.thrust','performance_analysis_group.lift_hover')
prob.model.connect('cruise_propeller_angular_speed', 'cruise_analysis_group.cruise_propulsion_group.angular_speed')

prob.model.connect('hover_analysis_group.hover_velocity_group.radius', 'hover_analysis_group.hover_propulsion_group.vertical_rotor_group.radius_scalar')

# prob.model.connect('hover_analysis_group.hover_velocity_group.hover_wing_angular_speed', 'hover_analysis_group_hover_propulsion_group.rotational_motor_group.angular_speed')

# prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.wing.twist_cp', 'hover_analysis_group.hover_aerodynamics_group.wing.twist_cp')

# new connections to be integrated into others
prob.model.connect('hover_analysis_group.hover_propulsion_group.vertical_shaft_power','hover_analysis_group.hover_propulsion_group.vertical_rotor_group.shaft_power')
# prob.model.connect('hover_analysis_group.hover_velocity_group.hover_wing_angular_speed','hover_analysis_group.hover_propulsion_group.hover_wing_angular_speed')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.aero_point.wing_perf.D','hover_analysis_group.hover_propulsion_group.drag')
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.wing.sweep','hover_analysis_group.hover_propulsion_group.sweep')
prob.model.connect('hover_analysis_group.hover_propulsion_group.rotational_rotor_group.thrust','hover_analysis_group.hover_propulsion_group.thrust')

prob.model.connect('hover_analysis_group.hover_propulsion_group.propeller_shaft_power_comp.propeller_shaft_power','hover_analysis_group.hover_propulsion_group.rotational_rotor_group.shaft_power')

# prob.model.connect('cruise_analysis_group.cruise_propulsion_group.propeller_shaft_power.propeller_shaft_power_comp.propeller_shaft_power','cruise_analysis_group.cruise_propulsion_group.rotor_group.shaft_power')
# # prob.model.connect('cruise_analysis_group.cruise_propulsion_group.propeller_shaft_power','cruise_analysis_group.cruise_propulsion_group.rotor_group.shaft_power')
prob.model.connect('cruise_analysis_group.cruise_propulsion_group.propeller_shaft_power_comp.propeller_shaft_power','cruise_analysis_group.cruise_propulsion_group.shaft_power')
prob.model.connect('hover_propeller_angular_speed', 'hover_analysis_group.hover_propulsion_group.rotational_rotor_group.angular_speed')

prob.model.connect('AR', ['cruise_analysis_group.cruise_aerodynamics_group.AR', 'hover_analysis_group.hover_aerodynamics_group.AR'])
prob.model.connect('wing_area', ['cruise_analysis_group.cruise_aerodynamics_group.area', 'hover_analysis_group.hover_aerodynamics_group.area'])
# prob.model.connect('sweep', ['cruise_analysis_group.cruise_aerodynamics_group.wing.sweep', 'hover_analysis_group.hover_aerodynamics_group.wing.sweep'])
# prob.model.connect('cruise_propeller_angular_speed', 'cruise_analysis_group.cruise_propulsion_group.angular_speed')
# prob.model.connect('power_coefficient', 'cruise_analysis_group.cruise_propulsion_group.power_coeff')

prob.model.connect('hover_wing_angular_speed', ['hover_analysis_group.hover_velocity_group.hover_wing_angular_speed', 'hover_analysis_group.hover_propulsion_group.vertical_rotor_group.angular_speed','hover_analysis_group.hover_propulsion_group.hover_wing_angular_speed'])

# prob.model.connect('twist', ['cruise_analysis_group.cruise_aerodynamics_group.wing.twist_cp', 'hover_analysis_group.hover_aerodynamics_group.wing.twist_cp'])

# prob.model.connect('hover_propeller_angular_speed', 'hover_analysis_group.hover_propulsion_group.rotational_rotor_group.angular_speed')
# prob.model.connect('hover_propeller_angular_speed', 'hover_analysis_group.hover_propulsion_group.angular_speed')

# prob.model.connect('sweep', ['cruise_analysis_group.cruise_aerodynamics_group.wing.sweep', 'hover_analysis_group.hover_aerodynamics_group.wing.sweep', 'hover_analysis_group.hover_propulsion_group.sweep', 'performance_analysis_group.sweep'])

# MOTOR CURRENT/VOLTAGE/EFFICIENCY CONNECTIONS
prob.model.connect('current', 'cruise_analysis_group.cruise_propulsion_group.propeller_shaft_power_comp.current')
prob.model.connect('cruise_analysis_group.cruise_propulsion_group.voltage', 'cruise_analysis_group.cruise_propulsion_group.propeller_shaft_power_comp.voltage')
prob.model.connect('cruise_analysis_group.cruise_propulsion_group.motor_efficiency', 'cruise_analysis_group.cruise_propulsion_group.propeller_shaft_power_comp.motor_efficiency')
prob.model.connect('current', 'hover_analysis_group.hover_propulsion_group.propeller_shaft_power_comp.current')
prob.model.connect('hover_analysis_group.hover_propulsion_group.voltage', 'hover_analysis_group.hover_propulsion_group.propeller_shaft_power_comp.voltage')
prob.model.connect('hover_analysis_group.hover_propulsion_group.motor_efficiency', 'hover_analysis_group.hover_propulsion_group.propeller_shaft_power_comp.motor_efficiency')

# AEROPOINT CONNECTIONS IN OAS
prob.model.connect('cruise_alpha','cruise_analysis_group.cruise_aerodynamics_group.aero_point.alpha')
prob.model.connect('re','cruise_analysis_group.cruise_aerodynamics_group.aero_point.re')
prob.model.connect('cg','cruise_analysis_group.cruise_aerodynamics_group.aero_point.cg')
prob.model.connect('hover_alpha','hover_analysis_group.hover_aerodynamics_group.aero_point.alpha')
prob.model.connect('re','hover_analysis_group.hover_aerodynamics_group.aero_point.re')
prob.model.connect('cg','hover_analysis_group.hover_aerodynamics_group.aero_point.cg')

# CONNECTIONS INTO PERFORMANCE GROUP
prob.model.connect('cruise_analysis_group.cruise_aerodynamics_group.wing.twist_cp','performance_analysis_group.cruise_twist')
prob.model.connect('hover_analysis_group.hover_aerodynamics_group.wing.twist_cp','performance_analysis_group.hover_twist')
# prob.model.connect('','')
# prob.model.connect('','')
# prob.model.connect('','')
# prob.model.connect('','')
# prob.model.connect('','')

# # Setup problem and add design variables, constraint, and objective
prob.model.add_design_var('cruise_analysis_group.cruise_aerodynamics_group.wing.twist_cp', lower=-20., upper=20.) # done
prob.model.add_design_var('hover_analysis_group.hover_aerodynamics_group.wing.twist_cp', lower=-20., upper=20.) # done
# prob.model.add_design_var('sweep', lower=0., upper=60.) # done / need to fix connection to dv
prob.model.add_design_var('AR', lower=4., upper=16.) # done
prob.model.add_design_var('current', lower=0., upper=25.) # done
prob.model.add_design_var('wing_area', lower=0.05, upper=0.1) # done
prob.model.add_design_var('cruise_alpha', lower=0., upper=10.) # done
prob.model.add_design_var('hover_alpha', lower=0., upper=10.) # done
# prob.model.add_design_var('cruise_analysis_group.cruise_propulsion_group.power_coeff', lower=0., upper=1.) # done / revisit dv
prob.model.add_design_var('cruise_propeller_angular_speed', lower=0., upper=3000.) # done
prob.model.add_design_var('hover_propeller_angular_speed', lower=0., upper=3000.) # done
prob.model.add_design_var('hover_wing_angular_speed', lower = 800*np.pi/60, upper = 1200 * np.pi/60)

prob.model.add_constraint('performance_analysis_group.vertical_cruise', lower=0.)
prob.model.add_constraint('performance_analysis_group.horizontal_cruise', lower=0.)
prob.model.add_constraint('performance_analysis_group.static_margin', lower=0., upper=1.)
prob.model.add_constraint('performance_analysis_group.rotational_hover', lower=0.)
prob.model.add_constraint('performance_analysis_group.vertical_hover', lower=0.)
prob.model.add_constraint('performance_analysis_group.weight', equals=.7 * 9.81)
# prob.model.add_constraint('performance_analysis_group.weight', lower=.7 * 9.81, upper=.7 * 9.81)
prob.model.add_constraint('cruise_analysis_group.cruise_aerodynamics_group.wing_span', lower = 0., upper=1.2)
# prob.model.add_constraint('performance_analysis_group.twist_equality', lower=np.zeros(9), upper = np.absol)
# prob.model.add_constraint('performance_analysis_group.twist_equality', lower = np.zeros(3), upper = np.array([1e-6, 1e-6, 1e-6]))
# prob.model.add_constraint('performance_analysis_group.twist_equality', lower = np.zeros(3), upper = np.array([5, 5, 5]))

prob.model.add_objective('performance_analysis_group.range', scaler=-1e0)

prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP' # ‘COBYLA’, ‘SLSQP’
prob.driver.options['tol'] = 1e-9 # or 1e-6
prob.driver.options['disp'] = True

# recorder = om.SqliteRecorder("aero_wb.db")
# prob.driver.add_recorder(recorder)
# prob.driver.recording_options['record_derivatives'] = True
# prob.driver.recording_options['includes'] = ['*']

prob.setup()

prob['cruise_analysis_group.inputs_comp.altitude'] = 500.
prob['hover_analysis_group.inputs_comp.altitude'] = 100.

prob['cruise_analysis_group.inputs_comp.speed'] = 50.
prob['hover_analysis_group.inputs_comp.speed'] = 1.

prob['cruise_analysis_group.cruise_propulsion_group.rotor_group.inputs_comp.radius_scalar'] = 0.0635
prob['hover_analysis_group.hover_propulsion_group.rotational_rotor_group.radius_scalar'] = 0.0635

# VOLTAGE/MOTOR EFFICIENCY VALUES
prob['cruise_analysis_group.cruise_propulsion_group.voltage'] = 16.
prob['cruise_analysis_group.cruise_propulsion_group.motor_efficiency'] = .875
prob['hover_analysis_group.hover_propulsion_group.voltage'] = 16.
prob['hover_analysis_group.hover_propulsion_group.motor_efficiency'] = .875

# prob.run_model()
prob.run_driver()

# prob.model.list_outputs(prom_name=True)
# prob.model.list_inputs(prom_name=True)

print('Range:', prob['performance_analysis_group.range'])
print('Sweep Angle:', prob['cruise_analysis_group.cruise_aerodynamics_group.wing.sweep'])
print('Aspect Ratio:', prob['AR'])
print('Wing Area:', prob['wing_area'])
print('Current:', prob['current'])
print('Cruise Propeller Angular Speed:', prob['cruise_propeller_angular_speed'])
print('Hover Propeller Angular Speed:', prob['hover_propeller_angular_speed'])
print('Hover Wing Angular Speed:', prob['hover_wing_angular_speed'])
print('Cruise Alpha:', prob['cruise_alpha'])
print('Hover Alpha:', prob['hover_alpha'])

# plot_wing aero_wb.db to plot wing over iterations
# plot_wingbox aero_wb.db of CS of airfoil (but produces error, yet to fix)

# print(prob['cruise_analysis_group.cruise_aerodynamics_group.wing.twist'])
# print(prob['cruise_analysis_group.cruise_aerodynamics_group.wing.twist_cp'])
