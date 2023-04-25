#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# @author: Georgios Gcharalampous (gcharalampous)
# version ='1.0'
# ---------------------------------------------------------------------------
"""
No user-inputs are required.

The scripts sweeps the width of the waveguide and calculates the overlap
integral for the given mode-number.
"""

#----------------------------------------------------------------------------
# Imports from user files
# ---------------------------------------------------------------------------
# Import necessary modules
import numpy as np
import lumapi
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os 


# Import user-defined input parameters from the waveguide package
from MODE.edge_coupler.user_inputs.user_sweep_parameters import *    
from MODE.edge_coupler.waveguide_render import *
from MODE.edge_coupler.fde_region import add_fde_region  

from MODE.edge_coupler.gaussian_beam_render import *  

# ------------------------- Directories for Results ---------------------------

# specify the directory path
path_to_write = ["MODE\\Results\\edge_coupler\\Figures\\sweep_mfd\\TE",
"MODE\\Results\\edge_coupler\\lumerical_files\\sweep_mfd\\TE",
"MODE\\Results\\edge_coupler\\Figures\\sweep_mfd\\TM",
"MODE\\Results\\edge_coupler\\lumerical_files\\sweep_mfd\\TM"]
directory_to_write = ['']*len(path_to_write)

# get the current file path
current_path = os.path.abspath(__file__)

# get the directory of the current file
current_dir = os.path.dirname(current_path)


# find the project root directory by traversing up the directory 
# tree until a specific file is found
while not os.path.isfile(os.path.join(current_dir, ".gitignore")):
    # move up to the parent directory
    current_dir = os.path.dirname(current_dir)

for i in range(0,len(path_to_write)):
    directory_to_write[i] = os.path.join(current_dir, path_to_write[i])

    # create the directory if it doesn't exist already
    if not os.path.exists(directory_to_write[i]):
        os.makedirs(directory_to_write[i])
        print("Directory:" + directory_to_write[i] + "\n created successfully!")
    else:
        print("Directory:" + directory_to_write[i] + "\n already exists!")



# ---------------------------------------------------------------------------





# Create a MODE instance and turn off redraw feature
mode = lumapi.MODE()
mode.redrawoff()

# Draw the waveguide structure and add a finite-difference eigenmode (FDE) region
waveguide_draw(mode)
add_fde_region(mode)

# Add the Gaussian Mode on the Global Deck
add_gaussian_beam(mode)

# Create an empty list for mode waist and use numpy to generate a list based on user-defined parameters
waist_array = np.arange(waist_start, waist_stop, waist_step) 

# Initialize empty 2D lists to store effective index and polarization fraction for each mode and width
polariz_frac = [0]*len(waist_array)

w, h = 2, len(waist_array)
overlap_TE = [[0 for x in range(w)] for y in range(h)] 
overlap_TM = [[0 for x in range(w)] for y in range(h)] 



# Nested for loop to iterate over each waveguide width and mode - Fundamental TE
if(polarization_angle == 0):

    for mfd in range(0,len(waist_array)):
        mode.switchtolayout()    
        mode.setnamed("FDE","waist radius",waist_array[mfd])
        mode.createbeam()
        mode.run()
        mode.mesh()
        mode.findmodes()
        
        # Save the file
        file_name_mode = os.path.join(directory_to_write[1], "overlap_TE_waist_sweep_" + str(mfd) + ".lms")
        mode.save(file_name_mode)           

        
        for m in range(1,num_modes+1):
                    polariz_frac[m-1] = (mode.getdata("FDE::data::mode"+str(m),"TE polarization fraction"))
                    
                    if ( polariz_frac[m-1] > 0.5 ):   # identify the TE-like or TM-like modes
            
                        # Do something when you find the TE Mode
                        print("TE Mode " + str(m) + "\n")
                        mode.copydcard("mode"+str(m),"mode"+str(m))
                        overlap_TE[mfd] = mode.overlap("global_" + "mode"+str(m),"gaussian"+str(mfd+1))
                        mode.cleardcard("global_" +"mode"+str(m))
                        break;
            
                    else:
                        # Do something when you find the TM Mode
                        print("TM Mode " + str(m) + "\n")
                        continue;
                        
                        
                        
    
    
    
    overlap_TE_coupling = [0]*len(overlap_TE)
    overlap_TE_power = [0]*len(overlap_TE)
    
    
    
    for i in range(0,len(overlap_TE)):
        overlap_TE_coupling[i] = overlap_TE[i][0]
        overlap_TE_power[i] = overlap_TE[i][1]
        
    
    
    
    
    # Plot mode overlap integral versus waveguide width for given mode
    plt.figure(1,figsize=(512/my_dpi, 256/my_dpi), dpi=my_dpi)
    
    plt.plot(waist_array*1e6,overlap_TE_coupling,'-o', label = 'Mode Coupling')
    plt.plot(waist_array*1e6,overlap_TE_power,'-o', label = 'Power Coupling')
    plt.legend()
    plt.xlabel("width (um)")
    plt.ylabel("TE Mode Overlap (%)")
    plt.ylim([0,1])
    plt.title("tip width "+ str(np.round(wg_width*1e6,2)) + " um") 
    
    plt.legend()
    plt.xlabel("waist radius (um)")
    plt.ylabel("TE overlap (%)")

    # Save the figure files as .png     
    file_name_plot = os.path.join(directory_to_write[0], "overlap_waist_sweep" + ".png")
    plt.tight_layout()
    plt.savefig(file_name_plot, dpi=my_dpi, format="png")



    
# If you set the source polarization angle, you will get the TM mode

if(polarization_angle == 90):
    
    overlap_TM_coupling = [0]*len(overlap_TM)
    overlap_TM_power = [0]*len(overlap_TM)

    
    
    
    
    # Nested for loop to iterate over each waveguide width and mode - Fundamental TM
    for mfd in range(0,len(waist_array)):
        mode.switchtolayout()    
        mode.setnamed("FDE","waist radius",waist_array[mfd])
        mode.createbeam()
        mode.run()
        mode.mesh()
        mode.findmodes()

        # Save the file
        file_name_mode = os.path.join(directory_to_write[3], "overlap_TM_width_sweep_" + str(mfd) + ".lms")
        mode.save(file_name_mode)
        
        for m in range(1,num_modes+1):
                    polariz_frac[m-1] = (mode.getdata("FDE::data::mode"+str(m),"TE polarization fraction"))
                    
                    if ( polariz_frac[m-1] > 0.5 ):   # identify the TE-like or TM-like modes
            
                        # Do something when you find the TE Mode
                        print("TE Mode " + str(m) + "\n")
                        continue;
            
                    else:
                        # Do something when you find the TM Mode
                        print("TM Mode " + str(m) + "\n")
                        mode.copydcard("mode"+str(m),"mode"+str(m));
                        overlap_TM[mfd] = mode.overlap("global_" + "mode"+str(m),"gaussian"+str(mfd+1))
                        mode.cleardcard("global_" +"mode"+str(m))
                        break;
    
        
    for i in range(0,len(overlap_TM)):
        overlap_TM_coupling[i] = overlap_TM[i][0]
        overlap_TM_power[i] = overlap_TM[i][1]
        
    
    # Plot mode overlap integral versus waveguide width for given mode
    plt.figure(2,figsize=(512/my_dpi, 256/my_dpi), dpi=my_dpi)
    
    plt.plot(waist_array*1e6,overlap_TM_coupling,'-o', label = 'Mode Coupling')
    plt.plot(waist_array*1e6,overlap_TM_power,'-o', label = 'Power Coupling')
    
    plt.legend()
    plt.xlabel("width (um)")
    plt.ylabel("TM Mode Overlap (%)")
    plt.ylim([0,1])
    plt.title("waist radius "+ str(np.round(wg_width*1e6,2)) + " um") 

    # Save the figure files as .png
    file_name_plot = os.path.join(directory_to_write[2], "overlap_tip_width_sweep" + ".png")
    plt.tight_layout()
    plt.savefig(file_name_plot, dpi=my_dpi, format="png")

# Turn on redraw feature to update simulation layout
mode.redrawon()


# Close the session
mode.close()