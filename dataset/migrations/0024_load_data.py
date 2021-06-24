# Generated by Django 3.2.4 on 2021-06-24 08:19

from django.db import migrations


def convert_keyword_type(apps, schema_editor):
	# We can't import the models directly as it may be a newer
	# version than this migration expects. We use the historical version.
	Keyword = apps.get_model('dataset', 'Keyword')
	for keyword in Keyword.objects.all():
			keyword.type = TYPE_CONVERSION[keyword.type]
			keyword.save()

def load_dataset(apps, schema_editor):
	# We can't import the models directly as it may be a newer
	# version than this migration expects. We use the historical version.
	Keyword = apps.get_model('dataset', 'Keyword')
	DataLocation = apps.get_model('dataset', 'DataLocation')
	Dataset = apps.get_model('dataset', 'Dataset')
	Characteristic = apps.get_model('dataset', 'Characteristic')
	ContentType = apps.get_model('contenttypes', 'ContentType')
	
	for data in DATASET_DATA:
		metadata_content_type = ContentType.objects.get_by_natural_key(*data['fields'].pop('metadata_content_type'))
		caharacteristics = Characteristic.objects.filter(name__in=data['fields'].pop('characteristics'))
		dataset = Dataset.objects.create(**data['fields'], metadata_content_type=metadata_content_type)
		dataset.characteristics.set(caharacteristics)
		DataLocation.objects.filter(dataset_name=data['pk']).update(dataset=dataset)
		Keyword.objects.filter(dataset_name=data['pk']).update(dataset=dataset)


class Migration(migrations.Migration):

	dependencies = [
			('dataset', '0023_add_dataset'),
	]
	
	operations = [
		migrations.RunPython(convert_keyword_type),
		migrations.RunPython(load_dataset),
	]



TYPE_CONVERSION = {
	'str': 'text',
	'bool': 'boolean',
	'int': 'integer',
	'long': 'integer',
	'float': 'real',
	'datetime': 'time (ISO 8601)'
}

DATASET_DATA = [
{
 "model": "dataset.dataset",
 "pk": "aia_lev1",
 "fields": {
	"name": "AIA level 1",
	"description": "Level 1 data corresponding to all ten wavelength channels of the AIA instrument, at a 12-second cadence, and a resolution of 4096 by 4096 pixel at 0.6 arcsec/pixel.",
	"contact_email": "",
	"archive_url": "https://aia.lmsal.com/",
	"telescope_id": "SDO",
	"instrument_id": "AIA",
	
	"metadata_content_type": [
	 "metadata",
	 "aialev1"
	],
	"characteristics": [
	 "space based",
	 "full sun",
	 "E.U.V."
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "chromis",
 "fields": {
	"name": "CHROMIS",
	"description": "Data acquired with the CHROMIS instrument processed with the <a href=\"https://dubshen.astro.su.se/wiki/index.php/SSTRED\" target=\"_blank\">SSTRED</a> data processing pipeline. This pipeline applies various calibrations, restores the images from blurring caused by turbulence in Earth's atmosphere, and packages the data into FITS files with various kinds of metadata.<br>\r\nFor download instructions and data policy, see <a href=\"https://dubshen.astro.su.se/wiki/index.php/Science_data\" target=\"_blank\">https://dubshen.astro.su.se/wiki/index.php/Science_data</a>.",
	"contact_email": "mats@astro.su.se",
	"archive_url": "https://www.isf.astro.su.se/",
	"telescope_id": "SST",
	"instrument_id": "CHROMIS",
	
	"metadata_content_type": [
	 "metadata",
	 "chromis"
	],
	"characteristics": [
	 "spectograph",
	 "ground based"
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "chrotel",
 "fields": {
	"name": "ChroTel",
	"description": "",
	"contact_email": "",
	"archive_url": "http://sdac.virtualsolar.org/cgi/show_details?source=ChroTel",
	"telescope_id": "ChroTel",
	"instrument_id": "ChroTel",
	
	"metadata_content_type": [
	 "metadata",
	 "chrotel"
	],
	"characteristics": [
	 "ground based",
	 "full sun",
	 "E.U.V."
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "crisp",
 "fields": {
	"name": "CRISP",
	"description": "Data acquired with the CRISP instrument processed with the <a href=\"https://dubshen.astro.su.se/wiki/index.php/SSTRED\" target=\"_blank\">SSTRED</a> data processing pipeline. This pipeline applies various calibrations, restores the images from blurring caused by turbulence in Earth's atmosphere, and packages the data into FITS files with various kinds of metadata.<br>\r\nFor download instructions and data policy, see <a href=\"https://dubshen.astro.su.se/wiki/index.php/Science_data\" target=\"_blank\">https://dubshen.astro.su.se/wiki/index.php/Science_data</a>.",
	"contact_email": "mats@astro.su.se",
	"archive_url": "https://www.isf.astro.su.se/",
	"telescope_id": "SST",
	"instrument_id": "CRISP",
	
	"metadata_content_type": [
	 "metadata",
	 "crisp"
	],
	"characteristics": [
	 "spectograph",
	 "ground based",
	 "spectropolarimetric data"
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "eit",
 "fields": {
	"name": "EIT level 0",
	"description": "The dataset consist of full sun images of the solar corona in the extreme ultraviolet range in 4 wavelengths: 17.1, 19.5, 28.4, and 30.4 nm",
	"contact_email": "",
	"archive_url": "https://umbra.nascom.nasa.gov/eit/",
	"telescope_id": "SOHO",
	"instrument_id": "EIT",
	
	"metadata_content_type": [
	 "metadata",
	 "eit"
	],
	"characteristics": [
	 "space based",
	 "E.U.V."
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "gris_lev1",
 "fields": {
	"name": "GRIS level 1",
	"description": "The following links provide additional information on: The <a href=\"http://archive.leibniz-kis.de/pub/gris/readme/archive_manual.pdf\">GRIS archive</a>, the <a href=\"http://archive.leibniz-kis.de/pub/gris/readme/level2_parameters.pdf\">1.5 &#956;m level2 data</a>, the <a href=\"http://adsabs.harvard.edu/abs/2012AN....333..796S\">GREGOR</a> telescope, the <a href=\"http://adsabs.harvard.edu/abs/2012AN....333..796S\">Adaptive Optics</a> system and the <a href=\"http://adsabs.harvard.edu/abs/2012AN....333..872C\">GRIS</a> instrument.\r\n<br>\r\nFor information on the spatial and spectral quality of the GRIS data, see the following papers <a href=\"http://adsabs.harvard.edu/abs/2016A%26A...596A...2B\">Borrero et al. (2016)</a> and <a href=\"http://adsabs.harvard.edu/abs/2016A%26A...596A...4F\">Franz et al. (2016)</a>.\r\nFor visualization and standard calibration of GRIS level1 data you may download an <a href=\"http://archive.leibniz-kis.de/pub/gris/readme/gui.tar\">IDL-GUI</a> which requires sswidl or runs as a virtual machine without a licence in IDL8.5 and higher. The installation procedure is described in the <a href=\"http://archive.leibniz-kis.de/pub/gris/readme/gui_manual.pdf\"> manual</a>.\r\n<br>\r\nIf you make use of this archive please acknowledge the GRIS & GREGOR projects by citing the abovementioned <a href=\"http://archive.leibniz-kis.de/pub/gris/readme/GREGOR_GRIS.bib\">publications</a> and add this <a href=\"http://archive.leibniz-kis.de/pub/gris/readme/GREGOR_GRIS.tex\">paragraph</a> to the end of your manuscript.\r\n<br>",
	"contact_email": "morten@leibniz-kis.de",
	"archive_url": "http://archive.leibniz-kis.de/pub/gris/",
	"telescope_id": "GREGOR",
	"instrument_id": "GRIS",
	
	"metadata_content_type": [
	 "metadata",
	 "grislev1"
	],
	"characteristics": [
	 "spectograph",
	 "ground based"
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "hmi_magnetogram",
 "fields": {
	"name": "HMI magnetogram",
	"description": "4096 by 4096 pixels full sun magnetograms at a cadence of 45 seconds from the HMI instrument.",
	"contact_email": "",
	"archive_url": "http://hmi.stanford.edu/",
	"telescope_id": "SDO",
	"instrument_id": "HMI",
	
	"metadata_content_type": [
	 "metadata",
	 "hmimagnetogram"
	],
	"characteristics": [
	 "space based",
	 "full sun"
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "ibis",
 "fields": {
	"name": "IBIS",
	"description": "Raw spectropolarimetric observations of the partial Sun at various spectral regions; FoV approx 40 x 90 arcsec ^2, cadence of 67 s, pixel scale approx 0.09 arcsec.",
	"contact_email": "ilaria.ermolli@oa-roma.inaf.it",
	"archive_url": "http://ibis.oa-roma.inaf.it/IBISA",
	"telescope_id": "DST",
	"instrument_id": "IBIS",
	
	"metadata_content_type": [
	 "metadata",
	 "ibis"
	],
	"characteristics": [
	 "ground based",
	 "spectropolarimetric data",
	 "partial sun"
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "rosa",
 "fields": {
	"name": "ROSA",
	"description": "This data was taken as part of the special DST service mode run ran entirely for flare studies in October 2014. The raw data is publicly available on the NSO website (http://nsosp.nso.edu/dst/smex). The data was reduced using the older version of the ROSA pipeline (v1.0) which is not 100% SolarNet compliant. The data was dark and flat corrected prior to Speckle reconstruction using the KISIP code. After speckle, images were aligned and destretched before the data was science ready. There were 2 pointings that day of the same AR. Pointing was shifted so as to capture a possible flare better. There are flares in both data sets. The quality of the first data set is better than the second, as the seeing was better earlier in the morning.",
	"contact_email": "p.keys@qub.ac.uk",
	"archive_url": "https://star.pst.qub.ac.uk/wiki/doku.php/public/research_areas/solar_physics/rosa_reconstructed_archive",
	"telescope_id": "DST",
	"instrument_id": "ROSA",
	
	"metadata_content_type": [
	 "metadata",
	 "rosa"
	],
	"characteristics": [
	 "ground based"
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "swap_lev1",
 "fields": {
	"name": "SWAP level 1",
	"description": "Level 1 images from the SWAP instrument.",
	"contact_email": "",
	"archive_url": "http://proba2.sidc.be/data/SWAP",
	"telescope_id": "PROBA2",
	"instrument_id": "SWAP",
	
	"metadata_content_type": [
	 "metadata",
	 "swaplev1"
	],
	"characteristics": [
	 "space based",
	 "full sun",
	 "E.U.V."
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "themis",
 "fields": {
	"name": "Themis",
	"description": "Themis",
	"contact_email": "",
	"archive_url": "http://bass2000.bagn.obs-mip.fr/Tarbes/",
	"telescope_id": "Themis",
	"instrument_id": "Themis",
	
	"metadata_content_type": [
	 "metadata",
	 "themis"
	],
	"characteristics": [
	 "test",
	 "ground based"
	]
 }
},
{
 "model": "dataset.dataset",
 "pk": "xrt",
 "fields": {
	"name": "XRT",
	"description": "",
	"contact_email": "",
	"archive_url": "http://sdac.virtualsolar.org/cgi/show_details?instrument=XRT",
	"telescope_id": "Hinode",
	"instrument_id": "XRT",
	
	"metadata_content_type": [
	 "metadata",
	 "xrt"
	],
	"characteristics": [
	 "space based",
	 "full sun"
	]
 }
}
]
