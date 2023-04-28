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
	
	data_dict = []
	for row in data:
		row_dict = {}
		for column in columns:
			row_dict[column['fieldname']] = row[columns.index(column)]
		data_dict.append(row_dict)


	report_data = []
	for row in data_dict:
		report_row = []
		for column in columns:
			cell_value = render_cell(row, column)
			report_row.append(cell_value)
		report_data.append(report_row)

	return columns, report_data


def render_cell(row, column):
	if column["fieldname"] == "status":
		value = cstr(row.get(column["fieldname"]))
		colors = {
			'Unknown': 'grey',
			'Scheduled': 'orange',
			'Overdue Arrival': 'red',
			'Arrived': 'green',
			'Unloading': 'blue',
			'Overdue Departure': 'red',
			'Delivered': 'darkgrey'
		}
		color = colors.get(value, '')
		if color:
			return f"<div style='color: {color};'>{value}</div>"

	return row.get(column["fieldname"])


def get_columns():
	columns = [
		{
			"label": _("Anchor No"),
			"fieldname": "achor_number",
			"fieldtype": "Data",
			"width": 60
		},
		{
			"label": _("Vessel Name"),
			"fieldname": "vessel",
			"fieldtype": "Link",
			"options": "Vessels",
			"width": 120
		},
		{
			"label": _("Terminal"),
			"fieldname": "loading_port",
			"fieldtype": "Link",
			"options": "Freight Location",
			"width": 120
		},
		{
			"label": _("Cargo"),
			"fieldname": "cargo",
			"fieldtype": "Link",
			"options": "Item",
			"width": 100
		},
		{
			"label": _("Quantity"),
			"fieldname": "quantity",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": _("ETA"),
			"fieldname": "ETA",
			"fieldtype": "Datetime",
			"width": 120
		},
		{
			"label": _("ETB"),
			"fieldname": "ETB",
			"fieldtype": "Datetime",
			"width": 120
		},
		{
			"label": _("ETC"),
			"fieldname": "ETC",
			"fieldtype": "Datetime",
			"width": 120
		},
		{
			 "label": _("24hr Disch/load rate"),
			 "fieldname": "discharge_rate",
			 "fieldtype": "Float",
			 "width": 100
		 },
		{
			"label": _("Qty (Remain)"),
			"fieldname": "remain_qty",
			"fieldtype": "Float",
			"width": 80
		},
		{
			"label": _("Receiver"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 120
		},
		{
			"label": _("Exporters"),
			"fieldname": "consignee",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 120
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Remarks"),
			"fieldname": "remarks",
			"fieldtype": "Data",
			"width": 120
		}
		# {
		# 	"label": _("Company"),
		# 	"fieldname": "company",
		# 	"fieldtype": "Link",
		# 	"options": "Company",
		# 	"width": 120
		# }
	]
	
	return columns


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
