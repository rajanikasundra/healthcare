
frappe.ui.form.on('Appointment', {
    refresh: function (frm) {

        frm.set_df_property('customer_name', 'reqd', 0);
    
        frm.set_df_property('customer_name', 'hidden', 1);

        if (!frm.is_new() && frm.doc.status === 'Approved') {
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

                            
                          
                            // frm.set_value('status', 'Completed');  
                            // frm.save().then(function() {
                            //     frm.reload_doc();  // Reload the document after saving
                            // }).catch(function(err) {
                            //     frappe.msgprint(__('Error while saving the document: ') + err.message);
                            // }); 
                        }
                    }
                });
            });
        } else {
            frm.page.get_primary_action().hide();  
        }

       
    }
});














































// frappe.ui.form.on('Appointment', {
//     refresh: function (frm) {
//         if (!frm.is_new() && frm.doc.status === 'Open') {
//             if (!frm.doc.custom_invoice_created) {
        
//                 frm.page.set_primary_action(__('Create Doctor Charge Invoice'), function () {
//                     frappe.call({
//                         method: "healthcare.payment_entry.generate_appointment_invoice", 
//                         args: {
//                             appointment_name: frm.doc.name
//                         },
//                         callback: function (response) {
//                             if (response.message) {
//                                 frappe.show_alert({
//                                     message: __('Sales Invoice Created: {0}', [response.message]),
//                                     indicator: 'green'
//                                 });
//                                 window.location.href = "/app/sales-invoice/" + response.message;

//                                 frm.set_value('custom_invoice_created', 1);
//                                 frm.save();
//                             }
//                         }
//                     });
//                 });
//             }else {
                
//                 frm.page.get_primary_action().hide();
//             }
//         }
//     }
// });





// // frappe.ui.form.on('Appointment', {
// //     refresh: function (frm) {
// //         if (!frm.is_new()) {
// //             // Add Generate Invoice Button
// //             frm.add_custom_button(__('Doctor Charge Invoice'), function () {
// //                 frappe.call({
// //                     method: "healthcare.payment_entry.generate_appointment_invoice",
// //                     args: {
// //                         appointment_name: frm.doc.name
// //                     },
// //                     callback: function (response) {
// //                         if (response.message) {
// //                             frappe.show_alert({
// //                                 message: __('Sales Invoice Created: {0}', [response.message]),
// //                                 indicator: 'green'
// //                             });
// //                             window.location.href = "/app/sales-invoice/" + response.message;
// //                         }
// //                     }
// //                 });
// //             }, __("A"));
// //         }
// //     }
// // });




