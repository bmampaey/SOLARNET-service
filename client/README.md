SOLARNET API client
===================

Common usage
------------
```python
from SOLARNET import datasets

# See all available datasets
for dataset in datasets:
	print dataset

# Get a specific dataset
aia_lev1 = datasets.get("aia_lev1")

# Filter the record in that dataset for February 2012 with a wavelength of 171A
filtered_aia_lev1 = aia_lev1.filter("DATE-OBS", "2012 Feb", WAVELNTH = 171)

# Display the date of observation and the wavelength in that filtered dataset
for record in filtered_aia_lev1:
	print record.meta_data["DATE-OBS"], record.meta_data["WAVELNTH"]

# Download the data from a record
record.download("/tmp")
```
