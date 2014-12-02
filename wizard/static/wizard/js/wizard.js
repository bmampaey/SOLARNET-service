/*
TODO
*/

// Global variables
debug = true;
selections = {};

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

// Select all checkboxes in a table and update the selection
function select_all(table)
{
	log("select_all");
	var selection = selections[table.attr("dataset_name")];
	$("input:checkbox", table).each(function(){$(this).prop('checked', true);});
	selection.all_selected = true;
	selection.data_ids = new Set();
}

// De-select all checkboxes in a table and update the selection
function unselect_all(table)
{
	log("unselect_all");
	var selection = selections[table.attr("dataset_name")];
	$("input:checkbox", table).each(function(){$(this).prop('checked', false);});
	selection.all_selected = false;
	selection.data_ids = new Set();
}

// Update selection from selected checkboxes in a table
function update_selection_from_table(table)
{
	var selection = selections[table.attr("dataset_name")];
	
	if(selection.all_selected)
	{
		$("input:checkbox:not(:checked)", table).each(function(){selection.data_ids.add(this.value);});
	}
	else
	{
		$("input:checkbox:checked", table).each(function(){selection.data_ids.add(this.value);});
	}
}

// Select checkboxes in a table from the selection
function update_table_from_selection(table)
{
	var selection = selections[table.attr("dataset_name")];
	if (selection)
	{
		if(selection.all_selected)
		{
			$("input:checkbox", table).prop("checked", true).each(function(){
				if(this.value in selection.data_ids)
				{
					$(this).prop("checked", false);
				}
			});
		}
		else // Do the opposite
		{
			$("input:checkbox", table).prop("checked", false).each(function(){
				if(this.value in selection.data_ids)
				{
					$(this).prop("checked", true);
				}
			});
		}
	}
}

function load_section(section, url, post_load_section, indicator)
{
	log("load_section", section.attr("id"), "with url", url);
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
		if (post_load_section !== undefined)
		{
			post_load_section(section);
		}
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


// Make forms pretty
function post_load_search_section(section)
{
	log("post_load_search_section: ", section.attr("id"));
	
	// Transform search button
	$('button.search', section).button({
			icons: {
				primary: "ui-icon-search"
			},
			text: true,
	});
	
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
	
	// Set some JQuery classes to make sections pretty
	section.addClass("ui-widget ui-widget-content ui-corner-all");

}


function post_load_search_dataset_form_section(section)
{
	post_load_search_section(section);
	
	log("post_load_search_dataset_form_section: ", section.attr("id"));
	
	// Transform the search form to do ajax request instead
	$("form", section).submit(function(e){
		e.preventDefault();
		var form = $(e.target);
		
		// Make the search and load the table
		load_section($("div.search_dataset_results_section", form.closest("div.panel")), form.attr("action") + "?" + form.serialize(), post_load_search_dataset_result_section);
	});
}

// Set-up the section after the load
function post_load_search_dataset_result_section(section)
{
	log("post_load_search_dataset_result_section: ", section.attr("id"));
	
	// Make dataset row openable
	$("tr.open_data_search", section).hover(function(){
		$(this).toggleClass('ui-state-hover');
	}).each(function(){
		var row =$(this);
		$("td:not(:has(input))", row).click(function() {
			log("Row for dataset",row.attr("dataset_name"), "was clicked");
			add_search_data_panel(row.attr("dataset_name"), row.attr("search_data_form_href"), row.attr("search_data_results_href"), row.attr("dataset_description"));
		});
	});
	
	// Set some JQuery classes to make sections pretty
	section.addClass("ui-widget ui-widget-content ui-corner-all");
}

function post_load_search_data_form_section(section)
{
	post_load_search_section(section);
	
	log("post_load_search_data_form_section: ", section.attr("id"));
	
	// Transform the search form to do ajax request instead
	$("form", section).submit(function(e){
		e.preventDefault();
		var form = $(e.target);
		
		// Reset the selection
		selections[form.attr("dataset_name")] = {
			all_selected: false,
			data_ids: new Set(),
		};
		
		// Make the search and load the table
		load_section($("div.search_data_results_section", form.closest("div.panel")), form.attr("action") + "?" + form.serialize(), post_load_search_data_result_section);
	});
	
	// Set up the selection
	selections[$("form", section).attr("dataset_name")] = {
		all_selected: false,
		data_ids: new Set(),
	};
	
	// Set some JQuery classes to make sections pretty
	section.addClass("ui-widget ui-widget-content ui-corner-all");
}



// Set-up the section after the load
function post_load_search_data_result_section(section)
{
	log("post_load_search_data_result_section: ", section.attr("id"));
	
	// Transform download_data anchors to button
	$('a.download_data', section).button({icons: {primary: 'ui-icon-arrowthickstop-1-s'}, text:false}).click(function(e){
		// Change the color of the icon so user knows what he already downloaded
		$(this).addClass('ui-button-disabled ui-state-disabled');
	});
	
	// Transform navigation anchors to buttons
	$('a.first_page', section).button({icons: {primary: "ui-icon-seek-first"}, text:false});
	$('a.previous_page', section).button({icons: {primary: "ui-icon-seek-prev"}, text:false});
	$('a.next_page', section).button({icons: {primary: "ui-icon-seek-next"}, text:false});
	$('a.last_page', section).button({icons: {primary: "ui-icon-seek-end"}, text:false});
	
	// Attach navigation buttons click handler
	$('div.page_navigation a', section).each(function(){
		if($(this).attr("href")) 
		{
			$(this).click(function(e){
				e.preventDefault();
				// We update the selection
				update_selection_from_table($('table.search_results_table', section));
				
				// We get the new search result table
				load_section(section, $(this).attr("href"), post_load_search_data_result_section)
			});
		}
		else
		{
			$(this).addClass('ui-button-disabled ui-state-disabled');
		}
	});
	
	// Attach select_all unselect_all buttons click handler
	$('button.select_all', section).button({icons: {primary: "ui-icon-check"}, text:true}).click(function(e){
		select_all($('table.search_results_table', section));
	});
	$('button.unselect_all', section).button({icons: {primary: "ui-icon-close"}, text:true}).click(function(e){
		unselect_all($('table.search_results_table', section));
	});
	
	// Mark as checked the checkboxes from previous selection
	update_table_from_selection($("table.search_results_table", section));
	
	// Transform add button to do ajax request
	$('input.add_to_selection', section).button({
			icons: {
				primary: "ui-icon-cart"
			},
			text: true,
	}).click(function(e){
		e.preventDefault();
		var button = $(e.target);
		
		// update and get the selection
		update_selection_from_table($("table.search_results_table", section));
		var selection = selections[$("input[name='dataset_name']", form).val()];
		
		log("submit action: ", button.attr("action"), "query: ", selection);
		
		$.get(button.attr("href"), selection)
		.done(function(response){
			log("GET form succeeded: ", response);
			// Create a dialog with the form
			var box = $('<div><span class="ui-icon ui-icon-info" style="float: left; margin-right: 0.3em;">Info:</span>' + response + '</div>');
			box.dialog({
				modal: false,
				draggable: false,
				title: "Note",
				resizable: false,
				width: "auto",
				dialogClass: "ui-state-highlight dialog_box",
			});
			$("form.data_selection_create", box).submit(function(e){
				e.preventDefault();
				var form = $(e.target);
				log("submit form action: ", form.attr("action"), "query: ", form.serialize());
			
				$.post(form.attr("action"), form.serialize())
				.done(function(response){
					log("POST succeded, response: ", response);
						//Load the user section with href with the content at the url 
						$('#user_panel > .section[href]').each(function(){
							load_section($(this), $(this).attr('href'), post_load_user_section);
						});
						$("#accordion").accordion("option", "active", $("#accordion>div").index($('#user_panel')));
				})
				.fail(function(request, status){
					log("POST FAILED, response: ", request.responseText);
					alert_user(request.responseText);
				});
				box.dialog("close");
			});
		})
		.fail(function(request, status){
			log("GET form failed: ", request.responseText);
			alert_user(request.responseText);
		});
	});
	
	// Set some JQuery classes to make sections pretty
	section.addClass("ui-widget ui-widget-content ui-corner-all");
	
}

function post_load_login_section(section)
{
	// Transform the login form to do ajax request instead
	$("form#login_form").submit(function(e){
		e.preventDefault();
		var form = $(e.target);
		log("submit form action: ", form.attr("action"), "query: ", form.serialize());
		
		$.post(form.attr("action"), form.serialize())
		.done(function(response){
			log("login SUCCEEDED response: ", response);
			USERNAME = response;
			// Update the user panel title
			$('#user_panel_title').html(USERNAME+"'s data selections");
			// Load the section of the user panel
			$('#user_panel > .section[href]').each(function(){
					load_section($(this), $(this).attr('href'), post_load_user_section);
				});
			// Hide the login panel and title and show the user panel
			$('#login_panel_title, #login_panel').hide();
			$('#user_panel_title, #user_panel').show();
		})
		.fail(function(request, status){
			log("login FAILED response: ", request.responseText);
			alert_user(request.responseText);
		});
	});
}

function open_user_data_selection(href, name)
{
	log("Open user_data_selection for", name);
	var dialog = $("<div/>", {
	'class': "section",
	});
	load_section(dialog, 	href);
	dialog.dialog({
		title: name,
	});
}

function post_load_user_section(section)
{
	log("post_load_user_section");

	// Make dataset row openable
	$("tr.open_user_data_selection", section).hover(function(){
		$(this).toggleClass('ui-state-hover');
	}).each(function(){
		var row =$(this);
		$("td:not(:has(input))", row).click(function(){open_user_data_selection(row.attr("href"), row.attr("name"));});
	});
	
	// Transform the logout to a button
	$('#logout').button({
		icons: {
			primary: "ui-icon-eject"
		},
		text: true,
	}).click(function(){
			log("Logging out of the application. Href:", $('#logout').attr('href'));
			window.location.href = $('#logout').attr('href');
	});
}

// TODO make this more pretty
function add_search_data_panel(dataset_name, search_data_form_href, search_data_results_href, dataset_description)
{
	log("Adding search data panel for", dataset_name)
	
	var content = '<div class="section search_data_form_section" href="'+search_data_form_href+'">Please wait for the search form to load</div>\
				<div class="section search_data_results_section" href="'+search_data_results_href+'">You can search for data using the form on the left</div>';
	var title = 'Search data ' + dataset_name + ' <button type="button" class="help small_button" title="' + dataset_description + '">Help</button>';
	
	// Check if a panel with that id exists already
	var content_element = $("#"+dataset_name);
	if(content_element.length)
	{
		// If the element exists already, we replace it's content
		log("Search data panel for", dataset_name, "already exists, uppdating content", content_element.html());
		content_element.html(content);
		// If the title is provided we replace it
		var title_element = $("#"+dataset_name+"_title");
		if(title_element.length)
		{
			title_element.html(title);
		}
	}
	else
	{
		// Else we append the title and the content to the accordion
		log("Creating new search data panel for", dataset_name, "and title", title)
		title_element = $("<h3/>", {
			id: dataset_name+'_title',
		}).append(title);
		content_element = $("<div/>", {
			id: dataset_name,

			'class': "panel"
		}).append(content);
		
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
		
		$("#accordion").append(title_element, content_element);
	}
	//Load the loadable_sections with href with the content at the url 
	$('.search_data_form_section[href]', content_element).each(function(){
		load_section($(this), $(this).attr('href'), post_load_search_data_form_section);
	});
	$('.search_data_results_section[href]', content_element).each(function(){
		load_section($(this), $(this).attr('href'), post_load_search_data_result_section);
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
	
	//Load the search_dataset_form_section with href with the content at the url 
	$('.search_dataset_form_section[href]').each(function(){
		load_section($(this), $(this).attr('href'), post_load_search_dataset_form_section);
	});
	
	//Load the search_dataset_results_section with href with the content at the url 
	$('.search_dataset_results_section[href]').each(function(){
		load_section($(this), $(this).attr('href'), post_load_search_dataset_result_section);
	});
	if (USERNAME)
	{
		//Load the user section with href with the content at the url 
		$('#user_panel > .section[href]').each(function(){
			load_section($(this), $(this).attr('href'), post_load_user_section);
		});
	}
	else
	{
		//Load the login section
		$('#login_panel > .section[href]').each(function(){
			load_section($(this), $(this).attr('href'), post_load_login_section);
		});
	}
	
	// Make the accordion
	$("#accordion").accordion({ heightStyle: "content" });
	
}


// Attach all the events handler 
$(document).ready(load_events_handlers);
