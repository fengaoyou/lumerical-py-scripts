#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# @author: Georgios Gcharalampous (gcharalampous)
# version ='1.0'
# ---------------------------------------------------------------------------
"""
User-inputs are required.

In this file, the user must enter the sweep parameters. 

The waveguide parameters to sweep are 'wg_thickness' and 'wg_width' .



               ^                                                                         
               |                                                                         
               |                                                                         
               |                    -                                                    
            wg_width                                                                     
        <--------------->                                                                
       +-------|--------+ ^                                                              
       |       |        | |                                                              
       |   waveguide    | | wg_thickness                                                 
       |       |        | |                                                              
   ------------|----------v--------------------->                                        
          (0,0)|                                                                         
               |                                                                         
               |                                                                         
               |                                                                         

"""





wg_width_start = 2.0e-6     # Choose the start waveguide width 'wg_width_start' you want to start sweeping
wg_width_stop = 5.25e-6      # Choose the stop waveguide width 'wg_width_stop' you want to finish sweeping
wg_width_step = 0.25e-6      # Choose the step of each sweep 'wg_step'


wg_taper_start = 10.0e-6     # Choose the start waveguide length 'wg_taper_start' you want to start sweeping
wg_taper_stop = 110.0e-6      # Choose the stop waveguide length 'wg_taper_stop' you want to finish sweeping
wg_taper_step = 10.0e-6      # Choose the step of each sweep 'wg_taper_step'



