# TODO

## Improve performance of date filtering

Currently if a user want to search between 2 dates date_min and date_max, such that date_min < date_max, PostgreSQL is performing very poorly.

```sql
select * from metadata_aia_level_1_5 where date_min < date_end and date_beg < date_max;
```

If we ANALYZE such a query, we see that PostgreSQL considers both comparison as distinct, and thinks that there will be twice as many rows as there should be :
(row count for date_min < date_end) + (row count for date_beg < date_max)

One solution to envisage is to use a GIST index on the date range

```sql
CREATE INDEX mytable_date_range_idx
ON mytable
USING gist (daterange(date_beg, date_end, '[]'));
```

And in Django or Tastypie, intercept this type of request and replace it with

```sql
SELECT * FROM mytable
WHERE daterange(date_beg, date_end, '[]') && daterange(date_min, date_max, '[]');
```

An other solution is to be explicit, define a computed column called date_range as the range [date_beg, date_end]

```sql
date_range daterange GENERATED ALWAYS AS (
        daterange(date_beg, date_end, '[]')
    ) STORED
```

And add it to the read only fields of Tastypie and Admin, and add specific filters in tastypie `?date_range_min=2026-07-01&date_range_max=2026-07-15`
Allowing for specifying only one of the two.

## Decrease size of dataset EUVI level 0

EUVI level 0 is too large, we can remove the fits_header, BUT FIRST:

- extract the COMMENT, and the HISTORY keywords (check if need to be split by consecutive block)
- extract the keyword comments (after the /) if they are not constant for a specific keyword, i.e. they provide a human readable value eg. DOOR = 0 /closed or DOOR = 1 / open, then we can a keyword door_status

## Create a TAP Tastypie resource

By inheriting directly from Resource and not ModelResource, create a TapResource that can populate the data from a TAP service instead of the database

## Add TAP datasets

[currents](https://idoc-dachs.ias.u-psud.fr/__system__/dc_tables/show/tableinfo/currents_epn.epn_core): cartes des courants électriques dans les régions actives.

[synopticmaps](https://idoc-dachs.ias.u-psud.fr/__system__/dc_tables/show/tableinfo/synopticmaps.epn_core): SDO/AIA and SDO/HMI synchronic synoptic maps (these might be split in 2 if you like)
