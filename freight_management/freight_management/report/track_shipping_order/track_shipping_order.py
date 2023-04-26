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
		_("Code") + ":Link/Direct Shipping:120",
		_("Vessel Name") + ":Link/Vessels:120",
		_("Terminal") + ":Link/Freight Location:200",
		_("Cargo") + "::100",
		_("Quantity") + "::120",
		_("ETA") + ":Date:120",
		_("ETB") + ":Date:120",
		_("ETC") + ":Date:120",
		_("Status") + "::60",
		# _("Company") + ":Link/Company:120",
	]


def get_employees(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(
		# tabFreight Order Line
		"""select name, vessel, loading_port,
	'Cargo', 'Qty', order_date, actual_date_berthing, actual_receive_date, workflow_state
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
