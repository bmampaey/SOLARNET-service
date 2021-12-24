# SVO RESTful API User Manual

## Intro
The SVO service is a catalog of data and metadata of solar observations grouped into datasets. The grouping is somewhat arbitrary and intuitive, but all metadata records in one dataset must have the same fields (or keywords).

The catalog is made accessible for reading to any user though a [RESTful API](https://en.wikipedia.org/wiki/Representational_state_transfer) at the url https://solarnet.oma.be/service/api/svo.

The API also allows dataset providers to create/update/delete metadata, tags and data location in the catalog.

The technical documentation on the API [HTTP request methods](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods) and [query string parameters](https://en.wikipedia.org/wiki/Query_string) is accessible at https://solarnet.oma.be/service/api_doc/

Below is a more human friendly documentation for the API users. We assume that you are familiar with the basics of the HTTP protocol.

## Accessing the catalog information
The catalog is stored in a database. A database table made accessible through the API is called a resource. A single object (or row) in a database table is also called a resource, but to distinguish it from the previous, we call it a resource instance. Both resources and resource instances are identified by an [URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier) that is immutable.

The URI for the resources are listed at https://solarnet.oma.be/service/api/svo/ (under list_endpoint), and the schema (or resource fields) are available there also.

All of the resources and resource instances can be accessed through the GET HTTP Request method on the URL corresponding to the URI, i.e. by specifying the server name. For example the dataset resource has the URI */service/api/svo/dataset*, soa GET request on https://solarnet.oma.be/service/api/svo/dataset will retrieve the list of datasets. It is also possible to retrieve a single resource instance directly using the resource instance URI, for example to retrieve only the CRISP dataset you can make a GET request on https://solarnet.oma.be/service/api/svo/dataset/CRISP/

Most resources are accessible without authentication, but if you need it or prefer to use it see the chapter [Registration and Authentication](#registration-and-authentication) below.

## Available resources
Here is a short presentation of the resources representing the catalog information:

- [dataset](https://solarnet.oma.be/service/api/svo/dataset) : with information about the dataset, such as the name, the description, the URL of the official archive, and the URI of the corresponding metadata resource. Also to each dataset resource are associated an instrument, a telescope and a list of characteristics (see below).
- [instrument](https://solarnet.oma.be/service/api/svo/instrument) : with the information about a instrument used to make the solar observations.
- [telescope](https://solarnet.oma.be/service/api/svo/telescope) : with the information about a telescope or a satellite on which the instrument is mounted.
- [characteristic](https://solarnet.oma.be/service/api/svo/characteristic) : a simple information about a dataset, for example "space based" or "earth based", "full sun" or "partial sun", etc.
- [data_location](https://solarnet.oma.be/service/api/svo/data_location) : with the information about the data files inside a dataset, such as the URL to the file, the size of the file, a file path to eventually organize the files into a directory structure, an optional URL to a thumbnail of the data, the time of last update of the file, and a boolean to tell if the file is offline, that is inaccessible via the URL.
- [keyword](https://solarnet.oma.be/service/api/svo/keyword) : with the information about the metadata fields off a specific dataset, such as the name of the field, a verbose name (often the FITS keyword), the type of the field (i.e. how to interpret the value of the field), an optional unit and a description.
- several metadata resources : to each dataset correspond a single metadata resource, for example to the *CRISP* dataset correspond the resource [metadata_crisp](https://solarnet.oma.be/service/api/svo/metadata_crisp); the information associated to a metadata resource is defined by the keyword resource associated to the dataset.
- [tag](https://solarnet.oma.be/service/api/svo/tag) : a simple information associated to a solar observation, for example "moon transit", "test", etc. To each metadata instance can be associated 0 or more tags.

Note that characteristics and tags are added by the data providers as hints and are not strict or exhaustive.

## Filtering
Resource URI accept also query string with filter parameters to select only some of the resource instance in the list. This is particularly useful with data_location and metadata resources. For example, to retrieve metadata from the XRT dataset that has a target = AR, it is possible to make a GET request on https://solarnet.oma.be/service/api/svo/metadata_xrt/?target=AR.

The acceptable filters for each resource are listed in the [technical documentation](https://solarnet.oma.be/service/api_doc/). It is possible to combine several filters together, in that case they will **all** be respected (logical AND). For example to retrieve metadata from the XRT dataset that has a target = AR, AND an observation time after January 1st 2015, it is possible to make a GET request on https://solarnet.oma.be/service/api/svo/metadata_xrt/?target=AR&date_obs__gte=2015-01-01

Usually filters can be applied on any resource field by specifying the field name, eventually followed by 2 underscores and a suffix:
 - numeric comparison : **__gt** the field value must be greater than the parameter value, **__gte** greater than or equal, **__lt** lower than, **__lte** lower than or equal
 - textual comparison : **__contains** the field value must contain the parameter value, **__icontains** case insensitive contain, **__startswith** start with, **__istartswith** case insensitive start with, **__endswith** end with, **__iendswith** case insensitive end with
 - regular expression comparison, **__regex** the field value must match the regular expression of the parameter value, **__iregex** case insensitive regex
 - value selection : **__in** the field value must be equal to one of the parameter values, repeat several time for several values, for example https://solarnet.oma.be/service/api/svo/metadata_xrt/?target__in=AR&target__in=CH will select XRT metadata instance that has a target in the list [AR, CH].
 - null value : **__isnull** followed by the value true or false
 - equality : **__exact** the field value must be equal to the parameter value, same as not specifying any suffix, e.g. ?target=AR or ?target__exact=AR are the same.

Metadata resources accept also the **search** parameter filter. This parameter can contain a string with a complex logical query containing any of the filters described above articulated with the logical operators "AND", "OR", "NOT", and parentheses. For example to retrieve XRT metadata that has a target = AR after January 1st 2015 or a target = CH, it is possible to make a GET request on [https://solarnet.oma.be/service/api/svo/metadata_xrt/?search=( ( target=AR  AND date_obs__gte=2015-01-01) OR target=CH )](https://solarnet.oma.be/service/api/svo/metadata_xrt/?search=((target=AR%20AND%20date_obs__gte=2015-01-01)%20OR%20target=CH))

Additionaly, metadata resources accept a **tag** parameter filter that allows to search metadata that has a specific tag. For example to request all SWAP level 1 metadata that observed a moon eclipse, it is possible to make a GET request on [https://solarnet.oma.be/service/api/svo/metadata_swap_level_1/?tag=moon transit](https://solarnet.oma.be/service/api/svo/metadata_swap_level_1/?tag=moon%20transit)

Some resource instances have relations to resource instances of another type, and it is possible to filter using these relations by specifying the resource name followed by 2 underscores and followed by a filter as described above. For example, data_location instances have a relation to a dataset instance, so to retrieve data locations corresponding to the XRT dataset, it is possible to make a GET request on https://solarnet.oma.be/service/api/svo/data_location/?dataset__name=XRT.

## Ordering
Resource URI accept also a query string with an *order_by* parameter specifying the order of the list. For example to retrieve metadata from the XRT dataset, ordered by date of observation, it is possible to make a GET request on https://solarnet.oma.be/service/api/svo/metadata_xrt/?order_by=date_obs.

## Offset and limit
Because the data_location and metadata resources can contain millions of instance, a GET on the resource URI will retrieve by default only the first 20 instances. The resource URI accept also a query string with an *offset* parameter that allows to retrieve instances further in the list, and by doing several GET requests, to retrieve as many instances as necessary. For example to retrieve the following 20 instances of the example above, it is possible to make a GET request on https://solarnet.oma.be/service/api/svo/metadata_xrt/?order_by=target&offset=20

Resource URI accept also a query string with a *limit* parameter specifying the maximum number of instances to retrieve. For example to retrieve only 5 dataset instances, it is possible to make a GET request on https://solarnet.oma.be/service/api/svo/dataset/?limit=5

Note that for the data_location resource the absolute limit is 1000 and for metadata resources it is 100.

## Time values
All time values in the catalog are expressed using the ISO 8601, with a millisecond precision in the UTC timezone, i.e. YYYY-MM-DDThh:mm:ss.sssZ

## Request/Response format
The API understands requests and can respond in the following formats and mime types
 - json : application/json
 - xml : application/xml
 - yaml : text/yaml
 - plist : application/x-plist

The default format is JSON. To request data in a specific format, you must set the **Accept** header in your HTTP request to the appropriate mime type.

Alternately, you can specify the format as a query string parameter, for example to request the list of dataset in xml you you can make a GET request on https://solarnet.oma.be/service/api/svo/dataset/?format=xml

Similarly, if you need to send data with a POST or PATCH HTTP request, you can send it using one of the above format by setting the **Content-Type** header with the corresponding mime type.

## Registration and Authentication
To use authentication, a user account in the API is necessary. The [user resource](https://solarnet.oma.be/service/api/svo/user) can be used to create a new user account. For this, one must make a POST HTTP request to the user URI submitting the data "email", "password", "first_name" and "last_name". In response, you will receive an API key.

To retrieve the user data and API key, it is possible to make a GET request on the user URI by using the [Basic authentication scheme](https://en.wikipedia.org/wiki/Basic_access_authentication) specifying the email as username, and the password submitted during registration.

To change any of the user password, first name or last name, it is possible to make a PATCH request on the user URI, using the Basic authentication scheme ( using the old password ), and submitting the data "password" ( the new password ), "first_name" or "last_name".

To delete the user account **and all associated user data** in the API, it is possible to make a DELETE request on the user resource using the Basic authentication scheme.

To use authentication for all other resources, all HTTP requests to the API must contain an **Authorization** header with the username ( same as the email ) and the API key like so:

ApiKey *username*:*api_key*

## Saving data selection
In addition to the resources listed above, there is also a [data_selection resource](https://solarnet.oma.be/service/api/svo/data_selection). This allows users to save a metadata resource search (see [filtering](#filtering)), and therefore retrieve the associated data.

Note that these data selection are dynamic, i.e. if the catalog of metadata changes, the metadata resource search will yield different results. For example, saving the XRT metadata search https://solarnet.oma.be/service/api/svo/metadata_xrt/?target=AR (with a target = AR) may yield additional resource instance if new XRT data is added to the catalog.

To be able to save data selections, consult the saved data selections, or delete them, a user must use the authentication scheme described above. If you wish to develop API client that use the data_selection resource, please contact the SVO administrators for more ample instructions.
