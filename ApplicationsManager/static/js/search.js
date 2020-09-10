$(document).ready(function ()
{
	$("#searchbox").on("input", function ()
	{
		// Get our search results field and the csrf token needed by django.
		var searchresultsdeal = $(".searchresults");
		var csrftoken = $("input[name=\"csrfmiddlewaretoken\"]").val();
		var searchquery = $(this).val();
		searchresultsdeal.empty();
		searchresultsdeal.append($("<p></p>").text("Searching for "), $("<strong></strong>").text(searchquery));
		searchresultsdeal.css("visibility", "visible");
		console.log("Searching: " + searchquery);
		console.log("searchresultsdeal: " + searchresultsdeal);
		console.log("csrfmiddlewaretoken: " + csrftoken);

		$.ajax({
			url: "/api/search/",
			type: "POST",
			data: { csrfmiddlewaretoken: csrftoken, query: searchquery },
			dataType: "json",
			statusCode: {
				500: function () {
					searchresultsdeal.empty();
					searchresultsdeal.append($("<p></p>").text("500 Internal Server Error."));
				}
			},
			timeout: function () {
				searchresultsdeal.empty();
				searchresultsdeal.append($("<p></p>").text("Timed out"));
			},
			success: function (result, status) {
				// Find the search results div, we need to add some data to it.
				searchresultsdeal.empty();
				console.log("success: " + result["status"]);
				if (result["status"] == 0)
				{
					searchresultsdeal.append($("<p></p>").text(result["msg"]));
				}
				if (result["status"] == 1)
				{
					var objects = result["objects"];
					console.log(objects);
					var listitems = $("<ul></ul>");
					for (var i = 0; i < objects.length; i++)
					{
						var item = $("<li></li>");
						var application = objects[i];
						var name = application["username"]
						if (application["firstname"] && application["lastname"])
						{
							name = application["firstname"] + " " + application["lastname"];
						}
						var stuff = $("<a></a>").attr("href", "/view/" + application['applicationid'] + "/").text(name);
						item.append(stuff);
						listitems.append(item);
					}
					searchresultsdeal.append(listitems);
				}
			},
			error: function (result, status) {
				searchresultsdeal.empty();
				var shit = $("<ul></ul>").append($("<li></li>").append($("<p></p>").text("Error: " + result["msg"])))
				searchresultsdeal.append(shit);
			},
		});
	});
});