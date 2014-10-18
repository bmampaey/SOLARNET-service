/*
TODO
*/

// Global variables
debug = true;

// Set implementation
var Set = function() {};
Set.prototype.add = function(o) { this[o] = true; };
Set.prototype.remove = function(o) { delete this[o]; };
Set.prototype.values = function() { return Object.keys(this); };

// Logging function, log to console if available, else log to overlay
function log(a, b, c, d, e)
{
	if(debug)
	{
		var bits = [a, b, c, d, e];
		var message = "";
		for (var i = 0; i<bits.length; ++i)
		{
			if(bits[i] !== undefined)
			message += bits[i].toString() + " ";
		}
		if(typeof console === "undefined")
		{		
			$("#debug_console").append('<p style="margin-top:1em;">'+message+'</p>');
		}
		else
		{
			console.log(message);
		}
	}
}


// Things to do at the very beginning
function load_events_handlers()
{
	// Create artificial console log
	if(debug && typeof console === "undefined")
	{
		$(document.body).append('<div id="debug_console" style="width:50em; border: 2px solid red; position: absolute; right: 0; bottom:0;vertical-align: bottom;"></div>');
	}
	
	// Make clickable things clickable
	$(".clickable[href]").click(function() {
			log("Clickable was clicked");
			window.document.location = $(this).attr("href");
	});
	/*
		// Set defaults for all datetime pickers
	$.datepicker.setDefaults(
		{
			buttonImage: CALENDAR_IMAGE_URL,
			buttonImageOnly: true,
			buttonText: "Click to open date picker",
			showOn: "button",
			changeYear: true,
			changeMonth: true,
			dateFormat: 'yy-mm-dd',
		}
	);
	*/
	// Attach datetime picker to date_time_inputs
	
	$("input.date_time_input").datetimepicker(
		{
			buttonImage: CALENDAR_IMAGE_URL,
			buttonImageOnly: true,
			buttonText: "Click to open date picker",
			showOn: "button",
			changeYear: true,
			changeMonth: true,
			dateFormat: 'yy-mm-dd',
			//minDateTime: new Date(2010,02,29), //Find a way to specialize this
			//maxDateTime: new Date(),
			timeFormat: 'HH:mm:ss', 
			hourGrid: 6,
			minuteGrid: 10,
			showSecond: false,
		}
	);
	
	// Transform download_data anchors to button
	$('a.download_data').button({icons: {primary: "ui-icon-arrowthickstop-1-s"}, text:false}).click(function(e){
		// Change the color of the icon so user knows what he already downloaded
		$(this).addClass('ui-button-disabled ui-state-disabled');
	});
}


// Attach all the events handler 
$(document).ready(load_events_handlers);
