import pandas as pd
import geopandas as gpd
import plotly.express as px
from map import check_cols
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Read data files
df = []
for year in range(2017, 2022):
    data = pd.read_csv(f'../../usc_data/sc_loc{year}.csv', low_memory=False)
    data['year'] = year

    # Check if the columns are consistent
    _, data = check_cols('lat', 'lon', data, "")

    df.append(data)

# Combine the dataframes
df = pd.concat(df, ignore_index=True)
print(f"Length of the dataset: {len(df):,}")

# Group by county and year, count accidents
accidents_by_county_year = df.groupby(['cty', 'year']).size().reset_index(name='accidents')

county_dict = {
    1: 'Abbeville', 2: 'Aiken', 3: 'Allendale', 4: 'Anderson', 5: 'Bamberg',
    6: 'Barnwell', 7: 'Beaufort', 8: 'Berkeley', 9: 'Calhoun', 10: 'Charleston',
    11: 'Cherokee', 12: 'Chester', 13: 'Chesterfield', 14: 'Clarendon', 15: 'Colleton',
    16: 'Darlington', 17: 'Dillon', 18: 'Dorchester', 19: 'Edgefield', 20: 'Fairfield',
    21: 'Florence', 22: 'Georgetown', 23: 'Greenville', 24: 'Greenwood', 25: 'Hampton',
    26: 'Horry', 27: 'Jasper', 28: 'Kershaw', 29: 'Lancaster', 30: 'Laurens',
    31: 'Lee', 32: 'Lexington', 33: 'McCormick', 34: 'Marion', 35: 'Marlboro',
    36: 'Newberry', 37: 'Oconee', 38: 'Orangeburg', 39: 'Pickens', 40: 'Richland',
    41: 'Saluda', 42: 'Spartanburg', 43: 'Sumter', 44: 'Union', 45: 'Williamsburg',
    46: 'York'
}

# Replace the numerical representation with county names
accidents_by_county_year['cty'] = accidents_by_county_year['cty'].replace(county_dict)

counties_gdf = gpd.read_file('South Carolina County Boundaries.geojson')

# Merge accident data with geospatial data
merged_data = counties_gdf.merge(accidents_by_county_year, left_on='name', right_on='cty')

# Calculate the center of South Carolina
center_lat, center_lon = 33.8361, -81.1637

# Create the Mapbox choropleth map
fig = px.choropleth_mapbox(
    merged_data,
    geojson=merged_data.geometry,
    locations=merged_data.index,
    color='accidents',
    animation_frame='year',
    color_continuous_scale="Viridis",
    range_color=(0, merged_data['accidents'].max()),
    mapbox_style="carto-positron",
    zoom=6.5,
    center={"lat": center_lat, "lon": center_lon},
    opacity=0.7,
    labels={'accidents': 'Number of Accidents'},
    hover_name='name',  # Add county name to hover info
    hover_data={'accidents': True, 'name': False},  # Show accidents, hide redundant name
    title='Traffic Accidents in South Carolina Counties Over Time'
)

# Update the map layout
# Possible mapbox styles:
#   From various public tile servers: "carto-positron", "carto-darkmatter", "open-street-map"
#   From Mapbox: "basic", "streets", "outdoors", "light", "dark", "satellite", or "satellite-streets"
#   Source: https://plotly.com/python/mapbox-layers/
fig.update_layout(
    mapbox_style="satellite-streets",
    mapbox=dict(
        accesstoken=getenv('mapbox'),
        center=dict(lat=center_lat, lon=center_lon),
        zoom=6.5
    ),
    margin={"r": 0, "t": 40, "l": 0, "b": 0}
)

# Show the figure
fig.write_html("../maps/choropleth-mapbox-satellitestreets.html")
