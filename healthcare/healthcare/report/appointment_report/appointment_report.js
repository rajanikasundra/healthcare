// Copyright (c) 2024, sigzen and contributors
// For license information, please see license.txt

// frappe.query_reports["appointment report"] = {
// 	"filters": [


// 	]
// };


frappe.query_reports["appointment report"] = {
    filters: [
        {
            fieldname: "custom_doctor",
            label: __("Doctor"),
            fieldtype: "Link",
            options: "Doctor",
            reqd: 0, 
            default: "",
            width: 200,
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 1, 
            default: frappe.datetime.month_start(),
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 1, 
            default: frappe.datetime.month_end(),
        },
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: "\nOpen\nUnverified\nClosed", 
        },
    ],
};
