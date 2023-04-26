# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		_("Anchor No") + "::20",
		_("Vessel Name") + ":Link/Vessels:120",
		_("Terminal") + ":Link/Freight Location:200",
		_("Cargo") + ":Link/Item:100",
		_("Quantity") + "::120",
		_("ETA") + ":Date:120",
		_("ETB") + ":Date:120",
		_("ETC") + ":Date:120",
		_("24hr Disch/load rate") + ":Float:60",
		_("Qty (Remain)") + ":Float:60",
		_("Status") + "::120",
		# _("Company") + ":Link/Company:120",
	]


def get_data(filters):
	conditions = get_conditions(filters)
	where_condition = ""
	if conditions is not None:
		"""WHERE {conditions}""".format(conditions=conditions)

	# query = """
	# 	SELECT name, vessel, loading_port, 'cargo', 'qty', order_date, 
	# 		actual_date_berthing, actual_receive_date, workflow_state
    #     	FROM `tabDirect Shipping`
	# 	"""+where_condition

	query = """
		SELECT 
			DS.achor_number, DS.vessel, DS.loading_port,
			FOL.items as 'cargo', FOL.quantity, 
			DS.order_date as ETA, 
			COALESCE(DS.actual_date_berthing, DS.expected_date_berthing) as ETB,
			COALESCE(DS.actual_receive_date, DS.expected_receive_date) as ETC,
			FOL.discharge_rate, FOL.remain_qty,

			CASE
				WHEN DS.expected_date_berthing IS NULL THEN 'Unknown'
				WHEN DS.actual_date_berthing IS NULL AND DS.expected_date_berthing > NOW() THEN 'Scheduled'
				WHEN DS.actual_date_berthing IS NULL AND DS.expected_date_berthing <= NOW() THEN 'Overdue Arrival'
				WHEN DS.actual_date_berthing IS NOT NULL AND DS.expected_receive_date IS NULL THEN 'Arrived'
				WHEN DS.actual_date_berthing IS NOT NULL AND DS.actual_receive_date IS NULL AND DS.expected_receive_date > NOW() THEN 'Unloading'
				WHEN DS.actual_date_berthing IS NOT NULL AND DS.actual_receive_date IS NULL AND DS.expected_receive_date <= NOW() THEN 'Overdue Departure'
				WHEN DS.actual_receive_date IS NOT NULL THEN 'Delivered'
				ELSE 'Unknown'
			END AS status

			FROM `tabFreight Order Line` FOL
			JOIN `tabDirect Shipping` DS
			ON FOL.parent = DS.name
	"""+where_condition

	print("query is", query)
	result = frappe.db.sql(query, as_list=1)
	return [r for r in result]


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
