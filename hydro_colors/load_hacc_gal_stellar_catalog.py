# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_load_hacc_gal_stellar_catalog.ipynb.

# %% auto 0
__all__ = ['GALS_DIR', 'GALS_FILE', 'Z_SOLAR_HACC', 'Z_SOLAR_PADOVA', 'H0', 'load_fsps_spectral_library']

# %% ../nbs/01_load_hacc_gal_stellar_catalog.ipynb 3
import numpy as np
import os
import matplotlib.pylab as plt

# %% ../nbs/01_load_hacc_gal_stellar_catalog.ipynb 4
GALS_DIR = '../hydro_colors/data/test_hacc_stellar_catalog/'
GALS_FILE = 'Gals_Z0.txt'

# %% ../nbs/01_load_hacc_gal_stellar_catalog.ipynb 5
Z_SOLAR_HACC = 0.012899 # Solar metallicity value in HACC Hydro
Z_SOLAR_PADOVA = 0.019 # Solar metallicity value in Padova 
H0 = 71.0 # Hubble Constant in HACC Hydro

# %% ../nbs/01_load_hacc_gal_stellar_catalog.ipynb 6
def _convert_metallicity(hacc_metallicity:np.array=None, # Metallicity values from HACC  
                         Z_solar:np.float32=Z_SOLAR_PADOVA, # Z_solar value from Padova
                        )-> np.array: # Metallicity array in Z/Z_solar units
    return hacc_metallicity/Z_solar

def _convert_age(hacc_age:np.array=None, #Age in 1/H0 units 
                 H0:np.float32=H0, # LastJourney H0 value
                )-> np.array: #Age in Gyr 
    '''
    (hacc_age is in 1/H0 units)
    H0 = (71 km/s/Mpc) x (1 Mpc/3.08 x 1e19 km) = 2.37 x 1e−18 1/s
    '''
    # https://www.e-education.psu.edu/astro801/content/l10_p5.html
    
    H0_per_sec = H0*(1/(3.08*1e19)) #seconds
    one_over_H0 = 1/H0_per_sec/(3.1536*1e16)
    age_hydro_gyr = hacc_age*one_over_H0
    
    return age_hydro_gyr

# %% ../nbs/01_load_hacc_gal_stellar_catalog.ipynb 7
def load_fsps_spectral_library(fileIn:str=GALS_DIR+GALS_FILE, # Input galaxy catalog file from HACC hydro sim
                              Z_solar:np.float32=Z_SOLAR_PADOVA, #Solar metallicity
                              H0:np.float32=H0, # Hubble constant
                              ) -> tuple: # galaxy_tag, stellar_indices, metallicity, mass, age, x, y, z
    
    gal_tag, stellar_idx, metal, mass, age, x, y, z = np.loadtxt(fileIn, 
                                                                 skiprows=1, 
                                                                 unpack=True)
    
    metal_z_solar = _convert_metallicity(metal, Z_solar)
    
    age_gyr = _convert_age(age, H0)
    
    return gal_tag, stellar_idx, metal_z_solar, mass, age_gyr, x, y, z
