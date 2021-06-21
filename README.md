SOLARNET Data Archive (SDA)
===========================
The SDA is an application supported by the [SOLARNET](http://www.solarnet-east.eu/) project, funded by the European Commission’s FP7 Capacities Programme under the Grant Agreement 312495.

It's purpose is to collect metadata from as many solar observations as possible, especially those made thanks to the SOLARNET project, in a common repository and make them available to the scientific community.

The first version was released in February 2016, and the second version is currently in active development

SDA API
-------
The SDA API is a [RestFul](https://en.wikipedia.org/wiki/Representational_state_transfer) API accessible at the url ...TBD.../api/v1/

It allows to create/read/update/delete metadata in the archive and find the url of the corresponding data. It also allows to create/read/update/delete data selections.

The API documentation is accessible at ...TBD.../api/doc/

Different tools have been developped to access the API:
- A web application, the [Solar Virtual Observatory](https://github.com/bmampaey/SVO/) (SVO) accessible at ...TBD.../SVO
- A python client, the [SOLARNET-python-client](https://github.com/bmampaey/SOLARNET-python-client)
- An IDL client, the [SOLARNET-IDL-client](https://github.com/bmampaey/SOLARNET-IDL-client)

Adding a new dataset
--------------------

Below we use the following terms:
- *dataset*: global information about the dataset, such as  instrument, telescope, characteristics, ...
- *metadata*: specific information about individual files in the dataset, such as date of observation, wavelength, etc. (Typically fits keywords)
- *keyword*: the columns name of the metadata table, they usually correspond to the Fits keywords.
- *data location*: specific information about the data itself, such as the url of the file, it's size, a thumbnail, etc. There can be more the one metadata for a single data location (for example if there is several HDU in a fits file).

Each of these correspond to a table in the database (DB)
- *SDA admin*: user that has the right to create, update and delete any information in the system
- *dataset admin*: user that can create, update and delete information only for a spefic dataset, it's metadata and data location

Here are the steps to add a dataset:

### Add the dataset description
As the SDA admin, connect to the [admin page](...TBD.../SDA/admin) and add, if necessary the instrument and the telescope, and then the dataset.

Then add a group with the same name as the dataset id. Create, if necessary, the dataset admins, __make them staff__, and add them to the group.

### Add the keywords
There is 2 ways of adding the keywords:

1. Manually using the [admin page](...TBD.../SDA/admin). For this connect as one of the dataset admin and add each keyword in the DB.

2. Use the `extract_keywords` django command<sup>[1](#1)</sup> to parse several Fits files. The command will try to guess the correct values for the keywords and save them to the DB. The more file you provide, the better the results will be. If possible try to use files spread over the entire dataset, instead of consecutive files (this will allow to detect changes over time in the header of the files). When it is done, do verify the discovered keyword and correct them using the admin page like in 1.

### Generate the metadata model and create the DB table
Using the `write_model_file` django command<sup>[1](#1)</sup>, create the model for the metadata. Then execute the django commands `makemigrations` and `migrate` to create the DB table of the metadata.

### Add the admin definition
Add the admin definition class and register the metadata model in the metadata/admin.py file. (See other metadata admin classes for example)

### Add the tastypie resource classes
Add the ressource definition class to the metadata/resources.py. Register the resource created to the api in the SDA/api.py file

Adding data location and metadata to the DB
-------------------------------------------
There is 2 ways of adding data location and metadata:

1. Use the RestFul api to post the information.

2. Use the `populate` django command<sup>[1](#1)</sup> to fetch the information through http. This requires to create a record definition class for the metadata, which specifies how to convert the fits header to the correct values for the DB, in the metadata/records folder.

Adding tags to metadata
-----------------------
There is 2 ways of adding tags to metadata:

1. Use the RestFul api to post the information.

2. Manually using the [admin page](...TBD.../SDA/admin). For this connect as one of the dataset admin and add each tag in the DB.

Mounting the data Selection file system
---------------------------------------

To allow the download of data selections via FTP, a Pseudo filesystem has been develloped to create the directory tree corresponding to the data selections. To mount it use the `mount_filesystem` django command<sup>[1](#1)</sup>


---------------------------------------------------------------------------
#### Footnotes
<a name="#1">1</a>: A django command is a script that is executed in the context of django. To execute the command, execute the manage.py file in the SDA folder followed by the command name and it's parameters. For example `cd SDA; ./manage.py write_model_file eit` will create the model file for the eit dataset
