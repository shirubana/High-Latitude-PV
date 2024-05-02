# -*- coding: utf-8 -*-
"""
Created on Thu May  2 09:54:05 2024

This file does a data dump from NSRDB by accessing it directly through NREL's kestrel services.
The script is currently tylored to download data above 60 degrees latitude. For May 2024, this is about 400 datapoints.

For instructions on accessing NSRDB through AWS for big data download like this, go to their documentation on setting up the instances to communicate and download/use data.
More information also available on PVDeg github developing spatial analysis capabilities for multiple functions and datasets.

Questions? mspringer, etonita, sovaitt

"""

import numpy as np
import os
import pandas as pd
import pvdeg
from datetime import timedelta


meta_aux_fp = "/projects/pvsoiling/pvdeg/data/meta_world_map_aux.csv"
weather_aux_fp = "/projects/pvsoiling/pvdeg/data/world_map_aux.h5"
save_path="/home/etonita/WeatherFiles/High-Lat_TMY_v2/"

meta_world_map_aux = pd.read_csv(meta_aux_fp, index_col=0)

print(meta_world_map_aux)

weather_arg = {}

for idx, point in meta_world_map_aux[0:437].iterrows():
    gid = idx
    database = point.weather_db
    df_weather_kwargs = point.drop('weather_db', inplace=False).filter(like='weather_')
    df_weather_kwargs.index = df_weather_kwargs.index.map(lambda arg: arg.lstrip('weather_'))
    weather_kwarg = weather_arg | df_weather_kwargs.to_dict()

    weather_df, meta = pvdeg.weather.get(
                database = database,
                id = gid,
                **weather_kwarg)
    
    df_TMY=pd.DataFrame()
    weather_df["Datetime"]=pd.to_datetime(weather_df["time_index"])
    weather_df["Datetime"]=weather_df["Datetime"] - timedelta(minutes=30)
    df_TMY["Year"]=weather_df["Datetime"].dt.year
    df_TMY["Month"]=weather_df["Datetime"].dt.month
    df_TMY["Day"]=weather_df["Datetime"].dt.day
    df_TMY["Hour"]=weather_df["Datetime"].dt.hour
    df_TMY["Minute"]=weather_df["Datetime"].dt.minute
    df_TMY["DHI"]=weather_df["dhi"]
    df_TMY["DNI"]=weather_df["dni"]
    df_TMY["Dew Point"]=weather_df["dew_point"]
    df_TMY["Surface Albedo"]=weather_df["surface_albedo"]
    df_TMY["Wind Speed"]=weather_df["wind_speed"]
    df_TMY["Temperature"]=weather_df["air_temperature"]
    df_TMY["Pressure"]=weather_df["surface_pressure"]
    df_TMY["GHI"]=weather_df["ghi"]
    df_TMY["Wind Direction"]=weather_df["wind_direction"]

    loc_name=meta["name"]
    if loc_name=="unknown":
        loc_name="lat"+str(round(meta["latitude"],2))+"-lon"+str(round(meta["longitude"],2))
    loc_name=loc_name.replace("/","-")
    loc_name=loc_name.replace(" ","-")

    print("Running for: "+loc_name)

    #header_1="Source,Location ID,City,State,Country,Latitude,Longitude,Time Zone,Elevation,Local Time Zone,Dew Point,DHI Units,DNI Units,GHI Units,Temperature Units,Pressure Units,Wind Direction Units,Wind Speed Units,Surface Albedo Units,Version"
    #header_2=meta["source"]+","+str(meta["identifier"])+","+meta["name"]+","+meta["county"]+","+meta["country"]+","+str(meta["latitude"])+","+str(meta["longitude"])+","+str(round(meta["timezone"]))+","+str(meta["altitude"])+","+str(round(meta["timezone"]))+",c,w/m2,w/m2,w/m2,c,mbar,Degrees,m/s,N/A,unknown"
    #header=header_1+"\n"+header_2

    header=pd.DataFrame()
    header["Source"]=meta["source"]
    header["Location ID"]=meta["identifier"]
    header["City"]=meta["name"]
    header["State"]=meta["county"]
    header["Country"]=meta["country"]
    header["Latitude"]=meta["latitude"]
    header["Longitude"]=meta["longitude"]
    header["Time Zone"]=round(meta["timezone"])
    header["Elevation"]=meta["altitude"]
    header["Local Time Zone"]=round(meta["timezone"])
    header["Dew Point"]="c"
    header["DHI Units"]="w/m2"
    header["DNI Units"]="w/m2"
    header["GHI Units"]="w/m2"
    header["Temperature Units"]="c"
    header["Pressure Units"]="mbar"
    header["Wind Direction Units"]="Degrees"
    header["Wind Speed Units"]="m/s"
    header["Surface Albedo Units"]="N/A"
    header["Version"]="unknown"

    df_TMY2=pd.concat([header,df_TMY],axis=0)

    df_TMY2.to_csv(save_path+"TMY_"+loc_name+".csv",index=False)
    #with open(save_path+"TMY_"+loc_name+".csv") as outfile:
    #    data=outfile.read()
    #header += "\n"
    #header += data
    #with open(save_path+"TMY_"+loc_name+".csv",'w') as fp:
    #    fp.write(header)

    print("TMY data file saved for: "+loc_name)


