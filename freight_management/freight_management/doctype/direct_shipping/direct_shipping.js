frappe.ui.form.on('Direct Shipping', {
	refresh(frm) {
		frm.set_value('status', get_berthing_status(frm.doc));
	},
	actual_date_berthing: function(frm) {
		if(!frm.doc.actual_date_berthing)
        	frm.set_value('actual_date_berthing', frm.doc.expected_date_berthing);
    },
	actual_receive_date: function(frm) {
		if(!frm.doc.actual_date_berthing)
        	frm.set_value('actual_receive_date', frm.doc.expected_receive_date);
    },
})


function get_berthing_status(doc) {
    if (!doc.expected_date_berthing) {
        return 'Unknown';
    }
    if (!doc.actual_date_berthing && doc.expected_date_berthing > frappe.datetime.now_datetime()) {
        return 'Scheduled';
    }
    if (!doc.actual_date_berthing && doc.expected_date_berthing <= frappe.datetime.now_datetime()) {
        return 'Overdue Arrival';
    }
    if (doc.actual_date_berthing && !doc.expected_receive_date) {
        return 'Arrived';
    }
    if (doc.actual_date_berthing && !doc.actual_receive_date && doc.expected_receive_date > frappe.datetime.now_datetime()) {
        return 'Unloading';
    }
    if (doc.actual_date_berthing && !doc.actual_receive_date && doc.expected_receive_date <= frappe.datetime.now_datetime()) {
        return 'Overdue Departure';
    }
    if (doc.actual_receive_date) {
        return 'Delivered';
    }
    return 'Unknown';
}


// frappe.listview_settings['Direct Shipping'] = {
//     get_indicator: function(doc) {
//         console.log("hello there!");
//         return [doc.status, { 'Unknown': 'grey',
//             'Scheduled': 'orange',
//             'Overdue Arrival': 'red',
//             'Arrived': 'green',
//             'Unloading': 'blue',
//             'Overdue Departure': 'red',
//             'Delivered': 'darkgrey'
//         }[doc.status]];
//     }
// };
