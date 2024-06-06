frappe.views.calendar["Lead"] = {
    field_map: {
		"start": "start_date",
		"end": "start_date",
		"id": "name",
		"title": "title",
		"allDay": "allDay",
		"color":"color"
	},
    get_events_method: "business_catalyst.api.get_calendar_details"
}