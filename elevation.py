#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 20:05:27 2023

@author: miguelsolis
"""

import numpy as np
from rioxarray import open_rasterio
import pystac_client
import planetary_computer
#import xrspatial
#from datashader.transfer_functions import shade, stack
#from datashader.colors import Elevation
#import matplotlib.pyplot as plt
#import pandas as pd

class elevation:
    # Constructor
    def __init__(self):
        self.catalog = pystac_client.Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1/",
            modifier=planetary_computer.sign_inplace,
        )
        self.elevations = []
    
    # Creates and returns items from CopernicusEDM according to the tiles list
    def deliver_items(self, tile):
            search = self.catalog.search(
                collections=["cop-dem-glo-30"],
                intersects={"type": "Point", "coordinates": tile},
            )
        
            return list(search.get_items())
    
    # Extracts the raw data
    def extractraw(self, tiles):
        for tile in tiles: 
            items = self.deliver_items(tile)   
            try:
                signed_asset = planetary_computer.sign(items[0].assets["data"])
                data = open_rasterio(signed_asset.href)
                self.elevations.append(data)
            except Exception as e:
                print(f"Error reading elevation data: {e}")
        return self.elevations