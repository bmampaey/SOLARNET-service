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

// Display a pop up with an error message or write it to the box if provided.
function alert_user(message, box)
{
	log("alert_user message: ", message);
	if(box == null)
	{
		box = $('<div><span class="ui-icon ui-icon-alert" style="float: left; margin-right: 0.3em;">Alert:</span>' + message + '</div>');
		box.dialog({
			modal: true,
			draggable: false,
			title: "Error",
			resizable: false,
			width: "auto",
			dialogClass: "ui-state-error dialog_box",
			buttons: {
				Ok: function() {
					$( this ).dialog( "close" );
				}
			}
		});
	}
	else
	{
		box.removeClass("ui-state-highlight").addClass("ui-state-error");
		box.html('<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: 0.3em;">Note:</span><strong>' + message + '</strong></p>');
	}
}

// Display a pop up with a informational message or write it to the box if provided
function inform_user(message, box)
{
	log("inform_user message: ", message);
	if(box == null)
	{
		box = $('<div><span class="ui-icon ui-icon-info" style="float: left; margin-right: 0.3em;">Info:</span>' + message + '</div>');
		box.dialog({
			modal: false,
			draggable: false,
			title: "Note",
			resizable: false,
			width: "auto",
			dialogClass: "ui-state-highlight dialog_box",
			buttons: [
				{
					text: "Ok",
					click: function() {
						$( this ).dialog( "close" );
					}
				}
			]
		});
		//box.remove();
	}
	else
	{
		box.removeClass("ui-state-error").addClass("ui-state-highlight");
		box.html('<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: 0.3em;">Note:</span>' + message + '</p>').effect("highlight", {}, 2000);
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
	// Make dataset row openable
	$("tr.open_data_search", section).click(function() {
			log("Clickable was clicked");
			add_accordion_panel('<div class="section search_form_section" href="'+$(this).attr("search_data_form_href")+'">Please wait for the search form to load</div><div class="section search_results_section" href="'+$(this).attr("search_data_results_href")+'">You can search for data using the form on the left</div>', $(this).attr("dataset_name") + '_search_data', 'Search data ' + $(this).attr("dataset_name") + "  <button type='button' class='help small_button' title='" + $(this).attr("dataset_description") + "'>Help</button>", true);
	}).hover(function(){
		$(this).toggleClass('ui-state-hover');
	})
	
	// Transform help text in ? button
	$("span.helptext", section).replaceWith(function() {return "<button type='button' class='help small_button' title='" + $(this).text() + "'>Help</button>";});
	$("button.help").button({icons: {primary: "ui-icon-help"}, text:false}).addClass('ui-state-highlight').click(function(e){
		inform_user($(this).attr("title"));
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
	content_element = $("#"+id);
	if(content_element.length)
	{
		// If the element exists already, we just replace it's content
		log("Element with id", id,"already exists, uppdating content", content_element.html());
		content_element.html(content);
	}
	else
	{
		// Else we append the title and the content to the accordion
		log("Creating new element with id", id, "and title", title)
		title_element = $("<h3>/", {
			id: id+'_title',
		}).append(title);
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
	//Load the loadable_sections with href with the content at the url 
	$('.section[href]').each(function(){
		load_section($(this), $(this).attr( 'href' ));
	});
	// We need to refresh the accordion to adjust the panel sizes
	$("#accordion").accordion("refresh");
	$("#accordion").accordion("option", "active", $("#accordion>div").index(content_element));
	
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
	
	
}


// Attach all the events handler 
$(document).ready(load_events_handlers);
