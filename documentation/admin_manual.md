# Server administrator manual

Below we use the following terms:
- **dataset** global information about the dataset, such as  instrument, telescope, characteristics, ...
- **metadata** specific information about individual files in the dataset, such as date of observation, wavelength, etc. (Typically FITS keywords)
- **keyword** the columns name of the metadata table, they usually correspond to the FITS keywords.
- **data location** specific information about the data itself, such as the url of the file, it's size, a thumbnail, etc. There can be more than one metadata for a single data location (for example if there is several HDU in a fits file).
- **server admin** user that has the right to create, update and delete any information in the system (i.e. he has superuser status)
- **dataset admin** user that can create, update and delete information only for a specific dataset, the associated keywords, metadata and data location (i.e. he belongs to the dataset user_group and has staff status)
- **management command** a script that is executed in the context of django, to execute such a command, execute the script `/opt/SOLARNET/server/manage.py` followed by the command name and it's parameters

## Adding a new dataset

Before adding a new dataset, the provider must:
1. Make the data accessible through HTTP(s)

1. Define the following information:
 - the name of the dataset
 
 - the person who is responsible: name, email

 - a description of the telescope and instrument: simple text, only if not already defined

 - a description of the dataset: can be in HTML with links, emphasis, etc.

	In the dataset description, one can explain for example the format of the data, the processing applied, or how to work with the data; whereas the instrument description is more about the physical description of the instrument. It also means that it is possible to have several datasets, e.g with different processing levels, linked to a single instrument.

 - the list of characteristics of the dataset: for example "full sun", "space based", etc.

 - the list of keywords that will appear in the database: name, type, description, unit

	If the data are FITS files, the [provider tool][provider_tools] `extract_keywords_from_fits` can be used to inspect them and generate a list in JSON format that can be easily altered.

1. Decide if he will push the new metadata, in that case a generic python3 script is available and can be customized as needed. Or if instead the SVO will scan the HTTP archive every day or so, and do the update.

Once the information has been collected, the server admin must follow the following steps:

### Create the telescope, instrument, dataset

In the [admin interface][admin_interface]:
- create if necessary the telescope and the instrument
- create the dataset and add the characteristics

### Create the keywords

There is 2 ways of creating the keywords:

1. Manually using the [admin interface][admin_interface]

1. If the dataset admin has used the script `extract_keywords_from_fits`, use the management command `load_keywords_from_json` to load the JSON file into the database

### Generate the metadata model, resource and admin

1. Use the management command `write_metadata_files`, this will generate files in metadata/models, metadata/admin and metadata/resources

1. Review the files and eventually modify them

1. Import the model in the models/\_\_init__.py file, the resource in the resources/\_\_init__.py and the admin in the admin/\_\_init__.py file

1. Register the resource with the svo_api in metadata/urls.py

1. Create the metadata DB tables (replace DATASETNAME by the name of the model)
	
	```
	./manage.py makemigrations metadata -n add_DATASETNAME
	./manage.py migrate metadata
	```

1. Set the dataset metadata_content_type to the metadata model via the [admin interface][admin_interface] (this should create the dataset user_group automatically)

1. Reload apache for the changes to take effect

### Create the dataset admin user

If necessary, create the user responsible for the dataset via the [admin interface][admin_interface]:

- __give him staff status__
- add him to the dataset user_group and to the "dataset manager" group

## Creating/Updating/Deleting metadata, data locations and tags

The proper way of managing these is using the [RESTful api][restful_api]

Alternatively, a dataset admin can also use the [admin interface][admin_interface], but it can be cumbersome to add metadata that way.

Some of the datasets are managed and populated by the server admin, and for these use the [data provider tools][provider_tools].

## Mounting the data selection file system

The data selection file system is a pseudo file system, that use libfuse to create the directory tree corresponding to the data selections. A FTP server allows users to download the data selections.

To mount the pseudo file system, use the management command `mount_data_selection_filesystem` (TODO be more explicit on the proper args to the command, notably the chosen mountpoint)


[admin_interface]: https://solarnet2.oma.be/service/admin/
[restful_api]: https://solarnet2.oma.be/service/api_doc/
[provider_tools]: https://github.com/bmampaey/SOLARNET-provider-tools
