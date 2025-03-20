#importing tkinter for the gui
import tkinter as tk
from tkinter import filedialog
#importing gpx_converter to convert gpx into pandas df
from gpx_converter import Converter
#importing georasters to convert a tiff file into a pandas df
import georasters as gr
import pandas as pd
import sys
import folium
# import webbrowser,os
import time
from folium.plugins import HeatMap

#importing the PM 2.5 data for entire North American region at the grain of a sqkm(0.01 lat x 0.01 long) 
aqi = gr.from_file('C:/Users/14699/Music/2021.tif')
#converting to pandas df
aqi_df_full = aqi.to_pandas()
#Filtering for DFW lat long boundaries for efficient join to outdoor trajectory gpx
aqi_df_fil = aqi_df_full[(aqi_df_full['y'] >= 31) & (aqi_df_full['y'] <= 34) & (aqi_df_full['x'] >= -97.5) & (aqi_df_full['x'] <= -96.5)]
#re-indexing the filtered df for error-free referencing
aqi_df = aqi_df_fil.reset_index(drop=True)   

#Function to visualize and display the trajectory and PM 2.5 data
def display_map(gpx_df):
    #Folium map to display the trajectory
    route_map = folium.Map(
    location=[gpx_df['latitude'].mean(), gpx_df['longitude'].mean()],
    zoom_start=15,
    tiles='CartoDBPositron',
    width=1024,
    height=600)
    coordinates = [tuple(x) for x in gpx_df[['latitude', 'longitude']].to_numpy()]
    folium.PolyLine(coordinates, weight=6).add_to(route_map)    
    #Folium map to show heat map of the PM 2.5 data
    aqi_df['weight'] = aqi_df['value'] / aqi_df['value'].abs().max()
    map_values1 = aqi_df[['y','x','weight']]
    data = map_values1.values.tolist()
    hm = HeatMap(data,gradient={0.1: 'blue', 0.3: 'lime', 0.5: 'yellow', 0.7: 'orange', 1: 'red'}, 
                min_opacity=0.05, 
                max_opacity=0.9, 
                radius=50,
                use_local_extrema=False)
    route_map.add_child(hm)
    date = time.time()
    file_name = 'outputmap'+ str(date) +'.html'
    route_map.save(file_name)
    # webbrowser.open('file://' + os.path.realpath('C:/Users/14699/Desktop/'+file_name))

#Function to calculate dynamic aqi exposure
def dynamic_aqi(gpx_df):
    #filtering the data to take every 60th second in the gpx file for efficient calculations and re-indexing
    gpx_aqi_df_60_oi = gpx_df.iloc[::60, :]
    gpx_aqi_df_60 = gpx_aqi_df_60_oi.reset_index(drop=True)
    #looping through the gpx trajectory locations and finding the nearest sqkm area from the aqi df
    for i,row in gpx_aqi_df_60.iterrows():
        #adding a new column dynamic_aqi to the gpx_df after joining to the aqi_df 
        gpx_aqi_df_60.at[i,'dynamic_aqi'] = (aqi_df[(aqi_df['row'] == aqi_df.iloc[(aqi_df['y']-row['latitude']).abs().argsort()[0]]['row'])
           & (aqi_df['col'] == aqi_df.iloc[(aqi_df['x']-row['longitude']).abs().argsort()[0]]['col'])]['value'].values[0])    
    #calculating the mean of the new dynamic_aqi for the set of gpx files uploaded
    return round(gpx_aqi_df_60['dynamic_aqi'].mean(),4)
        

#tkinter upload button function
def UploadAction(event=None):
    #defining a global variable to hold the filepath of the gpx files uploaded
    global gpx_filepath
    #prompt to upload gpx files
    filenames = filedialog.askopenfilenames(title = "Open 'gpx' file(s)")
    #looping through the set of selected gpx files
    for filename in filenames:
        #throw a warning if the file format is not gpx
        if '.gpx' not in filename:
            tk.messagebox.showinfo(title='Warning', message = filename + 'file is not in gpx format!')
        #convert all the gpx files into pandas df and append them into one df
        else:
            gpx_df_map = Converter(input_file = filename).gpx_to_dataframe()
            display_map(gpx_df_map)
            gpx_df = pd.DataFrame()
            gpx_df = gpx_df.append(Converter(input_file = filename).gpx_to_dataframe(), ignore_index = True)
    #call the dynamic aqi calculating function passing the unioned gpx df
    dynamic_aqi_calc = dynamic_aqi(gpx_df)
    #print the output mean dynamic_aqi
    print_msg = 'Dynamic mean PM 2.5 exposure for the gpx files selected per day is '+ str(dynamic_aqi_calc)
    tk.messagebox.showinfo(title='Output', message=print_msg)
    
    #exit
    root.withdraw()
    sys.exit()
        
            
    
#Logic for the tkinter GUI and calling main
root = tk.Tk()
root.geometry("700x350")
label = tk.Label(root, text="Select the Button to Open the File", font=('Aerial 11'))
label.pack(pady=30)
button = tk.Button(root, text='Select gpx Files', command=UploadAction)
button.pack()

root.mainloop()

