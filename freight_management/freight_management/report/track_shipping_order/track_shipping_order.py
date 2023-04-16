# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_employees(filters)

	return columns, data


def get_columns():
	return [
		_("Vessel Name") + ":Link/Employee:120",
		_("Terminal") + ":Data:200",
		_("Cargo") + ":Date:100",
		_("Quantity") + ":Link/Branch:120",
		_("ETA") + ":Link/Department:120",
		_("ETC") + ":Link/Designation:120",
		_("Status") + "::60",
		# _("Company") + ":Link/Company:120",
	]


def get_employees(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		# tabFreight Order Line
		"""select name, loading_port, name1',
	'Qty', order_date, expected_receive_date, docstatus
	from `tabDirect Shipping` %s"""
		% conditions,
		as_list=1,
	)


def get_conditions(filters):
	conditions = ""
	# if filters.get("month"):
	# 	month = [
	# 		"Jan",
	# 		"Feb",
	# 		"Mar",
	# 		"Apr",
	# 		"May",
	# 		"Jun",
	# 		"Jul",
	# 		"Aug",
	# 		"Sep",
	# 		"Oct",
	# 		"Nov",
	# 		"Dec",
	# 	].index(filters["month"]) + 1
	# 	conditions += " and month(date_of_birth) = '%s'" % month

	# if filters.get("company"):
	# 	conditions += " and company = '%s'" % filters["company"].replace("'", "\\'")

	return conditions
