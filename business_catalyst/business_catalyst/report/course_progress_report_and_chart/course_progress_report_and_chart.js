// Copyright (c) 2025, Viral Patel and contributors
// For license information, please see license.txt

frappe.query_reports["Course Progress Report and Chart"] = {
	"filters": [
		{
			fieldname: "course",
			label: __("Course"),
			fieldtype: "Link",
			options: "LMS Course",
			reqd: 1,
		},
		{
			fieldname: "current_lesson",
			label: __("Course Lesson"),
			fieldtype: "Link",
			options: "Course Lesson",
			reqd: 0,
		},
		{
			fieldname: "current_lesson_like",
			label: __("Course Lesson Like"),
			fieldtype: "Data",
			options: "Course Lesson",
			reqd: 0,
		}
	]
};
