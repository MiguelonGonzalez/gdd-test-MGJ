# Geospatial Data Developer Take Home Challenge

## Intro

Welcome to the Geospatial Data Developer Take Home Challenge! 

In Cambium, we're growing our data toolset and it is important that developers are capable and flexible enough to learn and adapt to new technologies if needed. 

The challenge is divided into two parts which value is presented below. We're aware that this test is quite open, as we intend to give value to innovative approaches and not that much to applying tool A or B, the whole assignment should take 1-3 days at most (you can take the time you need to resolve it). Please also note that the bonus section is completely optional, we know that these THT take time and we value your effort. 

The delivery format is up to you, it can be a GitHub repository, a .zip file, a Google Drive folder, or whatever you prefer.

We're excited to see how you solve it, please take your time and be aware that there is no one unique approach to it, feel free to use any resources you want and more importantly, enjoy it.


## Part 1. Setting up the infrastructure with Docker :whale: (3 points)

While we wrangle data at different levels and stages of maturity, PostgreSQL and its extensions ecosystem has demonstrated to be great at solving quite a lot of the challenges we face in our day to day, specially when it comes to answering questions that lay on different geospatial data sources and types, including raster, vector and spatial index (H3) data mainly.

The first part of the challenge is to set up a Docker image that fulfills the following requirements:

- Runs **PostgreSQL**, with minimum major version 14 
- Has **PostGIS** extension installed, with minimum major version 3
- Has the [**h3-pg** extension](https://github.com/zachasme/h3-pg/tree/main/docs) installed

### Bonus part: Running on Kubernetes :anchor: (2 bonus points)

We can run our database on Kubernetes using the [Cloud Native PG Operator](https://cloudnative-pg.io/) for as long as we ensure that our Docker image is compatible, see [this section](https://cloudnative-pg.io/documentation/1.22/container_images/) from the CNPG documentation for further details.

>NOTE: If you're not familiar with CNPG, the docs (and specially the [Quickstart](https://cloudnative-pg.io/documentation/1.22/quickstart/) section) are your friend!

Can you set up a compatible image and run it on a Kubernetes cluster? You can use [minikube](https://minikube.sigs.k8s.io/docs/start/) or the managed cluster of your choice (EKS, GKE, AKS, etc.)

## Part 2. Building a suitability analysis tool :earth_americas: (7 points) 

One of the main type of projects we develop at Cambium are Afforestation, Reforestation, and Revegetation (ARR). To analyze the areas that can be of interest, we leverage different types of data including remote sensing information from different providers. 

Our projects require that the area we choose does not correspond to wetlands or forests category today nor 5 years prior to the starting date of the project (let's say project start date is March 2025 for simplicity sake). 

For this exercise we will simplify the ecological needs of our project's key species [_Peltophorum dubium_](https://es.wikipedia.org/wiki/Peltophorum_dubium) to well-drained soils (minimum slope of 1%, height above the nearest drainage >= 1 m). Any additional ecological aspects considered are welcome but not required. 

<img src="assets/img/peltophorum_dubium.png" width="400" height="300">

Image: _Peltophorum dubium_ in early stages of growth in Argentinian plant nursery.



**The challenge** is to create a tool (this could be a web application, an API, a notebook or simply a script, you're free to choose) using Python as your main language (SQL is also your friend if you like) that answers the following requirements:

- Allows an input geospatial dataset in one of the following formats: GeoParquet, ESRI Shapefile, GeoJSON, KML. This dataset has a geometry column that represents the area of interest of our team, the area will always be a **region within the argentinian province of Corrientes, generally ranging from 100-5.000 hectares**. You can find an example area of interest in the [data folder](data/) in GeoJSON format.

- Provides a **visual output (map)** that has areas divided into 3 categories representing the **suitability of the area for our projects** (Low, Medium, High) and any additional information that may help business users take data-driven decisions (total usable area, etc).


>NOTE: You don't necessarily need to use the PostgreSQL + PostGIS configuration from the previous step to solve this part of the challenge, we know that there are a bunch of tools out there and there might be another one that is better suited for the job. Simply explain the reasoning behind your choice.

You can use any datasets you may find interesting, we're listing some in case those are any useful!

* Land Use Land Cover datasets at 10m resolution available in the [Planetary Computer Hub](https://planetarycomputer.microsoft.com/dataset/io-lulc-annual-v02) or Dynamic World V1 avialable in the [Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1#bands) platform.

* Global 30m Height Above Nearest Drainage (HAND) dataset available in [Google Earth Engine](https://gee-community-catalog.org/projects/hand/) (it's also available in other platforms such as the [Registry of Open Data on AWS](https://registry.opendata.aws/glo-30-hand/))

* ALOS World 3D-30m elevation dataset available in the [Planetary Computer Hub](https://planetarycomputer.microsoft.com/dataset/alos-dem)

* [Protected areas in Argentina](https://dnsg.ign.gob.ar/apps/api/v1/capas-sig/Geodesia+y+demarcaci%C3%B3n/L%C3%ADmites/area_protegida/json) 


### Additional questions

- What kind of aspects would you take into account if you were assigned with the task of implementing this type of analysis at scale?

- How can you ensure that the output result is consistent over time and responds to the data quality business users expect?

- If one or more of the input data sources vary with time by their nature (e.g., land use change, deforestation, etc.), how would you approach this challenge? How can we compare the results of the analysis today vs a few months ago?


Have fun!