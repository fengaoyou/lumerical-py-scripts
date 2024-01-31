#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# @author: Georgios Gcharalampous (gcharalampous)
# version ='1.0'
# ---------------------------------------------------------------------------
"""
No user-inputs are required.

The purpose of this script is to take the parameters from the 
'simulation_parameters.py' file and render the FDE region

                                   
                                ^ y-axis               
                                |                      
                                |                      
                                |                      
                                |                      
                                |                      
                              z o ------------- >  x-axis
                                                                                                                                      
                                                         
                     +---------------------------------+                                                                                 
                     |  +---------------------------+  |                                                                                 
                     |  ||-------------------------||  |                                                                                 
                     |  ||       Claddding         ||  |                                                                       
                     |  ||      +----------+       ||  |                                                                                 
                     |  ||      |          |       ||  |                                                                                 
                     |  ||      |   Core   |       ||  |                                                                                 
                     |  ||      |          |       ||  |                                                                                 
                     +--||-------------------------||--+                                                                                 
                     |  ||           Box           ||  |                                                                                 
                     +--||-------------------------||--+                                                                                 
                     |  ||                         ||  |                                                                                 
                     |  ||                     FDE ||  |                                                                                 
                     |  ||-------------------------||  |                                                                                 
                     |  +---------------------------+  |                                                                                 
                     |            Substrate            |                                                                                 
                     +---------------------------------+                                                                                 
                                                                                                                                       
The dimensions of the FDE and mesh region are defined from the 
'user_simulation_parameters.py'. 

Remember to leave enough space within your FDE region to allow
the devices to decay enough avoiding interfering with the simulation
boundaries.

"""
import lumapi
from config import *


#----------------------------------------------------------------------------
# Imports from user files
# ---------------------------------------------------------------------------

from DEVICE.pin_modulator.user_inputs.user_simulation_parameters import *  
from DEVICE.pin_modulator.user_inputs.user_materials import *  
from DEVICE.pin_modulator.waveguide_render import waveguide_draw

def add_charge_region(device):

    # Add the mesh and the FDE regions
    device.addchargesolver()
    device.addchargemesh()
    device.addchargemonitor(name = "charge_monitor")
    device.addbandstructuremonitor(name = "band_monitor")

    # Adds the doping
    device.adddope(name = "pepi")
    device.adddope(name = "p++")
    device.adddope(name = "n++")
    
    # Adds the anode and cathode
    device.addelectricalcontact(name = "anode")
    device.addelectricalcontact(name = "cathode")

    # Adds the recombination modes
    device.addsurfacerecombinationbc(name = "semi_oxide")
    device.addsurfacerecombinationbc(name = "semi_metal")
    
    configuration = (
        
    ("CHARGE", 
              (("min edge length", min_edge_length),
              ("max edge length", max_edge_length))),

        
    ("CHARGE::mesh", 
             (("x", 0.),
              ("z", 0),
              ("y min", 0.),
              ("x span", wg_width),
              ("y max", wg_thickness),
              ("max edge length", max_edge_length_mesh_override),
              ("enabled", mesh_enable))),
    
    ("simulation region",
             (("dimension", "2D Z-Normal"),
              ("x", 0.),
              ("y", 0.),
              ("z", 0.),
              ("x span", simulation_span_x),
              ("y min", simulation_min_y),
              ("y max", simulation_max_y))),  
    
    ("CHARGE::pepi", 
             (("x min", -simulation_span_x/2 - 0.5e-6),
              ("x max", simulation_span_x/2 + 0.5e-6),
              ("y min", -30e-9),
              ("z", 0.),
              ("y max", wg_thickness + 30e-9),
              ("z span", 5e-6),
              ("dopant type","p"),
              ("concentration", pepi_p_doping*1e6))),
    
    ("CHARGE::p++", 
             (("x min", -simulation_span_x/2 - 0.5e-6),
              ("x max", -offset_Ppp),
              ("y min", -30e-9),
              ("z", 0.),
              ("y max", wg_thickness + 30e-9),
              ("z span", 5e-6),
              ("dopant type","p"),
              ("concentration", Ppp*1e6))),
    
    
    ("CHARGE::n++", 
             (("x min", offset_Nnn),
              ("x max", simulation_span_x/2 + 0.5e-6),
              ("y min", -30e-9),
              ("z", 0.),
              ("y max", wg_thickness + 30e-9),
              ("z span", 5e-6),
              ("dopant type","n"),
              ("concentration", Nnn*1e6))),
    
    ("CHARGE::charge_monitor",
             (("monitor type", 7),
              ("integrate total charge", 1),
              ("x", 0.),
              ("y", 0.),
              ("z", 0.),
              ("x span", simulation_span_x),
              ("y min", simulation_min_y),
              ("y max", simulation_max_y))),

    ("CHARGE::band_monitor",
             (("monitor type", 2),
              ("x", 0.),
              ("y", slab_thickness/2),
              ("z", 0.),
              ("x span", simulation_span_x))),



    ("CHARGE::boundary conditions::anode",
             (("bc mode", "steady state"),
              ('sweep type', 'single'),
              ('voltage', v_anode),
              ("surface type", "solid"),
              ("solid", "metal_anode"))),


    ("CHARGE::boundary conditions::cathode",
             (("bc mode", "steady state"),
              ('sweep type', 'single'),
              ('voltage', v_cathode),
              ("surface type", "solid"),
              ("solid", "metal_cathode"))),
    
    
    
    ("CHARGE::boundary conditions::semi_oxide",
             (("enabled", semi_oxide_enabled),
              ("surface type", "material:material"),
              ('material 1', wg_material),
              ('material 2', oxide_material),
              ("electron velocity", e_velocity_semi_oxide),
              ("hole velocity", h_velocity_semi_oxide),
              ("apply to majority carriers", 1))),
  
    
    ("CHARGE::boundary conditions::semi_metal",
             (("enabled", semi_metal_enabled),
              ("surface type", "material:material"),
              ('material 1', wg_material),
              ('material 2', contact_material),
              ("electron velocity", e_velocity_semi_metal),
              ("hole velocity", h_velocity_semi_metal),
              ("apply to majority carriers", 0))),
  
     
    
    )
    
    

    # Populate the waveguide simulation region

    for obj, parameters in configuration:
           for k, v in parameters:
               device.setnamed(obj, k, v)
               
               
if(__name__=="__main__"):
    with lumapi.DEVICE(hide=True) as device:
    
      # Draw the waveguide structure using a custom function
      device.redrawoff()
      waveguide_draw(device)
      
      # Draw the Simulation Region
      add_charge_region(device)


      device.save(PIN_MODULATOR_DIRECTORY_WRITE_FILE + "\\pin_waveguide_render.ldev")


