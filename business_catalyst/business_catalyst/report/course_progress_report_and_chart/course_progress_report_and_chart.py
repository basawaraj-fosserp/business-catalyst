# Copyright (c) 2013, FOSS United and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _
from frappe.utils import cint


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	charts = get_charts(data)
	return columns, data, [], charts


def get_data(filters=None):
	summary = []
	query_filter = {}
	conditions = []
	values = {}

	if filters:
		if filters.get("course"):
			conditions.append("course = %(course)s")
			values["course"] = filters.course

	if filters.get("current_lesson"):
		conditions.append("current_lesson = %(current_lesson)s")
		values["current_lesson"] = filters.get("current_lesson")

	if filters.get("current_lesson_like"):
		conditions.append("current_lesson LIKE %(current_lesson_like)s")
		values["current_lesson_like"] = filters.get("current_lesson_like")

	# Build SQL WHERE clause safely
	where_clause = " AND ".join(conditions) if conditions else "1=1"

	memberships = frappe.db.sql(
		f"""
		SELECT 
			name,
			course,
			member,
			member_name,
			progress,
			current_lesson
		FROM `tabLMS Enrollment`
		WHERE {where_clause}
		ORDER BY course
		""",
		values,
		as_dict=True
	)

	for membership in memberships:
		summary.append(
			frappe._dict(
				{
					"course": membership.name,
					"course_name": frappe.db.get_value("LMS Course", membership.course, "title"),
					"member": membership.member,
					"member_name": membership.member_name,
					"progress": cint(membership.progress),
					"current_lesson" : membership.current_lesson
				}
			)
		)

	return summary


def get_columns():
	return [
		{
			"fieldname": "course_name",
			"fieldtype": "Data",
			"label": _("Course Name"),
			"width": 300,
		},
		{
			"fieldname": "member",
			"fieldtype": "Link",
			"label": _("Member"),
			"options": "User",
			"width": 200,
		},
		{
			"fieldname": "member_name",
			"fieldtype": "Data",
			"label": _("Member Name"),
			"width": 150,
		},
		{
			"fieldname": "current_lesson",
			"fieldtype": "Data",
			"label": _("Current Lesson"),
			"width": 150,
		},
		{
			"fieldname": "progress",
			"fieldtype": "Data",
			"label": _("Progress (%)"),
			"width": 120,
		},
	]


def get_charts(data):
	if not data:
		return None

	completed = 0
	less_than_hundred = 0
	less_than_seventy_one = 0
	less_than_forty_one = 0
	less_than_eleven = 0

	for row in data:
		if row.progress == 100:
			completed += 1
		elif row.progress < 100 and row.progress > 70:
			less_than_hundred += 1
		elif row.progress < 71 and row.progress > 40:
			less_than_seventy_one += 1
		elif row.progress < 41 and row.progress > 10:
			less_than_forty_one += 1
		elif row.progress < 11:
			less_than_eleven += 1

	charts = {
		"data": {
			"labels": ["0-10", "11-40", "41-70", "71-99", "100"],
			"datasets": [
				{
					"name": "Progress (%)",
					"values": [
						less_than_eleven,
						less_than_forty_one,
						less_than_seventy_one,
						less_than_hundred,
						completed,
					],
				}
			],
		},
		"type": "pie",
		"colors": ["#ff0e0e", "#ff9966", "#ffcc00", "#99cc33", "#339900"],
	}
	return charts
