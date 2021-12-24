# SVO Data Provider Manual


## Intro
The SVO service is a catalog of data and metadata of solar observations grouped into datasets. The grouping is decided by the data providers, but all metadata records in a dataset must have the same fields (or keywords).

The SVO allows dataset providers to create/update/delete metadata, tags and data location in the catalog. And also to choose and modify the information about the dataset and the keywords.

Below is the documentation for the data providers. We assume that you are familiar with the basics of the HTTP protocol and we encourage you to also read the [SVO RESTful API user manual](#TODO put link here).

## User
Data providers must have a special user in the SVO service. For this, the data provider will be registered by the SVO admin using an email and a password, and will receive in return a username (normally the same as the email) and an API key. If they have created a simple user through the Restful API previously, the user can be re-used, but some parameters must be adapted by the SVO admin.

## Administration Interface
Data providers can make use of the administration interface available at https://solarnet.oma.be/service/admin/ to manage their data. For example it is possible for a data provider to modify the URL or the description, of their dataset via this interface.

Some information cannot be changed because the change would require some actions by the SVO admin. For example changing the name of a keyword require to modify the corresponding database table for the metadata records.

Although it is also possible to manage the data location, metadata and associated tags via the administration interface, it is probably more convenient to use the RESTful API.

The use of the administration interface is deemed intuitive enough, and won't be explained. In case of doubt, please contact the SVO admin.

## OID
Each metadata resource instance is identified uniquely by an OID (Observation ID), i.e. 2 instances of the same metadata resource can never have the same OID.

The OID attributed at creation may never change, but all other fields can be updated.

An OID is a string that should preferably contain the date of observation in the format YYYYMMDD_hhmmss. The milliseconds can be added if the second precision is not enough, or eventually the wavelength.

## RESTful API for the data providers
Below we use the terms resource to denote the whole list of objects in a single DB table, and the term resource instance (or instance for short) to denote a single object. For example, the list of *dataset* is a resource, and the *SWAP level 1* dataset is a resource instance of the *dataset* resource.

Data providers can retrieve all resources through the RESTful API like any other [user](#TODO put link here). They can also create, modify or delete resource instances for the *data_location* resource, the metadata resources for which they are responsible, and the *tag* resource.

The URI for the resources are listed at https://solarnet.oma.be/service/api/svo/ (under list_endpoint), and the schema (or resource fields) are available there also.

The URI for a data_location instance, is the data_location resource URI followed by the id of the instance (an integer). For example /service/api/svo/data_location/2818931/

The URI for a metadata instance, is the metadata resource URI followed by the oid of the instance (a string). For example /service/api/svo/metadata_swap_level_1/20091120082529/

The URI for a tag instance, is the tag resource URI followed by the name of the instance (a string). For example /service/api/svo/tag/moon transit/

### Authentication
To modify the catalog, that is to create, modify or delete resource instances, the data provider must use the API authentication scheme.

The username ( usually the email ) and API key must be specified in all the HTTP requests as an **Authorization** header like so:

ApiKey *username*:*api_key*

### Creating a new data_location resource instance
Data provider can only create new data_location instances for a dataset for which they are responsible.

For this, make a POST HTTP request, with a valid *Authorization* header, to the [data_location](https://solarnet.oma.be/service/api/svo/data_location) resource URI, and the following data:
 - dataset : The URI of the dataset instance
 - file_url : A valid URL to the data file
 - file_size : An integer representing the size of file in bytes
 - file_path : The file name, eventually preceded by a relative folder structure (use / as the path separator and avoid the characters \:*?"\'<>|\r\n\0')
 - thumbnail_url : Optional, a valid URL to a thumbnail image of the data (preferably JPEG or PNG) for quick preview
 - offline : Optional, the value `true` or `false` indicating if the file is NOT available for download. If not specified, the default value will be `false`.

The resource instance of the newly created data_location resource instance will be returned as a response, along with the URI of the instance.

## Creating a new metadata resource
Data provider can only create new metadata instances for a dataset for which they are responsible.

For this, make a POST HTTP request, with a valid *Authorization* header, to the metadata resource URI, and the following data:
 - oid : a unique string that identify uniquely the metadata resource instance, see [above](#oid)
 - date_beg : The date of the start of the observation in the ISO 8601 format
 - date_end : The date of the end of the observation in the ISO 8601 format
 - wavemin: Optional, the minimum wavelength observed in nanoseconds
 - wavemax: Optional, the maximum wavelength observed in nanoseconds
 - data_location : The URI (not the URL) of the data_location resource instance
 - fits_header : Optional, the entirety of the FITS header as a single string
 - tags : Optional, a list of tag URI
 - a value for each metadata field, they are all optional, and if not provided will be set to null.

The resource instance of the newly created metadata resource instance will be returned as a response, along with the URI of the instance.

Note that for the data_location, instead of providing a resource URI, it is possible and preferable to provide a full resource instance, and in that case a new data_location resource instance will be created.

### Updating an existing data_location resource instance
Data provider can only update a data_location instance for a dataset for which they are responsible.

For this, make a PATCH HTTP request, with a valid *Authorization* header, to the resource instance URI, and the data for any of the field that you wish to update.

### Updating an existing metadata resource instance
Data provider can only update a metadata instance for a dataset for which they are responsible.

For this, make a PATCH HTTP request, with a valid *Authorization* header, to the resource instance URI, and the data for any of the field that you wish to update.

### Deleting an existing data_location resource instance
Data provider can only deleta a data_location instance for a dataset for which they are responsible.

For this, make a DELETE HTTP request, with a valid *Authorization* header, to the resource instance URI.

### Deleting an existing metadata resource instance
Data provider can only update a metadata instance for a dataset for which they are responsible.

For this, make a DELETE HTTP request, with a valid *Authorization* header, to the resource instance URI.

## Tagging
Metadata records can be tagged with information pertaining to the observation. For example the tag "moon transit" denotes that the moon can be seen in the observation of the sun. Tag names should be very short and not dataset specific. For dataset specific tagging, use a metadata keyword instead.

Tags can be created using the [administration interface](#administration-interface) or the [RESTful API](#TODO put link here). Once created, tags cannot be modified, nor deleted. In case of an error, please contact the SVO admin.

To associate tags to metadata records, you can use the [administration interface](#administration-interface) or the [RESTful API](#TODO put link here). Using the administration interface can be difficult, and it is probably easier to use the RESTful API.

Tags can be added directly at the creation of the metadata record by specifying a list of tag URI in the data of the [POST request](#creating-a-new-metadata-resource).

Tags can be modified after creation of the metadata record, by [updating the metadata resource instance](#updating-an-existing-metadata-resource-instance) and specifing a list of tag URI in the data of the PATCH request. Note that this operation **does not add the tags to the current list but completely replaces it**. This can be used to remove all tags by specifying an empty list.
