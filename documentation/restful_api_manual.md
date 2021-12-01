# RESTful API manual


## Intro
The SVO service is a catalog of metadata of solar observations grouped into datasets.

The metadata is made accessible for reading to anyone though a [RESTful API](https://en.wikipedia.org/wiki/Representational_state_transfer) at the url https://solarnet2.oma.be/service/api/svo

It also allows dataset providers to create/update/delete metadata, tags and data location in the catalog.

The API documentation is accessible at https://solarnet2.oma.be/service/api_doc/

Expalin how to retrieve the API key
the search metadata
the order_by
the limit and offset
can never change an oid
only metadata and data_location for providers, the rest must be modified through the admin interface
all users can create data_selection, but these are dynamic a data selection a selection of data depending on some selection critireia on metadata
what about tags?
