
frappe.ui.form.on('Appointment', {
    refresh: function (frm) {
        if (!frm.is_new()) {
        
            frm.page.set_primary_action(__('Create Doctor Charge Invoice'), function () {
                frappe.call({
                    method: "healthcare.payment_entry.generate_appointment_invoice", 
                    args: {
                        appointment_name: frm.doc.name
                    },
                    callback: function (response) {
                        if (response.message) {
                            frappe.show_alert({
                                message: __('Sales Invoice Created: {0}', [response.message]),
                                indicator: 'green'
                            });
                            window.location.href = "/app/sales-invoice/" + response.message;
                        }
                    }
                });
            });
        }
    }
});























































// frappe.ui.form.on('Appointment', {
//     refresh: function (frm) {
//         if (!frm.is_new()) {
//             // Add Generate Invoice Button
//             frm.add_custom_button(__('Doctor Charge Invoice'), function () {
//                 frappe.call({
//                     method: "healthcare.payment_entry.generate_appointment_invoice",
//                     args: {
//                         appointment_name: frm.doc.name
//                     },
//                     callback: function (response) {
//                         if (response.message) {
//                             frappe.show_alert({
//                                 message: __('Sales Invoice Created: {0}', [response.message]),
//                                 indicator: 'green'
//                             });
//                             window.location.href = "/app/sales-invoice/" + response.message;
//                         }
//                     }
//                 });
//             }, __("A"));
//         }
//     }
// });


// frappe.ui.form.on('Appointment', {
//     refresh: function (frm) {
//         console.log("Script is running for Appointment DocType");
//     }
// });



