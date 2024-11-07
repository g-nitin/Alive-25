# Plotting Scripts

This directory contains scripts for plotting maps and other visualizations of the data. The files are as follows:

- `scatter.py`: A script for plotting scatter plot of the data.
    - Required files : 
      - `data/south carolina.geojson`: [download link](https://github.com/glynnbird/usstatesgeojson/blob/master/south%20carolina.geojson)
      - `data/South Carolina County Boundaries.geojson`: [download link](https://cartographyvectors.com/map/1123-south-carolina-with-county-boundaries)
    - Command Line Arguments:
        - `csv_file`: The path to the CSV file containing the data to be plotted.
        - `--print_stats`: An optional flag indicating whether to print the statistics of the data. Default is `False`.
    - Usage: `python scatter.py <csv_file> [--print_stats]`
    - Output: A scatter plot of the data under the `output` directory and a statistics markdown file under the `output` directory if the `--print_stats` flag is used.
- `choropleth.py`: A script for plotting choropleth map of the data.
    - Required files : 
      - `data/South Carolina County Boundaries.geojson`: [download link](https://cartographyvectors.com/map/1123-south-carolina-with-county-boundaries)
    - Command Line Arguments:
        - `csv_file`: The path to the CSV file containing the data to be plotted.
    - Usage: `python choropleth.py <csv_file>`
    - Output: A choropleth map of the data under the `output` directory.
