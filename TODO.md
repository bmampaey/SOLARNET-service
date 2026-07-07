# TODO

## Constants keywords

Some dataset have keywords that always have the same value, for exemple INSTRUMENT. To gain Database space and performance, these can be removed from the metadata table, but added to the API resources

This is being implemented in branch constant_value

- [x] Add to keywords a constant_value
- [ ] Modify the management command write_metadata_files to add it to metadata files

  - [x] in model file: add constant keyword as a class constant instead of model field
  - [x] in resource file: add constant keywords as readonly field without attribute, remove them from filtering, and check they dont appear in the schema filter
  - [ ] in admin files: add them as readonly fields ?

- [x] Add management command inspect_constant_fields, to find which keywords are good candidates to be defined as constant

- [ ] Add unitest, including the beavior when providers still try to push values for these constant keywords (have a nice error message)

## Finish processing XRT level 1

Process from year **2011.bis** to **2026**, in **order** :

- On yama, check that each year has finished first, then reprocess it with re_extract_xrt.sh to redownload errored files
- On solarnet : use management command load_metadata_from_jsonl to load the json files

## Improve performance of date filtering

Currently if a user want to search between 2 dates date_min and date_max, such that date_min < date_max, PostgreSQL is performing very poorly.

```sql
select * from metadata_aia_level_1_5 where date_min < date_end and date_start < date_max;
```

If we ANALYZE such a query, we see that PostgreSQL considers both comparison as distinct, and thinks that there will be twice as many rows as there should be :
(row count for date_min < date_end) + (row count for date_start < date_max)

One solution to envisage is to use a GIST index on the date range

```sql
CREATE INDEX mytable_date_range_idx
ON mytable
USING gist (daterange(date_start, date_end, '[]'));
```

And in Django or Tastypie, intercept this type of request and replace it with

```sql
SELECT * FROM mytable
WHERE daterange(date_start, date_end, '[]') && daterange(date_min, date_max, '[]');
```

## Decrease size of dataset EUVI level 0

EUVI level 0 is too large, we can remove the fits_header, BUT FIRST:

- extract the COMMENT, and the HISTORY keywords (check if need to be split by consecutive block)
- extract the keyword comments (after the /) if they are not constant for a specific keyword, i.e. they provide a human readable value eg. DOOR = 0 /closed or DOOR = 1 / open, then we can a keyword door_status

## Define constant keywords for large datasets

By using keywords with constant values, we can optimize the database storage space of large datasets :

- AIA level 1.5
- EUVI level 0 (but do the removing of fits_header first)
- Proba 2 datasets
- Any inhouse dataset

## Add datasets PROBA3/ASPIICS

From mails consider datasets L1, L2 and L3 (each time v2)

See <https://www.sidc.be/proba-3/aspiics-data>

## Create a TAP Tastypie resource

By inheriting directly from Resource and not ModelResource, create a TapResource that can populate the data from a TAP service instead of the database

## Add TAP datasets

[currents](https://idoc-dachs.ias.u-psud.fr/__system__/dc_tables/show/tableinfo/currents_epn.epn_core): cartes des courants électriques dans les régions actives.

[synopticmaps](https://idoc-dachs.ias.u-psud.fr/__system__/dc_tables/show/tableinfo/synopticmaps.epn_core): SDO/AIA and SDO/HMI synchronic synoptic maps (these might be split in 2 if you like)
