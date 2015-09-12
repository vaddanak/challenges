
// Variables declared as "var myvariable" is visible only within this block.
(function() {
	
	/* TO-DO
	create db to store questions and solution
	create backup of db in xml format
	make editor screen to add/edit entry
	retrieve content from db, in xml format
	
	*/
	
	get_topic_titles_xml();
	
	var $iframeContent = $("#iframeContent");
	var $issues_titles = $("#issues_titles");
	var fraction = .95;
	//set iframe height relative to window height	
	$iframeContent.height($(window).outerHeight()*fraction);
	//$issues_titles.height($(window).outerHeight()*.93);
	
	//attach resize event to window:
	//	1. adjust iframe height relative to $(window).outerHeight()
	//	2. adjust #issues_titles height relative to window also
	$(window).on("resize", function(event) {
		$iframeContent.height($(window).outerHeight()*fraction);
		//$issues_titles.height($(window).outerHeight()*.93);
	});
	
	
	//add entry to question list
	$('#add_entry').on('click', state);

	//var name = 'hat';// "var" make visible only within function namespace

	
	//alert($("#py1").text());

	//$('ul > li > a').addClass('no_underline'); 
	
	//$('#content_hints').hide();
	
	/*
		1. Add class activeLI to selected ul > li item
		2. Extract section id from ul > li > a[href]
		3. Use extracted id to retrieve section content
		4. Determine number of lines in section content
		5. Embed the section content in iframe via srcdoc attribute and
		   set its height using number of lines to ensure proper height
		6. Default trigger first ul > li upon page load   
	*/
	/*
	$('ul#topics').on('click', 'li', function(eventObject) {
		$(this).siblings().removeClass('activeLI');
		$(this).addClass('activeLI');
		//alert( $(this).html() );
		var $iframeContent = $('iframe#iframeContent');
		var $a = $(this).find('a[href]');
		var anchorID = $a.attr('href')
		anchorID = anchorID.match(/^#(\w+)/)[1];
		
		var content = $('#'+anchorID).parent().next('pre').html();
		var lineHeight = 17; // unit of em
		var totalLines = countLines(content);
		//$iframeContent.attr('height', (lineHeight*totalLines)+'em')
		//	.attr('srcdoc','<pre>'+content+'</pre>');
		$iframeContent.attr('height', $(document).innerHeight()*.97)
			.attr('srcdoc','<pre>'+content+'</pre>');
		//alert(content);
	}).children('li:first').trigger('click');
	*/
	
	
	
	
})();


/*
PURPOSE: 
PRECON: 
POSTCON: 
*/

/*
PURPOSE: Fn creates overlay that covers entire page and blocks access to
	HTML controls underneath it.
PRECON: 
POSTCON: 
*/
function overlay() {
	var $overlay = $("<div></div>");
	$overlay.css({
		position: "absolute",
		top: 0,
		left: 0,
		width:$(document).outerWidth(),
		height:$(document).outerHeight(),
		zIndex: 1000,
		opacity: 0.4,
		backgroundColor:"blue"
	});

	$(document.body).append($overlay);
	$(window).on("resize", function(event) {
		console.log(event.type);
		$overlay.css({
			width:$(document).outerWidth(),
			height:$(document).outerHeight()
		});
	});	
	
	return $overlay;
}

/*
PURPOSE: 
PRECON: 
POSTCON: 
*/
function state(event, edit_object) {
	//alert('called state()' + event.target.id);		
	
	//calcuate width and height dimensions
	var winWidth = $(window).innerWidth();
	var winHeight = $(window).innerHeight();
	var mwidth = winWidth*.8;
	var mleft = (winWidth-mwidth)/2;
	var mheight = winHeight*.8;
	var mtop = (winHeight-mheight)/2;
	
	//this div contains all elements that is displayed on blockUI for adding entry
	var $div = $("#text_edit_div");	
	var $div_textbox_textarea = $div.find("div");
	var $textbox = $("#topic_title");
	var $textarea = $("#topic_solution");
	var $save = $div.find("button[name='save']");
	var $clear = $div.find("button[name='clear']");
	var $quit = $div.find("button[name='quit']");		
	
	
	//blockUI shows window to add entry
	$.blockUI({
		message: $div,//for div#text_edit_div element
		//css for div.blockUI.blockMsg.blockPage created by blockUI "plugin"
		css: {width:mwidth, left:mleft, height:mheight, top:mtop, border:0,
			cursor:"default"},
		overlayCSS: {cursor:"default"},
		onBlock: function() {			
			//div#text_edit_div contains form to add entry
			$div
			.css({width:mwidth,height:mheight*.95,margin:0,border:0});
			//this div contains label + textbox + textarea
			//$("#text_edit_div div")
			$div_textbox_textarea
			.css({width:mwidth,margin:0,border:0});
			//textbox for topic title
			//$("#text_edit_div input[type='text']")
			$textbox
			.css({width:"98%",color:"blue",textAlign:"center"});			
			//textarea for topic solution
			//$("#text_edit_div textarea") //for textarea inside div
			$textarea
			.css({width:"98%",height:mheight*.80,margin:"auto",border:"auto"});
			
			//store textarea width and height to $textarea.data()
			$textarea.data("width", $textarea.outerWidth() );
			$textarea.data("height", $textarea.outerHeight() );
			
			//if passed in edit_object, then set title and solution
			//$.val() function works for form fields, whereas $.text() function works
			//	on elements that has open/close tags and content accessible via
			//	innerHTML.  $.text() does NOT work on form fields.			
			if(edit_object) {
				//$textbox.text(edit_object.title);//won't work here, weird???
				$textbox.val(edit_object.title);
				//$textbox[0].value = edit_object.title;//this works!!!
				//convert html entity to literal symbols inside <p> element,
				//	then extract <p> content as text and display as textarea value
				$textarea.val($("<p></p>").html(edit_object.solution).text());
			}
			
		},
		onUnblock: function(element, options) {
			$div.off(".editSpace");//remove event handler in .editSpace namespace	
		}
	});	
	
	
	//attach click event to button "save"; 
	//post topic "title" and "solution" to server
	//registering under namespace ".editSpace"
	$div.on("click.editSpace", "button[name='save']", function(event) {		
		event.preventDefault();
		//serialize textbox and textarea elements; create post data
		var mdata = $("#topic_title, #topic_solution").serialize();	
		//var mdata = "topic_title=" + encodeURI($textbox.val().trim())
		//	+ "&topic_solution=" + encodeURI($textarea.val().trim());
		$.ajax({
			method: "POST",
			data: mdata,
			dataType: "text",
			url: "cgi-bin/save.py",
			success: function(data, status, xhr) {
				alert("SUCCESS!\n" + data);
			}					
		});
	});
	
	
	//attach focusin, focusout, mouseup events to textarea
	//highlight label "solution" when textarea gets focusin;
	//prevents textarea resizing.
	$div.on("focusin.editSpace focusout.editSpace mouseup.editSpace",
		"#topic_solution", function(event) {
		event.preventDefault();
		//console.log(event.type);
		//on focusin event on textarea, textarea label gets highlight
		if(event.type=="focusin")
			$div.find("label[for='topic_solution']").css({backgroundColor:"yellow"});
		else if(event.type=="focusout")
			$div.find("label[for='topic_solution']").css({backgroundColor:""});
		//prevent resizing textarea		
		else if(event.type=="mouseup") {
			if($textarea.outerWidth() != $textarea.data("width"))
				$textarea.outerWidth($textarea.data("width"));
			if($textarea.outerHeight() != $textarea.data("height") )
				$textarea.outerHeight($textarea.data("height"));	
		}	
	});
	
	//attach focusin, focusout events to textbox
	//highlight label "Question or Topic" when textbox gets focusin	
	$div.on("focusin.editSpace focusout.editSpace", "#topic_title",
		function(event) {
		event.preventDefault();
		//console.log(event.type);
		//on focusin event on textbox, textbox label gets highlight
		if(event.type=="focusin")
			$div.find("label[for='topic_title']").css({backgroundColor:"yellow"});
		else if(event.type=="focusout")
			$div.find("label[for='topic_title']").css({backgroundColor:""});
	});
	
	//attach click event to button "quit"
	//unblockUI when "quit" button is pressed	
	$div.on("click.editSpace", "button[name='quit']", function(event) {
		$.unblockUI();
		$("#issues_titles div").remove();
		get_topic_titles_xml();		
	});
	
	//attach click event to button "clear"	
	$div.on("click.editSpace", "button[name='clear']", function(event) {
		event.preventDefault();//prevents form closing the data entry
		//$textbox[0].value = "";//empty the text content in the textbox field
		//$textarea[0].value = "";
		$textbox.val("");
		$textarea.val("");
	});
	
	//attach click event to button "delete"
	$div.on("click.editSpace", "button[name='delete']", function(event) {
		event.preventDefault();
		var title = encodeURI($textbox.val().trim());
		var post_string = "action=delete_topic_entry&topic_title=" + title;
		console.log(post_string);
		$.ajax({
			method: "POST",
			url: "cgi-bin/access.py",
			data: post_string,
			dataType: "text",
			success: function(data, status, xhr) {
				alert("deleted " + data + " row(s)");
				
			}
		});
	});
	
}

/*	NOTES on namespace --- code as-is in this block not work in current syntax
	var validate = function() {
	  // Code to validate form entries
	};
	 
	// Delegate events under the ".validator" namespace
	$( "form" ).on( "click.validator", "button", validate );
	 
	$( "form" ).on( "keypress.validator", "input[type='text']", validate );
	 
	// Remove event handlers in the ".validator" namespace
	$( "form" ).off( ".validator" );
	
	
	
	Remove all event handlers from all paragraphs:
	$( "p" ).off();
	
	Remove all delegated click handlers from all paragraphs:
	$( "p" ).off( "click", "**" );
	
	
	Remove just one previously bound handler by passing it as the third argument:
	var foo = function() {
	  // Code to handle some kind of event
	};
	 
	// ... Now foo will be called when paragraphs are clicked ...
	$( "body" ).on( "click", "p", foo );
	 
	// ... Foo will no longer be called.
	$( "body" ).off( "click", "p", foo );
	
	
	
*/
	
	
/*
PURPOSE: Fn counts the number of lines in given text.
PRECON: 'text' is a string.
POSTCON: Fn returns number of lines in 'text' plus one.
*/

/*
function countLines(text) {	
	var count = 0; //var makes local scope, ie only visible inside function
	var index = 0;
	do {
		index = text.indexOf('\n', index+1);
		if(index != -1)
			++count;
		else
			break;
	} while(true);
	
	//alert("inside: " + (count+1) );
	return count+1; // +1 for last line which does not end with \n
}
*/

/*
PURPOSE: 
PRECON: 
POSTCON: 
*/
function get_topic_titles_xml() {
	//BALLOT BOX, BALLOT BOX WITH CHECK, BALLOT BOX WITH X
	var symbol_box = ["&#x2610;", "&#x2611;", "&#x2612;"];
	var writing_hand = "&#x270D;"
	var active_element = $("#issues_titles").data("active_element");
	
	$.ajax({
		method: "POST",
		url: "cgi-bin/access.py",
		data: "action=get_topic_titles_xml",
		dataType: "text",
		success: function(data, status, xhr) {			
			//compose topic titles for html page insertion
			//in $.each() function, element == this, ie DOM object; 
			//	return false to stop iteration.
			//data is xml text, xml construct is ...
			//	<topics><topic><title>..</title>></topic></topics>
			var titles = "";
			var title = "";
			$(data).find("topic").each(function(index, element) {//for each topic el
				title = $(this).find("title").text().trim();
				titles += "<div><label>" + symbol_box[0] + "</label>"
					+"<label>" + writing_hand + "</label>"
					//this.textContent==the_title
					+ "<span" 
					+ (title==active_element?" class='active_element'>":">")
					+ title
					+ "</span></div>";
			});
			//insert newly created elements after "Add entry" button
			$("#issues_titles").append($(titles));
			//initialize $label.data("state") to 0; index for ballot box symbol
			//	set for both labels within "#issues_titles div"? yes
			//$("#issues_titles div label").each(function(index, element) {
				//alert(element.tagName); return false; //LABEL
				//console.log("here");
			//	$(element).data("state",0);
			//});			
			//attach click event to label:eq(0) to select different ballot box
			$("#issues_titles div").on("click", "label:eq(0)", function(event) {
				var $label = $(event.target);//label with ballot box
				var current_state = $label.data("state");
				//alert($label.data("state"));//undefined
				if(current_state===undefined)//data was not yet defined for label
					current_state=0;				
				var next_state = (current_state +1)%symbol_box.length;
				$label.data("state", next_state);
				//alert(next_state);
				$label.html(symbol_box[next_state]);
			});
			//attach click event to label:eq(1) element to open edit window
			$("#issues_titles div").on("click", "label:eq(1)", function(event) {
				var $label = $(event.target);//label with writing_hand icon
				var $span = $label.parent().find("span");
				var post_string = "action=get_topic_solution&topic_title=" 
					+ encodeURI($span.text());
				
				//store last active element text in #issues data to be retrieved
				//	after edit window closes; when edit window closes, actual 
				//	element will be removed and new ones will be created;
				//	so, you will need to find the new one with the same topic
				//	title text as this stored one and then add class .active_element
				//	to the new one found.
				//$("#issues").data("active_element", $span.text());//MOVED!
								
				//get topic solution for selected topic title and open
				//	edit window
				$.ajax({
					method: "POST",
					data: post_string,
					dataType: "text",
					url: "cgi-bin/access.py",
					success: function(data, status, xhr) {
						var edit_object 
							= {"title":$span.text(), "solution":data.trim()};
						state(null, edit_object);//OPEN EDIT WINDOW!!!
					}
				});
				
			});
			//attach click event to span element to retrieve topic solution
			//	from db and display in iframe.
			$("#issues_titles div").on("click", "span", function(event) {
				var $span = $(event.target);//span show topic title	
				
				//remove .active_element class from all span within "#issues div"
				//	then add class to selected span; store last active element
				//	in $("#issues").data("active_element").
				$("#issues_titles div span").removeClass("active_element");
				$span.addClass("active_element");
				$("#issues_titles").data("active_element", $span.text());
							
				//create post string with span topic title text
				action = "action=get_topic_solution&topic_title=" 
					+ encodeURI($span.text());//escape space in URL
				console.log(action);	
				$.ajax({
					method: "POST",
					url: "cgi-bin/access.py",
					data: action,
					success: function(data, status, xhr) {
						//alert(data);
						$("#iframeContent")[0].srcdoc 
							= "<pre>"+data.trim()+"</pre>";
					},
					dataType: "text"
				});
			});
			//
		}//end...	success		
	});//end... 	$.ajax
	
	
	/*
	$.post("cgi-bin/howto.py", function(data) {
		$("#showme").text(data);
	});
	*/
}









// Anonymouse function executes after the web page loads.
$(document).ready(function(){


});























