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

function load_section(section, url, indicator)
{
	log("GET request for url", url);
	// Make the request
	var request = $.get(url);
	
	// Change the indicator to running
	if (indicator !== undefined)
	{
		indicator.removeClass('ui-icon-check ui-icon-alert').addClass('ui-icon-loading').attr("title", "Section is being updated");
	}
	
	// Success
	request.done(function(response){
		log("GET request SUCCEEDED for url: ", url);
		// Update the div content
		section.html(response);
		// Change the indicator to success
		if (indicator !== undefined)
		{
			indicator.removeClass('ui-icon-loading ui-icon-alert').addClass('ui-icon-check').attr("title", "Section has been updated");
		}
		post_load_section(section)
	});
	
	// Failure or abort
	request.fail(function(request, status){
		log("GET request FAILED for url: ", url);
		alert_user(request.responseText);
		// Change the indicator to failure 
		if (indicator !== undefined)
		{	
			indicator.removeClass('ui-icon-loading ui-icon-check').addClass('ui-icon-alert').attr("title", "Section failed updating: " + request.responseText);
		}
	});
}

function post_load_section(section)
{
	// Make clickable things clickable
	$(".clickable[href]", section).click(function() {
			log("Clickable was clicked");
			window.document.location = $(this).attr("href");
	});

	// Attach datetimepicker picker to date_time_inputs
	$("input.date_time_input", section).datetimepicker(
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
	
	// Attach multipleSelect widget to multiple select
	$('select[multiple]', section).multipleSelect(
		{
			filter: true,
			selectAllDelimiter: ['',''],
			width: '10em'
		}
	);
	
	// Transform download_data anchors to button
	$('a.download_data', section).button({icons: {primary: 'ui-icon-arrowthickstop-1-s'}, text:false}).click(function(e){
		// Change the color of the icon so user knows what he already downloaded
		$(this).addClass('ui-button-disabled ui-state-disabled');
	});
	
	// Set some JQuery classes to make sections pretty
	section.addClass("ui-widget ui-widget-content ui-corner-all");

}


function add_accordion_panel(content, id, title, closeable)
{
	log("Adding accordion panel with id", id)
	// Check if an element with that id exists already
	existing_element = $("#"+id);
	if(existing_element.length)
	{
		// If the element exists already, we just replace it's content
		log("Element with id", id,"already exists, uppdating content", existing_element.html());
		existing_element.html(content);
	}
	else
	{
		// Else we append the title and the content to the accordion
		log("Creating new element with id", id, "and title", title)
		title_element = $("<h3>/", {
			id: id+'_title',
			text: title
		});
		content_element = $("<div/>", {
			id: id,
		}).append(content);
		if(closeable)
		{
			// Add a close button to the title
			$("<span/>", {
				text: "Close",
				'class': 'small_button',
				style: 'float: right;',
				click: function() {
					title_element.remove();
					content_element.remove();
				}
			}).button({
				icons: {
					primary: "ui-icon-closethick"
				},
				text: false,
			}).appendTo(title_element);
		}
		$("#accordion").append(title_element, content_element);
	}
	// We need to refresh the accordion to adjust the panel sizes
	$("#accordion").accordion("refresh");
	$("#accordion").accordion("option", "active", "#"+id+'_title');
	
}

// Things to do at the very beginning
function load_events_handlers()
{
	// Create artificial console log
	if(debug && typeof console === "undefined")
	{
		$(document.body).append('<div id="debug_console" style="width:50em; border: 2px solid red; position: absolute; right: 0; bottom:0;vertical-align: bottom;"></div>');
	}
	
	//Load the loadable_sections with href with the content at the url 
	$('.section[href]').each(function(){
		load_section($(this), $(this).attr( 'href' ));
	});
	
	// Make the accordion
	$("#accordion").accordion({ heightStyle: "content" });
	
	add_accordion_panel('<div class="section search_form_section" href="">Eit search form</div><div class="section search_results_section" href="">Eit search results</div>', 'eit_search_data', 'Search eit dataset', true);
	
}


// Attach all the events handler 
$(document).ready(load_events_handlers);
