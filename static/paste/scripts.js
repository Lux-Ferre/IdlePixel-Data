if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
			document.documentElement.setAttribute("data-bs-theme", "light")
}
$("document").ready(function(){
	const server_data = $("#server_data").data()

	const creation_datetime = new Date(server_data["creationTimestamp"] * 1000)
	const current_datetime = new Date()
	const keyword_map = {
		current_local_date: current_datetime.toLocaleDateString(),
		current_local_time: current_datetime.toLocaleTimeString(),
		current_local_datetime: current_datetime.toLocaleString(),
		current_utc_datetime: current_datetime.toUTCString().slice(0, -4),	// Slice removes confusing "GMT" timezone
		creation_local_date: creation_datetime.toLocaleDateString(),
		creation_local_time: creation_datetime.toLocaleTimeString(),
		creation_local_datetime: creation_datetime.toLocaleString(),
		creation_utc_datetime: creation_datetime.toUTCString().slice(0, -4)	// Slice removes confusing "GMT" timezone
	}

	const replace_keywords = function(index, html){
		let modified_html = html

		for (const [key, value] of Object.entries(keyword_map)) {
			modified_html = modified_html.replace(`{{ ${key} }}`, value)
		}

		return modified_html
	}

	$("#paste_title").html(replace_keywords);
	$("#paste_area").html(replace_keywords)

})