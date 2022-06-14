# solar-images-downloader

This project stores a collection of small scripts used to extract solar images and their metadata from different sources.

It is divided into two subprojects:
- image-script: Generates a script to download images from sdo dot gsfc dot nasa dot gov.
- solar-monitor: Result is the sunspot information extracted from solarmonitor dot org.

## image-script

This module generates a script with several `wget`s that can be used to download the images.
For simplicity at `main`, we define the dates for the start and end of the images that will download.

### To run
At the root folder of this project, do:

#### Create target folder

``
$ mkdir target
``

It will create a fold used as output for the scripts.

#### Install dependency

``
$ python3 -m pip install utils
``

It will install the internal needed dependency.

#### Run application 

``
$ python3 -m image-script.image_script_generator
``

It will create at `target` a script called `wgets.txt` with all that can be run to extract all the solar images.


## solar-monitor

This module is responsible for extracting the information that describes the sunspots and loading it to a data source that can be json or PostgreSQL.
The module is divided into two runners:

### solar_request

It is used to extract the sunspot information from solarmonitor dot org.
For simplicity, the range is hardcoded in the `main` function.
As an output, solar_request generates a `json` will all solar data available 

#### To run

At the root folder of this project, do:

##### Create target folder

``
$ mkdir target
``

It will create a fold used as output for the scripts.

##### Install dependencies

``
$ pip3 install -r requirements.txt
``

It will install the external needed dependencies.

``
$ python3 -m pip install utils
``

It will install the internal needed dependency.

##### Run application

``
$ python3 -m solar-monitor.solar_request
``

It will create at `target` a json called `sunspots.json` with all extracted sunspot information.


### database_loader

It will load the information from `sunspots.json` to a PostgreSQL database.
That step can be very helpful to manipulate the extracted information.

*Warning*: only not empty sunspots are loaded. And by not empty, it means sunspots we have the *McIntosh* available.

#### To run

Assuming the `sunspots.json` is created.

At the root folder of this project, do:

##### Start the database

``
$ mkdir -p target/vol
``

Create the vol folder for the database.

``
$ docker run -d --rm -P -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD="password" --name solar-postgres -v {project_root_folder}/target/vol:/var/lib/postgresql/data postgres
``

That will start a PostgreSQL database. 
Don't forget to replace `{project_root_folder}` before running the command.

##### Install dependencies

``
$ pip3 install -r requirements.txt
``

It will install the external needed dependencies.

##### Run application

``
$ python3 -m solar-monitor.database_loader
``

It will create the database table and load the sunspot data to it.
The configuration for the PostgreSQL connection is hardcoded in the script and reflects the one used to connect to the docker database image.

## Support

In case of any bugs and/or questions, please contact the author at carlossilveirajr.

## Acknowledge

The author would like to thank NASA for the access and support to its data. 
And the SolarMonitor dot org for access to the data.
