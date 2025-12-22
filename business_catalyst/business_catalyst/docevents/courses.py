import frappe
from lms.lms.utils import (
    update_course_filters,
    get_course_fields,
    get_featured_courses,
    get_enrollment_details,
    get_course_card_details
)
from frappe.rate_limiter import rate_limit


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=500, seconds=60 * 60)
def get_courses(filters=None, start=0):
    """Returns the list of courses."""

    if not filters:
        filters = {}

    filters, or_filters, show_featured = update_course_filters(filters)
    fields = get_course_fields()
    
    user = frappe.session.user

    premiumCource = frappe.db.get_list("LMS Course", {"only_allow_this_course" : 1}, pluck="name")

    enrolledCourse = frappe.db.get_list("LMS Enrollment", {"member" : user}, "course")

    enrolledCourse = [row.course for row in enrolledCourse]
     
    
    is_enrolled_for_premium = False
    if premiumCource:
        conditions = " course in {} ".format(
                    "(" + ", ".join([f'"{l}"' for l in premiumCource]) + ")")
        
        is_enrolled_for_premium = frappe.db.sql(
            f"""
                Select name
                From `tabLMS Enrollment`
                Where member = '{user}' and {conditions}

            """, as_dict=True
        )
        
        if is_enrolled_for_premium:
            filters.update({
                "name" : ["in" , enrolledCourse] 
            })

    courses = frappe.get_all(
        "LMS Course",
        filters=filters,
        fields=fields,
        or_filters=or_filters,
        order_by="enrollments desc",
        start=start,
        page_length=30,
    )

    if show_featured:
        courses = get_featured_courses(filters, or_filters, fields) + courses

    courses = get_enrollment_details(courses)
    courses = get_course_card_details(courses)
    return courses