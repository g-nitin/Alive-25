import sqlite3
from typing import Optional
from geopy.geocoders import Nominatim, nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pandas as pd
from time import sleep
from random import randint


# Initialize the geocoder with a cache
def init_geocoder() -> tuple[sqlite3.Connection, nominatim.Nominatim]:
    """
    Initialize the geocoder with a cache.
    :return: A tuple containing the connection to the cache database and the geocoder.
    """
    conn: sqlite3.Connection = sqlite3.connect('geocode_cache.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS cache
                    (address TEXT PRIMARY KEY, latitude REAL, longitude REAL)''')

    geolocator: nominatim.Nominatim = Nominatim(user_agent=f"my_app_{randint(0, 10000)}")
    return conn, geolocator


def geocode_address(row: pd.Series, address: str) -> tuple[Optional[float], Optional[float]]:
    """
    Geocode the address.
    :param row: A row of the dataframe. Should contain the columns 'als' and 'alsb'.
    :param address: The address as a string.
    :return: A tuple containing the latitude and longitude as floats.
    """
    if address == "":
        return None, None

    print(f"\nGeocoding address: {address}")
    conn, geolocator = init_geocoder()
    cursor = conn.cursor()  # Create a cursor object

    # Check cache first
    cursor.execute("SELECT latitude, longitude FROM cache WHERE address = ?", (address,))
    result = cursor.fetchone()
    if result:
        print(f"Cache hit for address: {address}")
        return result[0], result[1]

    # If not in cache, geocode and store
    max_retries = 5
    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(address, timeout=10)
            if location:
                print(f"Location found for address: {address}")
                cursor.execute("INSERT INTO cache VALUES (?, ?, ?)",
                               (address, location.latitude, location.longitude))
                conn.commit()
                return location.latitude, location.longitude
            else:
                # If address contains three commas then both `als` and `alsb` were used, but failed.
                # Retry with only `als` to see if that works.
                # See get_address() for more information.
                print(f"No results found for address: {address}")
                if address.count(',') == 3:
                    print("Retrying with only `als`...")
                    return geocode_address(row, get_address(row, trim=True))
                return None, None

        except (GeocoderTimedOut, GeocoderServiceError) as e:  # Retry on timeout
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt  # exponential backoff
                print(f"Error geocoding {address}: {str(e)}. Retrying in {sleep_time} seconds...")
                sleep(sleep_time)
            else:  # Max retries reached
                print(f"Max retries reached for address: {address}")

        except Exception as e:
            print(f"Unexpected error geocoding {address}: {str(e)}")
            break

    return None, None


def get_address(row: pd.Series, trim: bool = False) -> str:
    """
    Get the address from the row.
    :param row: A row of the dataframe. Should contain the columns 'als' and 'alsb'.
    :param trim: If True, only the first street name will be included in the address.
    :return: The address as a string.
    """
    # Get the street names. If the street name is missing, replace it with an empty string
    als = '' if pd.isnull(row['als']) else f"{row['als']}, "
    alsb = '' if pd.isnull(row['alsb']) else f"{row['alsb']}, "

    # If all street names are missing, return an empty string
    # Otherwise, return the address
    if als == '' and alsb == '':
        return ""
    if trim:  # Trim the address to only include the first street name
        return f"{als}South Carolina, USA"
    else:
        return f"{als}{alsb}South Carolina, USA"


def process_chunk(chunk) -> list[tuple[int, Optional[float], Optional[float]]]:
    """
    Process a chunk of the dataframe.
    :param chunk: A chunk of the dataframe.
    :return: A list of tuples containing the latitude, and longitude.
    """
    print("Processing chunk...")

    results = []
    for _, row in chunk.iterrows():
        address = get_address(row)
        lat, lon = geocode_address(row, address)
        results.append((row.name, lat, lon))
    return results
