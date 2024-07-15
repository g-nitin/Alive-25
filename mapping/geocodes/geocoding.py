import pandas as pd
import geopandas as gpd
import folium
from collections import defaultdict
import multiprocessing as mp
from numpy import array_split
from geocoding_funcs import *


def geocode() -> pd.DataFrame:
    """
    Geocode the street locations using multiprocessing.
    :return: A dataframe containing the street locations with latitude and longitude.
    """

    # Load the data
    df = pd.read_csv('../sc_data/sc_loc2018.csv').sample(frac=0.1)
    print(f"Number of rows: {df.shape[0]:,}")

    # Split the dataframe into chunks
    num_processes = mp.cpu_count() - 8
    print(f"Number of processes: {num_processes}")

    print(f"Splitting Array...")
    chunks = array_split(df, num_processes)

    # Use multiprocessing to geocode in parallel
    print(f"Use multiprocessing...")
    with mp.Pool(num_processes) as pool:
        all_results = pool.map(process_chunk, chunks)

    # Flatten results and update dataframe
    print(f"Flattening Results...")
    results_dict = defaultdict(lambda: [None, None])
    for chunk_result in all_results:
        for idx, lat, lon in chunk_result:
            results_dict[idx] = [lat, lon]

    df['latitude'] = df.index.map(lambda idx: results_dict[idx][0])
    df['longitude'] = df.index.map(lambda idx: results_dict[idx][1])

    # Remove rows with failed geocoding
    df = df.dropna(subset=['latitude', 'longitude'])
    print(f"Number of rows after dropping failed geocoding: {df.shape[0]:,}")

    return df


def create_map(df: pd.DataFrame) -> None:
    """
    Create a map of the street locations.
    :param df: A dataframe containing the street locations with latitude and longitude.
    """
    print("Creating map...")

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

    # Create a map centered on the mean point
    center = gdf.geometry.centroid.mean()
    m = folium.Map(location=[center.y, center.x], zoom_start=10)

    # Add points to the map
    for idx, row in gdf.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"ALS: {row['als']}, ALSB: {row['alsb']}, ALSS: {row['alss']}",
        ).add_to(m)

    file_name: str = "street_locations_map.html"
    m.save(file_name)
    print(f"Map saved as {file_name}")


if __name__ == "__main__":
    df = geocode()
    create_map(df)
