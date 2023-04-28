# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.utils import cstr


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_data(filters)

	report_data = []
	for row in data:
		report_row = []
		for column in columns:
			cell_value = render_cell(row, column)
			report_row.append(cell_value)
		report_data.append(report_row)

	return columns, report_data


def render_cell(doc, fieldname, row):
    print(f"fieldname is {fieldname}")
    print(f"row is {row}")
    
    value = cstr(row.get(fieldname))
    if fieldname == "my_column":
        if value == "Value A":
            return f"<div style='color: red;'>{value}</div>"
        elif value == "Value B":
            return f"<div style='color: blue;'>{value}</div>"
    return value



def get_columns():
	return [
		_("Anchor No") + "::60",
		_("Vessel Name") + ":Link/Vessels:120",
		_("Terminal") + ":Link/Freight Location:120",
		_("Cargo") + ":Link/Item:100",
		_("Quantity") + "::80",
		_("ETA") + ":Datetime:120",
		_("ETB") + ":Datetime:120",
		_("ETC") + ":Datetime:120",
		_("24hr Disch/load rate") + ":Float:100",
		_("Qty (Remain)") + ":Float:80",
		_("Receiver") + ":Cusomer:120",
		_("Exporters") + ":Cusomer:120",
		_("Status") + "::120",
		_("Remarks") + "::120"
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
			DS.customer, DS.consignee,

			CASE
				WHEN DS.expected_date_berthing IS NULL THEN 'Unknown'
				WHEN DS.actual_date_berthing IS NULL AND DS.expected_date_berthing > NOW() THEN 'Scheduled'
				WHEN DS.actual_date_berthing IS NULL AND DS.expected_date_berthing <= NOW() THEN 'Overdue Arrival'
				WHEN DS.actual_date_berthing IS NOT NULL AND DS.expected_receive_date IS NULL THEN 'Arrived'
				WHEN DS.actual_date_berthing IS NOT NULL AND DS.actual_receive_date IS NULL AND DS.expected_receive_date > NOW() THEN 'Unloading'
				WHEN DS.actual_date_berthing IS NOT NULL AND DS.actual_receive_date IS NULL AND DS.expected_receive_date <= NOW() THEN 'Overdue Departure'
				WHEN DS.actual_receive_date IS NOT NULL THEN 'Delivered'
				ELSE 'Unknown'
			END AS status,
			''

			FROM `tabFreight Order Line` FOL
			RIGHT JOIN `tabDirect Shipping` DS
			ON FOL.parent = DS.name
	"""+where_condition+" order by loading_port"

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
