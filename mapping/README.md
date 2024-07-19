# Mapping Incidents in SC

This folder contains the mapping of incidents in SC. The folder is organized as follows:
## scatter
  Contains files to create scatter plots of the incidents. More specifically, the files in this folder serve the following purposes:
  - `scatter.py`: Creates a scatter plot of the incidents over the data given in the `sc_data` folder at the root of the repository.
    Furthermore, the `data_statistics.md` file in the `scatter` folder contains statistics about the data used to create the scatter plot.
    Lastly, the scatter plot for different years can be found in a zip file in this folder called `sc_incidents_scatter.zip` under the `maps` folder.
    <br>A map of the 2021 year with less than 50% of the data can be found at `maps/sc_incidents_2021_reduced.html`. 
  - `heat.ipynb`: Creates a heat map with time of the incidents over time. Output found at `maps/heat_map.html`.
  - `choropleth.py`: Creates a choropleth map with time of the incidents over time. A simple choropleth map can be found at `maps/choropleth.html`.

## geocodes 
  Contains files to geocode the incidents based on their address.
  Note that the database of geocodes is not fully complete.
  
## maps
  Contains the output of the scatter plots and choropleth maps.
  <br>Note that many of the maps in this folder (ending with .html) can be visualized by appending their web address to the following url: https://htmlpreview.github.io/?
  <br>For example, the map `maps/choropleth.html` can be visualized at https://htmlpreview.github.io/?https://github.com/g-nitin/Alive-25/blob/main/mapping/maps/choropleth.html