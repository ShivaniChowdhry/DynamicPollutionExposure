# DynamicPollutionExposure
Python application to calculate dynamic air pollution exposure

Calculating dynamic air pollution exposure of an individual based on their activity
This project consists of an app that measures dynamic air pollution exposure of an individual based on their activity (location) data throughout the day after joining it with NASA's MODIS satellite data on PM 2.5 concentration available at a sq km grain.

Table of Contents
•	[General Info]
•	[Technologies Used]
•	[Features]
•	[Screenshots]
•	[Setup]
•	[Usage]
•	[Project Status]
•	[Room for Improvement]
•	[Contact]

General Information
-	The app calculates the mean exposure to PM 2.5 pollution for a given day's outdoor activity exposure.
-	The purpose of the app is to join outdoor trajectory data with pollution data at a spatiotemporal level to calculate real time pollution exposure and determine the mean exposure for the set of outdoor activities for a day.
-	The use of this app can be made in research studies about the health effects of air pollution exposure. The difficulty of relating air pollution exposure to individual health outcomes is brought on by the spatiotemporal variability in air pollutant concentrations and individuals’ movement in space and time, so it is important to model dynamic individual exposure to pollution. 
-	In future, the app will try to find a more time-wise granular data on PM2.5 levels at per sq km level to properly account for spatiotemporal variability in exposure from outdoor activities of an individual. 

Technologies used
-	Anaconda
-	Spyder
-	Jupyter
-	Python v 3.7+
Features
-	The app asks the user to upload their GPX files (downloadable from all activity trackers) for a day through “Open GPX files” button. App throws an error message if the file format is not GPX. All the GPX files uploaded by the user are then converted into a Pandas dataframe using the gpx_converter library.
-	The app considers the air pollution data from NASA’s MODIS satellite data on PM2.5 concentration. The monthly mean grid-level PM2.5 concentration data for entire North American region at the grain of a sq km (0.01 lat x 0.01 long) has been used. The app converts the MODIS data downloaded in raster (.TIFF) format to a Pandas Dataframe using georasters library.
-	The app calculates dynamic PM2.5 exposure: it takes every 60th second in the gpx file for efficient calculations after re-indexing, then loops through the gpx trajectory locations and finds the nearest sq km area from the PM2.5 data and stores its value, and adds a new column of dynamic_aqi to the gpx_df. It returns the mean value of all the new dynamic_aqi values, and presents it to the user as the final output in a text box.
-	The app also presents the trajectories overlaid on a Folium map showing a heat map made from the PM2.5 data. It shows the differential intensity of PM2.5 concentration in the areas that the user passes through during their activity.
 
 

Libraries Used and Setup
-	gpx_converter -- pip install gpx-converter
-	georasters -- pip install georasters
-	folium -- pip install folium==0.1.5
-	HeatMap from folium.plugins
-	tkinter  -- pip install tkinter
-	pandas, sys, webbrowser, os

Usage
-	The app asks the user to upload their GPX files for a day through “Open GPX files” button. App throws an error message if the file format is not gpx. All the GPX files uploaded by the user are then converted into a pandas dataframe using the gpx_converter library.
-	The app displays the mean PM 2.5 exposure for the set of gpx files uploaded.
-	It also displays a map with the trajectories overlayed with a Heatmap of the pollution data available at a sq km level.




Project Status
Project is still in progress and needs a lot of improvements as it is the first leg of my thesis dissertation project. I also need to model indoor pollution exposure and exposure during transit times spent in vehicles to get an overall estimate of daily air pollution exposure for an individual.

Room for Improvement
-	Right now, the app can’t show different activity trajectories on one single map, so it gives out different maps for different trajectories. They need to be panelized better in the future.
-	The maps also need to be a bit more interactive.

To do
-	The user should be able to select the geographical boundaries of the pollution data they want to limit their activities to for faster calculations. Same with limiting the pollution data for a certain timeframe with inputs from the user.
-	In the future, this app will also be able to take other formats for location data such as JSON used by Google Maps location history and run ML models to extrapolate the full trajectory from to and from co-ordinates. But for this first version, I have decided to use GPX file format used by most GPS trackers, which give a more accurate information on movement of people than other applications.

Acknowledgements
Data Sources:
1. Annual and monthly mean PM2.5 at 0.01 * 0.01 degrees from this site (& converted from .NC to .Tiff to work with raster data): https://sites.wustl.edu/acag/datasets/surface-pm2-5/
[Aaron van Donkelaar, Melanie S. Hammer, Liam Bindle, Michael Brauer, Jeffery R. Brook, Michael J. Garay, N. Christina Hsu, Olga V. Kalashnikova, Ralph A. Kahn, Colin Lee, Robert C. Levy, Alexei Lyapustin, Andrew M. Sayer and Randall V. Martin (2021). Monthly Global Estimates of Fine Particulate Matter and Their Uncertainty Environmental Science & Technology, 2021, doi:10.1021/acs.est.1c05309.] 

2. Personal GPX files from Apple Watch outdoor activity. (Attached.)

Code examples inspired from:
https://wustl.app.box.com/s/9073l0k8go8kehtxd5ok46dmw1q63oav (Code to convert .NC format to .TIFF format using R for MODIS PM2.5 data)
https://www.kaggle.com/code/daveianhickey/how-to-folium-for-maps-heatmaps-time-data/notebook
https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/fundamentals-raster-data/open-lidar-raster-python/
https://rasterio.readthedocs.io/en/latest/api/rasterio.plot.html#rasterio.plot.show
https://automating-gis-processes.github.io/2017/lessons/L5/interactive-map-folium.html
https://python-visualization.github.io/folium/modules.html

Contact
Created by Shivani Chowdhry (sxc200036). Email: shivani.chowdhry@utdallas.edu	
