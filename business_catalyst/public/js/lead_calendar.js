frappe.views.calendar["Lead"] = {
    field_map: {
		"start": "start_date",
		"end": "end_date",
		"id": "name",
		"title": "title",
		"color":"color"
	},
    get_events_method: "business_catalyst.api.get_calendar_details"
}