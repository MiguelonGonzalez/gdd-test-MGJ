# Geospatial Data Developer Take Home Challenge

Responses from Miguel González Jiménez

All the responses, with their explanation and file indications are included in the Word Document called 'Answers', within results folder.

## Part 1. Setting up the infrastructure with Docker :whale: (3 points)

The first part of the challenge is to set up a Docker image that fulfills the following requirements:

- Runs **PostgreSQL**, with minimum major version 14 
- Has **PostGIS** extension installed, with minimum major version 3
- Has the [**h3-pg** extension](https://github.com/zachasme/h3-pg/tree/main/docs) installed

## Part 2. Building a suitability analysis tool :earth_americas: (7 points)

<img src="assets/img/peltophorum_dubium.png" width="400" height="300">

Image: _Peltophorum dubium_ in early stages of growth in Argentinian plant nursery.

**The challenge** is to create a tool (this could be a web application, an API, a notebook or simply a script, you're free to choose) using Python as your main language (SQL is also your friend if you like) that answers the following requirements:

- Allows an input geospatial dataset in one of the following formats: GeoParquet, ESRI Shapefile, GeoJSON, KML. This dataset has a geometry column that represents the area of interest of our team, the area will always be a **region within the argentinian province of Corrientes, generally ranging from 100-5.000 hectares**. You can find an example area of interest in the [data folder](data/) in GeoJSON format.

The answer to this question is the cambium_tools module, which is operated (as an example) from the jupyter notebook 'Part 2.1.ipynb'.
This module contains some other useful function.

- Provides a **visual output (map)** that has areas divided into 3 categories representing the **suitability of the area for our projects** (Low, Medium, High) and any additional information that may help business users take data-driven decisions (total usable area, etc).

The files generated in this GIS analysis are within Layers folder, which could not be uploaded to github. They are available [here](https://drive.google.com/drive/folders/1SfHQhcZvCr05-QabxZvqyv_s_9TFQwE7?usp=sharing) on Google Drive.

The jupyter notebook that answer this question is 'Part2.2.ipynb'. The output map is kept within results/map folder, both the complete map and a small sample.

Since at the beggining I tried this exercise using only Python, at 'Extra.ipynb' notebook you can find the initial approach to the GIS analysis using `rasterio` library. Then I changed to a GIS desktop program to save time.