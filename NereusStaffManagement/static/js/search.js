
$("#searchbox").change(function() {
	$.ajax({
		url: "/api/search/",
		type: "POST",
		data: { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value, query: $(this).text() },
		dataType: "json",
		success: function ()
		{
			// TODO
		},
		failure: function ()
		{
			
		},
	});
});