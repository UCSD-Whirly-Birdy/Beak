# Used to plot

import numpy as np

from lsdo_viz.api import BaseViz, Frame

import seaborn as sns


sns.set()


mode = 'last'


class Viz(BaseViz):

    def setup(self):
        # self.use_latex_fonts()

        self.frame_name_format = 'output_{}'

        self.add_frame(Frame(
            height_in=8., width_in=12.,
            nrows=2, ncols=4,
            wspace=0.4, hspace=0.4,
        ), 1)

    def plot(self, data_dict_list, ind, video=False):
        if ind < 0:
            ind += len(data_dict_list)

        data_dict_list[ind]['cruise_analysis_group.cruise_aerodynamics_group.wing.sweep'] 
        data_dict_list[ind]['AR']
        data_dict_list[ind]['wing_area']
        data_dict_list[ind]['wing_span']
        data_dict_list[ind]['cruise_analysis_group.cruise_aerodynamics_group.wing_chord']
        data_dict_list[ind]['cruise_alpha']
        data_dict_list[ind]['hover_alpha']
        data_dict_list[ind]['performance_analysis_group.vertical_cruise']
        data_dict_list[ind]['performance_analysis_group.static_margin']

        self.get_frame(1).clear_all_axes()
        
        # ASPECT RATIO
        with self.get_frame(1)[0, 0] as ax:
            x = np.arange(ind)
            y = [
                data_dict_list[k]['AR'][0]
                for k in range(ind)
            ]
            ax.plot(x, y)
            if video:
                ax.set_xlim([0, len(data_dict_list)])
                ax.set_ylim(self.get_limits(
                    'AR', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
            ax.set_xlabel('Iteration')
            ax.set_ylabel('AR')

        # WING AREA
        with self.get_frame(1)[1, 0] as ax:
            x = np.arange(ind)
            y = [
                data_dict_list[k]['wing_area'][0]
                for k in range(ind)
            ]
            ax.plot(x, y)
            if video:
                ax.set_xlim([0, len(data_dict_list)])
                ax.set_ylim(self.get_limits(
                    'wing_area', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Wing Area (m^2)')

        # WING SPAN
        with self.get_frame(1)[0, 1] as ax:
            x = np.arange(ind)
            y = [
                data_dict_list[k]['wing_span'][0]
                for k in range(ind)
            ]
            ax.plot(x, y)
            if video:
                ax.set_xlim([0, len(data_dict_list)])
                ax.set_ylim(self.get_limits(
                    'wing_span', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Wing Span (m)')

        # CHORD LENGTH
        with self.get_frame(1)[1, 1] as ax:
            x = np.arange(ind)
            y = [
                data_dict_list[k]['cruise_analysis_group.cruise_aerodynamics_group.wing_chord'][0]
                for k in range(ind)
            ]
            ax.plot(x, y)
            if video:
                ax.set_xlim([0, len(data_dict_list)])
                ax.set_ylim(self.get_limits(
                    'cruise_analysis_group.cruise_aerodynamics_group.wing_chord', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Chord (m)')

        # SWEEP
        with self.get_frame(1)[1, 1] as ax:
            x = np.arange(ind)
            y = [
                data_dict_list[k]['cruise_analysis_group.cruise_aerodynamics_group.wing.sweep'][0]
                for k in range(ind)
            ]
            ax.plot(x, y)
            if video:
                ax.set_xlim([0, len(data_dict_list)])
                ax.set_ylim(self.get_limits(
                    'cruise_analysis_group.cruise_aerodynamics_group.wing.sweep', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Sweep (deg)')
            
        # CRUISE & HOVER ANGLE OF ATTACK
        with self.get_frame(1)[1, 1] as ax:
            x = np.arange(ind)
            y = [
                (data_dict_list[k]['cruise_alpha'][0], data_dict_list[k]['hover_alpha'][0])
                for k in range(ind)
            ]
            ax.plot(x, y)
            if video:
                ax.set_xlim([0, len(data_dict_list)])
                ax.set_ylim(self.get_limits(
                    'cruise_analysis_group.cruise_aerodynamics_group.wing_chord', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Chord (m)')

        # VERTICAL CRUISE CONSTRAINT
        with self.get_frame(1)[1, 1] as ax:
            x = np.arange(ind)
            y = [
                data_dict_list[k]['performance_analysis_group.vertical_cruise'][0]
                for k in range(ind)
            ]
            ax.plot(x, y)
            if video:
                ax.set_xlim([0, len(data_dict_list)])
                ax.set_ylim(self.get_limits(
                    'performance_analysis_group.vertical_cruise', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Cruise Vertical Net Force (N)')
        
        # STATIC MARGIN
        with self.get_frame(1)[1, 1] as ax:
            x = np.arange(ind)
            y = [
                data_dict_list[k]['performance_analysis_group.static_margin'][0]
                for k in range(ind)
            ]
            ax.plot(x, y)
            if video:
                ax.set_xlim([0, len(data_dict_list)])
                ax.set_ylim(self.get_limits(
                    'performance_analysis_group.static_margin', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Static Margin')
        

        with self.get_frame(1)[1, 1] as ax:
            x = [
                data_dict_list[ind]['CD'][0]
            ]
            y = [
                data_dict_list[ind]['CL'][0]
            ]
            ax.plot(x, y, 'o')
            if video:
                ax.set_xlim(self.get_limits(
                    'CD', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
                ax.set_ylim(self.get_limits(
                    'CL', lower_margin=0.1, upper_margin=0.1, mode=mode,
                ))
            ax.set_xlabel('CD')
            ax.set_ylabel('CL')

        self.get_frame(1).write()