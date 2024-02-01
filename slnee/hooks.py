from . import __version__ as app_version

app_name = "slnee"
app_title = "Slnee"
app_publisher = "Weslati Baha Eddine"
app_description = "Custom apps developed by Slnee engineers"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "baha@slnee.com"
app_license = "MIT"
#app_logo_url = "/assets/slnee/images/logo.png"


doc_events = {
        "Company": {

        "before_validate": "slnee.color.change_color"
		},
    #     "Payroll Entry":{
    #     "validate":["slnee.slnee.custom_hr.common.payroll_common.assign_override_methods"]
    # }
}

override_doctype_class = {
    "Payroll Entry": "slnee.slnee.custom_hr.common.payroll_common.CustomPayrollEntry",
}

	
jenv = {
    "methods": [
        "getqrcode:slnee.fatoora.getqrcode",
	"test:slnee.test.test",
	"money:slnee.data.money_in_words",
	"encrypt:slnee.utils.print_format.encrypt"

    ]
}




website_context = {
#	"favicon" : "/assets/slnee/images/favicon.png",
	"splash_image" : "/files/erplogo1.png",
}








fixtures = ["Custom Field",
	#{"dt":"Print Format","filters":[["name","like","VAT E-invoice KSA"]]},
	#{"dt":"Server Script","filters":[["name","like","columns number"]]},
	{"dt":"Font"},
	{"dt":"Translation"},
	#{"dt":"Navbar Settings"},
	#{"dt":"Website Settings"},
	#{"dt":"File", "filters":[["attached_to_field","like","flag"]]},
	{"dt":"Country"},
	{"dt":"Report", "filters":[['name','in',['Fonts','Sales Analytics','Purchase Analytics']]]},
	{"dt":"Workspace","filters":[['name','in',['Accounting','HR']]]},
	{"dt":"Translation"}
	#{"dt":"Custom Print Format","filters":[["name","like","invoice"]]},
	#{"dt":"div","filters":[["parent","like","invoice"]]},
	#{"dt":"Print Format","filters":[["name","like","invoice"]]}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
#app_include_css = "/assets/slnee/css/printview.css"
# app_include_js = "/assets/slnee/js/slnee.js"

# include js, css files in header of web template
# web_include_css = "/assets/slnee/css/slnee.css"
# web_include_js = "/assets/slnee/js/slnee.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "slnee/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "slnee.install.before_install"
# after_install = "slnee.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "slnee.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"slnee.tasks.all"
# 	],
# 	"daily": [
# 		"slnee.tasks.daily"
# 	],
# 	"hourly": [
# 		"slnee.tasks.hourly"
# 	],
# 	"weekly": [
# 		"slnee.tasks.weekly"
# 	]
# 	"monthly": [
# 		"slnee.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "slnee.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "slnee.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "slnee.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"slnee.auth.validate"
# ]

